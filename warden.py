import hcl
import json
import sys
import collections
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


def are_objects_equal(x, y):
    return collections.Counter(x) == collections.Counter(y)


def check_tags(service_hcl, policy):
    list_of_tags = service_hcl[service_hcl.keys()[0]]["tags"].keys()
    return are_objects_equal(list_of_tags, policy["tags"])


def check_exist(service_hcl, policy):
    checks = []
    for policy in policy["exist"]:
        policy_obj = service_hcl[service_hcl.keys()[0]][policy.keys()[0]]
        checks.append(are_objects_equal(policy_obj, policy[policy.keys()[0]]))
    if False not in checks:
        return True


def check_not_exist(service_hcl, policy):
    checks = []
    for prop in policy["not-exist"]:
        if prop in service_hcl[service_hcl.keys()[0]]:
            checks.append(False)
        else:
            checks.append(True)
    if False not in checks:
        return True


def check_for_policy_complience(service_name, service_hcl):
    with open("policies/"+service_name+".json", 'r') as fp:
        json_obj = json.loads(fp.read())
        if check_tags(service_hcl, json_obj) and \
           check_exist(service_hcl, json_obj) and \
           check_not_exist(service_hcl, json_obj):
            return True
        else:
            return False


def check_policies(hcl_obj):
    policies_list = listdir("policies")
    cleaned_policies_list = []
    for pol in policies_list:
        cleaned_policies_list.append(pol.split(".json")[0])
    for service in hcl_obj:
        for ser in service.keys():
            if ser in cleaned_policies_list:
                return check_for_policy_complience(ser, service[ser])
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
    print check_policies(all_resources)
    # pp = pprint.PrettyPrinter()
    # pp.pprint(get_resources(all_hcl_obj))


if __name__ == "__main__":
    main()
