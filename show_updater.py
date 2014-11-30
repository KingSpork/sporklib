import sporklib_utils
import sporklib
import argparse


arg_parser = argparse.ArgumentParser(description="Renames a directory of TV shows to more pleasant format")


arg_parser.add_argument("-d", "--dir", required=True, help="The directory containing the shows you'd like to rename")
arg_parser.add_argument("-n", "--name", required=True, help="Name of the show as you'd like it to appear. Pass UPDATE (all caps) to use name of show that is majority in directory.")
arg_parser.add_argument("-r", "--dryrun", required=False, help="Do a \"dry run\", printing new names but taking no action", action="store_true")

args = arg_parser.parse_args()

dir = sporklib.normalize_path(args.dir)
name = args.name
dry_run = args.dryrun

if dir == "":
    print("ERROR: Directory not specified")
    exit(1)
if name == "":
    print("ERROR: Name not specified")
    exit(2)

if name == "UPDATE":
    scoreboard = {}
    files_list = sporklib.list_files(dir, True, False)
    
    for file in files_list:
        fn = file.split(" - ")[0]
        if fn in scoreboard:
            scoreboard[fn] += 1
        else:
            scoreboard[fn] = 1
        
    biggest_value = 0
    biggest_key = ""
    for k in scoreboard.keys():
        if scoreboard[k] > biggest_value:
            biggest_value = scoreboard[k]
            biggest_key = k
            
    name = biggest_key
    
    
sporklib_utils.files.rename_shows(dir, name, dry_run)