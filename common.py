#!/usr/bin/env python3

import os
import hashlib
import shutil
import re
import glob


ROOTINVARIANT = '/mnt/us'


def get_hash(path):
    return hashlib.sha1(path.encode('utf-8')).hexdigest()


def safecopy(src, dstdir):
    dst = os.path.join(dstdir, os.path.basename(src))
    while os.path.exists(dst):
        parts = os.path.splitext(dst)
        dst = parts[0] + "_samename" + parts[1]

    shutil.copy2(src, dst)


def read_docs_folder(root):
    extensions = ['pdf', 'mobi', 'prc', 'txt', 'tpz', 'azw1', 'azw', 'manga', 'azw2', 'azw3']
    file_paths = []
    for extension in extensions:
        file_paths += glob.glob(root + "/documents/**/*.{}".format(extension), recursive=True)
    output = []
    asin_finder = re.compile(".*-asin_(.*)-type_.*")
    short_asin_finder = re.compile(".*-asin_(.*)\..*")

    for file_path in file_paths:
        file_properties = {}
        canonic_filename = file_path.replace(root, ROOTINVARIANT)
        file_properties["path"] = file_path
        file_properties["name"] = os.path.basename(file_path)
        file_properties["canonic_filename"] = canonic_filename
        file_properties["hash"] = get_hash(canonic_filename)
        file_properties["asin"] = None
        file_properties["processed"] = False
        asin_match = asin_finder.match(file_properties["name"])
        if not asin_match:
            asin_match = short_asin_finder.match(file_properties["name"])

        if asin_match:
            #maybe urlencode is better, but I don't have means to prove it
            file_properties["asin"] = asin_match.group(1).replace("!", "%21")
#        else:
#            print("non-asin: %s" % file_properties["name"])

        output += [file_properties]

    return output

def get_fileproperties(files, filepath):
    result = list(filter(lambda x: x["path"] == filepath, files))
    assert len(result) == 1, "multiple files with same paths. strange."
    return result[0]

