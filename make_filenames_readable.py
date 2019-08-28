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
    make_filenames_readable.py -r kindleroot
'''

def rename_files(root):
    all_files = glob.glob(root + "/documents/**/*.*", recursive=True)
    for filepath in all_files:
        ext = os.path.splitext(filepath)[1]
        directory = os.path.dirname(filepath)
        e = Ebook(filepath)
        title = e.title
        author = e.author if e.author else "Unknown"
        new_filename = u"[{}]-{}".format(author, title)
        new_filename = new_filename.replace(" ", "_")
        new_filename = new_filename.replace("/", "_")
        new_filename = new_filename.replace("\\", "_")
        new_path = os.path.join(directory, new_filename + ext)
        os.rename(filepath, new_path)


           
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
    rename_files(args.root)
    print("done.")

main()



