#!/usr/bin/python

import os
import sporklib
import shutil

class file(object):

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
				
	@staticmethod			
	def find_matching_file(match_str, tgt_dir,