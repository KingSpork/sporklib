import sporklib_utils
import sporklib
import argparse


arg_parser = argparse.ArgumentParser(description="Renames a directory of TV shows to more pleasant format")


arg_parser.add_argument("-d", "--dir", required=True, help="The directory containing the shows you'd like to rename")
arg_parser.add_argument("-t", "--target", required=True, help="Directory to extract unique files to")
arg_parser.add_argument("-r", "--dryrun", required=False, help="Do a \"dry run\", printing unique file names but taking no action", action="store_true")
arg_parser.add_argument("-m", "--move", required=False, help="Move files instead of copying them.", action="store_true")

args = arg_parser.parse_args()

dir = sporklib.normalize_path(args.dir)
target = sporklib.normalize_path(args.target)
dry_run = args.dryrun
move = args.move

if dir == "":
    print("ERROR: Directory not specified")
    exit(1)
if target == "":
    print("ERROR: target not specified")
    exit(2)


    
sporklib_utils.files.extract_unique_files(dir, target, move, dry_run)
