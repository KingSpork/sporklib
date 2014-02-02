#!/usr/bin/python

import os
import string
import argparse
import hashlib
import shutil



'''
safe_move allows you to move a file without fear of overwriting the dest. dir.
'''
def safe_move(path_source, path_dest):
    shutil.copy2(path_source, path_dest)
    os.remove(path_source)

'''
safe_mkdir will only make a directory if it does not exist
'''
def safe_mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
		
def zip_dir(dir_path, dest_path=""):

		
def __zip_dir(path, zipfile_obj_w, searchstr="", verbose=False):
    '''
	Path is path to the file you want to zip
    zip is a ZipFile object opened in write mode
	
    if you specify a searchstr equivalent to a directory name, zipadir will find that string in the full filepath
    and truncate the zipped path to that point.  For example if your full path is "/Users/pbellamy/Documents/file.txt"
    and you specify the searchstr "Documents" the zip file will contain "/Documents/file.txt" instead of burying it
    under the empty folders "/Users/pbellamy".
    '''
	for root, dirs, files in os.walk(path):
        for file in files:

            if search_str != "":
                index = root.index(search_str)
                zroot = "/" + root[index:]
            else:
                zroot = root

            fpath = root + "/" + file
            zpath = zroot + "/" + file
            '''
			print("ROOT: ");print(root) #DEBUG
            print("DIRS: ");print(dirs) #DEBUG
            print("FILES: ");print(files) #DEBUG
            print("FPATH:");print(fpath) #DEBUG
            print("ZROOT:");print(zroot) #DEBUG
            print("ZPATH:");print(zpath) #DEBUG
			'''
            zipfile_obj_w.write(fpath, zpath)		
		
		
		
		
'''
hash_file creates an md5 hash of a file's contents.
'''
def hash_file(path, validate_file=True):
    proceed = True
    if validate_file:
        proceed = os.path.isfile(path)

    if proceed:
        with open(path, "rb") as file:
            hasher = hashlib.md5()
            data = file.read()
            hasher.update(data)
            file_hash = hasher.hexdigest()
            del hasher

        return file_hash
    return

        
'''
hash_dir takes a directory and returns a dict where the key is a hash of the
file's contents and the value is the path to the file.
'''
def hash_dir(path, return_dupes=False):
    path = normalize_path(path)
    hash_dict = {}
    dupes = {}
    files = list_files(path, True)
    
    for file in files:
        h = hash_file(file)

        if h in hash_dict:
            if return_dupes:
                if h in dupes:
                    dupes[h].append(file)
                else:
                    dupes[h] = [hash_dict[h], file]
        else:
            hash_dict[h] = file

    if return_dupes:
        return (hash_dict, dupes)
    return hash_dict


'''
get_path_target returns the filename/directory name of the path target
'''
def get_path_target(path, return_root=False):
    path = normalize_path(path)
    i = path.rfind("/")
    if return_root:
        return tuple(path[:i], path[i+1:])
    return path[i+1:]
    

'''
diff_dir will return the paths of all files in path_1 that are not in path_2.
It is determined by file CONTENTS, not name.
'''
def diff_dir(path_1, path_2):
    hashes_1 = hash_dir(path_1)
    hashes_2 = hash_dir(path_2)
    uniques = tuple(filter(lambda x: x not in hashes_2, hashes_1))
    return dict((key, hashes_1[key]) for key in uniques)


'''
normalize_path replaces backslashes with forward slashes. Much more civilized.
'''
def normalize_path(path, skip_trailing_check=False):
    path = string.replace(path, "\\", "/")
    if not skip_trailing_check:
        l = len(path) - 1
        if path[l] == "/":
            path = path[:l]
    return path

'''
list_files returns a dict containing file and directory names or paths
'''
def list_files(path, files_only=False, full_paths=True):
    path = normalize_path(path)
    files = os.listdir(path)
    all_list = []
    files_list = []

    for file in files:

        if full_paths:
            file = path + "/" + file
            all_list.append(file)
        
        if os.path.isfile(file):
            files_list.append(file)

    if files_only:
        return files_list
        
    return {"dirs":list(set(files_list) ^ set(all_list)),
        "files":files_list}
