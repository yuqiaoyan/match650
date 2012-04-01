import sys
import json
import urllib
import csv
from indexing import addDoc, initializeIndex
from lucene import *
from BeautifulSoup import *

NAME_KEY = 'name'
INTEREST_KEY = 'interest'
ID_KEY = 'Id'
AFFLI_KEY = 'Affiliation'
INTERESTS_PATH = 'getData/person_interest.csv'


def interest_dict (file_name):
    reader = csv.reader(open(file_name, 'r'), delimiter=',',
            quotechar='\"')
    re_dict = {}
    for line in reader:
        re_dict[line[0]] = line[1]
    return re_dict
IN_DICT = interest_dict(INTERESTS_PATH)

def get_info(name, *attributes):
# get information from arnetminer
    url = "http://arnetminer.org/services/person/"
    url = url + name + "?u=oyster&o=tff"
    jsonString = urllib.urlopen(url).read()
    json_list = json.loads(jsonString)
    result = {}
    if json_list:
        re_dict = json_list[0]
        for key in attributes:
            if key == ID_KEY:
                Id = str(re_dict[key])
                result[INTEREST_KEY] = get_interest_by_id(Id)
                continue
            try:
                result[key.lower()] = str(re_dict[key].encode('utf8'))
            except KeyError:
                print >> sys.stderr, "the key", key, "doesn't exist!, set to empty string!"
                result[key.lower()] = ' '
    result[NAME_KEY] = name
    return result

def get_interest_by_id(Id):
    return IN_DICT.get(Id)

def read_file_build(name_list):
    writer = initializeIndex()
    with open(name_list, 'r') as f:
        for line in f:
            name = line.strip()
            print name
            profile = get_info(name, ID_KEY, AFFLI_KEY)
            if profile[INTEREST_KEY]:
                addDoc(writer, profile)
    writer.commit()

if __name__ == '__main__':
    read_file_build(sys.argv[1])


