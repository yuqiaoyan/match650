import BeautifulSoup as bs
import re
pattern = r'^(.*) \((.*)\)'

def get_name(file_name):
    doc = bs.BeautifulSoup(open(file_name, 'r'))
    name_blocks = doc.findAll('li')
    name_list = [re.findall(pattern ,item.text)[0].rstrip() for item in name_blocks if re.findall(pattern ,item.text)]
    return name_list

def write_name_file(name_list):
    with open('name_list', 'a') as f:
        for name in name_list:
            f.write("%s\n" % name)

if __name__ == "__main__":
    file_1 = 'KDD-2012  Conference Organizers.htm'
    file_2 = 'KDD-2012 ResearchProgramCommitteeList.htm'
    name_l_1 = get_name(file_1)
    name_l_2 = get_name(file_2)
    write_name_file(list(set(name_l_1+name_l_2)))


