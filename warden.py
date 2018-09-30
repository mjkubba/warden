import hcl
from os import listdir
import pprint

def combine_hcl(dir):
    hcl = ""
    file_list = listdir(dir)
    for file in file_list:
        if ".tf" in file:
             with open(dir+file, 'r') as fp:
                 hcl = hcl + fp.read()
    return hcl

def get_modules(hcl_obj):
    snd_file = []
    for key in hcl_obj.keys():
        for in_key in hcl_obj[key].keys():
            if "source" in hcl_obj[key][in_key]:
                snd_file.append(hcl_obj[key][in_key]["source"])
    return snd_file

def get_resources(hcl_obj):
    resouces = []
    for key in hcl_obj.keys():
        if (key == "resource"):
            resouces.append(hcl_obj[key])
    return resouces

def main():

    combined_hcl = combine_hcl("../tf-s3/")
    hcl_obj = hcl.loads(combined_hcl)
    for mod in get_modules(hcl_obj):
        all_hcl_obj = dict(hcl_obj)
        all_hcl_obj.update(hcl.loads(combine_hcl("../tf-s3/"+mod)))

    # pprint is a pretty printer, useful to print and read json(dict) in a friendly way
    pp = pprint.PrettyPrinter()
    pp.pprint(get_resources(all_hcl_obj))


if __name__ == "__main__":
    main()
