#!/usr/bin/python

import os
import sporklib
import shutil
import re

class files(object):
    @staticmethod
    def rename_shows(dir, show_name, dry_run=False):

        video_formats = [".mpg", ".mp4", ".avi", ".mkv", ".mpeg"]
    
        dir = sporklib.normalize_path(dir)
        season = "XX"
        episode = "XX"
        re_season = "[Ss]\d{1,2}"
        re_episode = "[Ee]\d{1,2}"
        files = []

        file_paths = sporklib.list_files(dir, True)
        #print("File paths are:");print(file_paths)
        
        for path in file_paths:
            i = path.rfind("/")
            f = path[i+1:]
            files.append(f)

        if len(file_paths) != len(files):
            raise IndexError("List of file paths did not have corresponding indices in list of file names.")

        #print("Renaming files in the following list:");print(files)

        i = 0
        for filename in files:    
            ext_i = filename.rfind(".")
            extension = filename[ext_i:]
            
            if extension in video_formats:
            
                new_name = ""
                
                s_matcher = re.compile(re_season)
                e_matcher = re.compile(re_episode)

                looper = [["s", s_matcher], ["e", e_matcher]]

                for loop in looper:

                    matcher = loop[1]

                    mo = matcher.search(filename)

                    if mo != None: #regex failed              
                        positions = mo.span()

                        match = filename[positions[0]:positions[1]]

                        match = re.sub("[^0 -9]", "", match)
                        match = int(match)

                        if match > 9:
                            match = str(match)
                        else:
                            match = "0" + str(match)

                        if loop[0] == "s":
                            season = match
                        elif loop[0] == "e":
                            episode = match
                        else:
                            print("ERROR! DID NOT RECOGNIZE LOOP DIRECTIVE: " + loop[0])
                            #raise exception here



                new_name = show_name + " - S" + season + "E" + episode + extension
               
                print(new_name)
                
                if dry_run == False:
                    path = file_paths[i]
                    print(path + " ----> " + dir + "/" + new_name)
                    os.rename(path, dir + "/" + new_name)
            
                i += 1


	@staticmethod
	def extract_unique_files(dir_1, dir_2, dir_dest, move=False):

		if (os.path.isfile(dir_1)) or (os.path.isfile(dir_2)) or (os.path.isfile(dir_dest)):
			raise IOError("extract_unique_files takes only directories as arguments, not files.")

		dir_dest = sporklib.normalize_path(dir_dest)
		sporklib.safe_mkdir(dir_dest)

		diff_hashes = sporklib.diff_dir(dir_1, dir_2)

		if move:
			for hash,path in diff_hashes.items():
				sporklib.safe_move(path, dir_dest)
		else:
			for hash,path in diff_hashes.items():
				shutil.copy2(path, dir_dest)

	@staticmethod
	def extract_duplicate_files(dir_source, dir_dest, move=False):
		if (os.path.isfile(dir_source)) or (os.path.isfile(dir_dest)):
			raise IOError("extract_unique_files takes only directories as arguments, not files.")

		dir_dest = sporklib.normalize_path(dir_dest)
		sporklib.safe_mkdir(dir_dest)

		dupes = sporklib.hash_dir(dir_source, True)[1]

		if move:
			for hash,paths in dupes.items():
				for p in paths[1:]:
					sporklib.safe_move(p, dir_dest)
		else:
			for hash,paths in dupes.items():
				for p in paths:
					shutil.copy2(p, dir_dest)

#	@staticmethod
#	def find_matching_file(match_str, tgt_dir,