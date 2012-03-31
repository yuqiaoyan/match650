import sys
import json
import urllib
import csv
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
    print attributes
    result = {}
    if json_list:
        re_dict = json_list[0]
        for key in attributes:
            try:
                if key == ID_KEY:
                    Id = str(re_dict[key])
                    result[INTEREST_KEY.lower()] = get_interest_by_id(Id)
                    continue
                result[key] = str(re_dict[key])
            except KeyError:
                print >> sys.stderr, "the key", key, "doesn't exist!"
    result[NAME_KEY] = name
    return result

def get_interest_by_id(Id):
    return IN_DICT.get(Id)

def read_file_build(name_list):
    with open(name_list, 'r') as f:
        for line in f:
            name = line.strip()
            print name
            profile = get_info(name, ID_KEY, AFFLI_KEY)
            print profile

if __name__ == '__main__':
    read_file_build(sys.argv[1])


