import sys
import argparse
import os

permlist = []

def extract_permissions(package_file, outformat, replace):
    if os.path.isdir(package_file):
        for subdir, dirs, files in os.walk(package_file):
            for file in files:
                if not file.endswith(".java"):
                    continue
                filepath = subdir + os.sep + file
                extract_permissions_from_file(file_reader(filepath), outformat, replace)
    else:
        extract_permissions_from_file(file_reader(package_file), outformat, replace)
    
def extract_permissions_from_file(file_content, outformat, replace):
    lines = file_content.split('\n')
    for line in lines:
        line = line.strip()
        if not line.startswith("@PreAuthorize") and not line.startswith("//@PreAuthorize") and not line.startswith("@PreAuthorizePermission") and not line.startswith("//@PreAuthorizePermission"):
            continue
        annotation_part = get_value_between(line, '(', ')')
        roles = annotation_part.split(',')
        for role in roles:
            role = strip_quotes(role)
            if role in permlist:
                continue
            permlist.append(role)
            print(format_value(outformat, replace, role))
    
def format_value(outformat, replace, value):
    replace = replace.split(',')
    value = value.replace(replace[0], replace[1])
    return outformat.replace("#{value}", value)
    
def strip_quotes(permission):
    permission = get_value_between(permission, "{", "}")
    permission = get_value_between(permission, "'", "'")
    permission = get_value_between(permission, '"', '"')
    return permission
    
def get_value_between(unprocessed, opening, closing):
    unprocessed = unprocessed.split(opening)
    index = len(unprocessed)-1
    while (index > 0):
        value = unprocessed[index]
        if value.strip() != "":
            unprocessed = value
            break
        index = index-1
    if type(unprocessed) == list:
        unprocessed = unprocessed[0]
    unprocessed = unprocessed.split(closing)
    if len(unprocessed) > 0:
        return unprocessed[0]
    return ""
    
def file_reader(source_file_path):
    if not os.path.isfile(source_file_path):
        print(source_file_path, "does not exist")
        exit(1)
    return open(source_file_path, "r").read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract all the spring security roles and permissions declared with @PreAuthorized annotation from a project.')
    parser.add_argument('package_file', help='The package folder or Java file')
    parser.add_argument('--outformat', default="#{value}", help="The output format to export each permission, default is '#{value}' which export like 'ROLE_ADMIN'")
    parser.add_argument('--replace', default=",", help="Replace part of the output value with another value, e.g. for value 'ROLE_ADMIN' 'ROLE_,R_'='R_ADMIN', 'ROLE_,'='ADMIN'")
    
    args = parser.parse_args()
    extract_permissions(args.package_file, args.outformat, args.replace)