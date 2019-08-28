#!/usr/bin/env python3

import os
import shutil
import glob
from ebook import Ebook

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

    for file_path in file_paths:
        e = Ebook(file_path)
        file_properties = {}
        file_properties["path"] = file_path
        file_properties["name"] = os.path.basename(file_path)
        file_properties["canonic_filename"] = e.path
        file_properties["hash"] = e.hash
        file_properties["asin"] = e.asin
        file_properties["processed"] = False

        output += [file_properties]

    return output

def get_fileproperties(files, filepath):
    result = list(filter(lambda x: x["path"] == filepath, files))
    assert len(result) == 1, "multiple files with same paths. strange."
    return result[0]

