#!/usr/bin/env python3

import sys
import os
import argparse
import json
import glob

import common
from ebook import Ebook

EPILOG = r'''
Examples
--------
    collections2filesys.py --output output --input kindleroot 
'''
           
def create_collections_by_filesystem(root):
    all_dirs = glob.glob(root + "/documents/**/*/", recursive=True)
    toplevel_dirs = glob.glob(root + "/documents/*/")
    if all_dirs != toplevel_dirs:
        print("only single level of nesting supported currently")
        exit()

    collections = {}

    for directory in toplevel_dirs:
        # normpath to remove trailing slash
        directory_name = os.path.basename(os.path.normpath(directory))
        collection_name = directory_name + "@en-US"
        collections[collection_name] = {"items": [], "lastaccess" : 0}
        filepaths = glob.glob(directory + "/*")
        for filepath in filepaths:
            e = Ebook(filepath)
            collections[collection_name]["items"] += [e.fileident()]

    return collections


def main():
    arg_parser = argparse.ArgumentParser(
        description="",
        epilog=EPILOG,
        formatter_class=argparse.RawTextHelpFormatter)

    arg_parser.add_argument(
        "-r",
        "--root",
        required=True,
        help="Kindle root directory")

    arguments = sys.argv[1:]
    args = arg_parser.parse_args(arguments)

    print("taking kindle filesystem from %s" % args.root)

    collections = create_collections_by_filesystem(args.root)

#    print(json.dumps(collections, sort_keys=True, indent=4))

    out_dir = os.path.join(args.root, "system")
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, "collections.json"), 'w') as outfile:
        json.dump(collections, outfile, sort_keys = True, indent = 4, ensure_ascii = True)

main()



