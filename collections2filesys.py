#!/usr/bin/env python3

import sys
import os
import argparse
import json
import re

import common

EPILOG = r'''
Examples
--------
    collections2filesys.py --output output --input kindleroot 
'''

def resolve(item, kindle_files):
    asin_re = re.compile("#(.*)\^.*")
    hash_re = re.compile("\*([a-z0-9]{40})")
    asin_match_obj = asin_re.match(item)
    hash_match_obj = hash_re.match(item)
    if asin_match_obj:
        id = asin_match_obj.group(1)
        column = "asin"
    elif hash_match_obj:
        id = hash_match_obj.group(1)
        column = "hash"
    else:
        print("bullshit")
        exit()

    for f in kindle_files:
        if f[column] == id:
            return f["path"]

    return ""

def resolve_all(items, kindle_files):
    result = []
    for item in items:
        result += [resolve(item, kindle_files)]
    return result

def read_collections_json(root, kindle_files):
    try:
        path_to_file = os.path.join(root, "system", "collections.json")
        json_file = open(path_to_file, "r")
        content = json.load(json_file)
    except:
        content = {}

    for (key, value) in content.items():
         value["items_filepath"] = resolve_all(value["items"], kindle_files)

    return content
    
def collection_name(collection_key):
    parts = collection_key.split("@")
    return parts[0]
    
def collections_to_folder(inputroot, outputroot, collections_config, files):
    for (key, value) in collections_config.items():
        collection = collection_name(key)
        out_dir = os.path.join(outputroot, collection)
        os.makedirs(out_dir, exist_ok=True)
        for index, item in enumerate(value["items_filepath"]):
            if item:
                common.safecopy(item, out_dir)
                files_items = [x for x in files if x["path"] == item]
                assert len(files_items) == 1, "something wrong with files"
                files_items[0]["processed"] = True
            else:
                print("collection [%s]: skipped unresolved item %s" % (collection, value["items"][index]))

    for f in files:
        if not f["processed"]:
             common.safecopy(f["path"], outputroot)
            

def main():
    arg_parser = argparse.ArgumentParser(
        description="",
        epilog=EPILOG,
        formatter_class=argparse.RawTextHelpFormatter)

    arg_parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input directory")

    arg_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output directory")

    arguments = sys.argv[1:]
    args = arg_parser.parse_args(arguments)

    print("taking kindle filesystem from %s -> putting output to %s" % (args.input, args.output))

    files = common.read_docs_folder(args.input)
    collections_config = read_collections_json(args.input, files)
#    print(json.dumps(collections_config, sort_keys=True, indent=4))

    collections_to_folder(args.input, os.path.join(args.output, "documents"), collections_config, files)

main()



