import hcl
import json
import sys
from os import listdir


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


def check_if_allowed_service(hcl_obj):
    with open("services/allowed.json", 'r') as fp:
        json_obj = json.loads(fp.read())
        for service in hcl_obj:
            for ser in service.keys():
                if ser not in json_obj:
                    return False
    return True


def check_for_policy_complience(service_name, service_hcl):
    print service_name, service_hcl
    with open("policies/"+service_name+".json", 'r') as fp:
        json_obj = json.loads(fp.read())
        # print service_hcl["tags"]
    return True


def check_policies(hcl_obj):
    policies_list = listdir("policies")
    cleaned_policies_list = []
    for pol in policies_list:
        cleaned_policies_list.append(pol.split(".json")[0])
    for service in hcl_obj:
        for ser in service.keys():
            if ser in cleaned_policies_list:
                check_for_policy_complience(ser, service[ser])
            else:
                print "Service: '" + ser + "' Do not have policy"


def main():
    directory = sys.argv[1]
    combined_hcl = combine_hcl(directory)
    hcl_obj = hcl.loads(combined_hcl)
    for mod in get_modules(hcl_obj):
        all_hcl_obj = dict(hcl_obj)
        all_hcl_obj.update(hcl.loads(combine_hcl(directory+mod)))
    all_resources = get_resources(all_hcl_obj)
    print check_if_allowed_service(all_resources)
    check_policies(all_resources)
    # pp = pprint.PrettyPrinter()
    # pp.pprint(get_resources(all_hcl_obj))


if __name__ == "__main__":
    main()
