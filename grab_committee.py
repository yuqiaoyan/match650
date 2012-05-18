import json
import urllib
import csv
import time


def get_info(name, *attributes):
    """
        get information of committees from Arnetminer
    """
    print 'getting info of', name
    url = "http://arnetminer.org/services/person/"
    url = url + name + "?u=oyster&o=tff&fields=:phduniv,phdmajor,\
                        phddate,msuniv,msmajor,msdate,bsuniv,\
                        bsmajor,bsdate,bio"
    jsonString = urllib.urlopen(url).read()
    return jsonString

def get_name(source_file):
    name_list = []
    with open(source_file) as sf:
        name_list = [name.strip() for name in sf if name]
    return name_list

def save_info(name_list, destination_file, error_fixing = False):
    error_list = []
    with open(destination_file, 'a') as df:
        if error_fixing:
            print 'fixing!'
        for name in name_list:
            try:
                json_string = get_info(name)
                df.write("%s\n" % json_string)
            except:
                print 'error!'
                error_list.append(name)
    return error_list

if __name__ == "__main__":
    import sys
    source, destination = sys.argv[1:]
    print 'source file is', source
    print 'destination file is', destination
    name_list = get_name(source)
    error_list = save_info(name_list, destination)
    while error_list:
        error_list = save_info(error_list,destination, error_fixing =
                                True)
