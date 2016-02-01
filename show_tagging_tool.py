import sporklib_utils
import sporklib
import argparse
from show_tagger import FileTagger
from random import randrange

g_engine = None
g_selected_record = None
g_search_results = []
g_yes_choices = ["yes", "y"]
YN = " Y/N\n"

class DoNotProceedException(Exception):
    def __init__(self):
        Exception.__init__(self,"Command received signal to not proceed.") 


        
def verify_args(arg_name="", *args):
    if arg_name == "":
        arg_name = "args"
    if not args:
        print("No % provided." % arg_name)
        raise DoNotProceedException
        
def verify_record_selected():
    if not g_selected_record:
        print("No record selected.")
        raise DoNotProceedException
    
            
def get_tag_from_int(n):
    return g_engine.get_avail_tags()[n+1]
        

def add_tags(tags):
    for t in tags:
        tag_to_add = get_tag_from_int(int(t))
        g_engine.add_tag_to_record(g_selected_record, tag_to_add)
        print("Successfully added tag: %s to record: %s" % tag_to_add, g_selected_record["name"])


def remove_tags(tags):
    for t in tags:
        tag_to_remove = get_tag_from_int(int(a))
        g_engine.remove_tag_from_record(g_selected_record, tag_to_remove)
        print("Successfully remove tag: %s to record: %s" % tag_to_remove, g_selected_record["name"])


def select_record_by_name(name):
    global g_selected_record
    try:
        g_selected_record = g_engine.get_records()[name]
    except KeyError:
        print("Cannot select record: record does not exist")
        
def select_random_record():
    global g_selected_record
    records = g_engine.get_records()
    rando = randrange(0,len(records))
    print("RANDO IS: %s" % rando)
    key = records.keys()[rando]
    print("KEY IS %s" % key)
    print("RAND REC %s" % records[key])
    g_selected_record = records[key]
    
def search_records_by_tags(tags):
    global g_search_results
    search_results = g_engine.get_tag_matches(tags)
    i = 0
    for r in search_results.keys():
        g_search_results[i] = r


def filter_records_by_tags(tags):
    global g_search_results
    search_results = g_engine_filter_by_tags(tags)
    i = 0
    for r in search_results.keys():
        g_search_results[i] = r

def create_tags(tags):
    for t in tags:
        g_engine.add_tag_to_avail(t)
        
def print_search_results():
    print("*** SEARCH RESULTS ***")
    sporklib.print_list_of_items(g_search_results)
    

def get_all_records():
    global g_search_results
    search_results = []
    for k in g_engine.get_records().keys():
        search_results.append(k)
    g_search_results = search_results
    
def print_selected_record():
    print("SELECTED RECORD IS: " + g_selected_record["name"])
    
def run_command(command_type, *args):

    command_types = {
        "help": ["help", "h"],
        "add_tags": ["add", "a"],
        "remove_tags": ["remove", "rem"],
        "select_record_by_name": ["selectname", "sn"],
        "select_random_record": ["random", "sr", "r"],
        "search_records_by_tags": ["search", "s","t"],
        "filter_records_by_tags": ["filter", "f",],
        "get_tags": ["get", "g"],
        "save": ["save"],
        "discard": ["discard"],
        "print_search_results": ["show","results", "u"],
        "create_tags": ["create", "c", "new"],
        "scan_content_dir": ["scan", "refresh"],
        "exit": ["exit", "quit", "x"],
        "browse":["browse", "b"],
        "print_selected_record":["printselected", "p"],
        "play_selected_record":["play", "y"],
        "print_avail_tags": ["avail", "tags"]
    }
    
    if command_type in command_types["help"]:
        print("COMMANDS ARE AS FOLLOWS:")
        for k in command_types.keys():
            print(k + ": " + str(command_types[k]))
    
    elif command_type in command_types["add_tags"]:
        fail_msg = "Cannot add tag(s). "
        try:
            verify_args("tags", args)
            verify_record_selected()
            add_tags(list(args))
        except DoNotProceedException:
            print(fail_msg)
        
        
    elif command_type in command_types["remove_tags"]:
        fail_msg = "Cannot remove tag(s). "
        try:
            verify_args("tags", args)
            verify_record_selected()
            remove_tags(list(args))
        except DoNotProceedException:
            print(fail_msg)
        
    elif command_type in command_types["select_record_by_name"]:
        fail_msg = "Cannot select record by name."
        try:
            verify_args("name", args)
            select_record_by_name(args[0])
        except DoNotProceedException:
            print(fail_msg)
            
    elif command_type in command_types["select_random_record"]:
        select_random_record()
        
    elif command_type in command_types["search_records_by_tags"]:
        fail_msg = "Cannot search by tags."
        try:
            verify_args("tags", args)
            search_records_by_tags(list(args))
            print_search_results()
        except DoNotProceedException:
            print(fail_msg)
    
    elif command_type in command_types["filter_records_by_tags"]:
        fail_msg = "Cannot filter by tags."
        try:
            verify_args("tags", args)
            filter_records_by_tags(list(args))
            print_search_results()
        except DoNotProceedException:
            print(fail_msg)
            
            
    elif command_type in command_types["print_search_results"]:
        print_search_results()
        
    elif command_type in command_types["save"]:
        inp = raw_input("Are you sure you want to save settings?" + YN)
        if inp in g_yes_choices:
            print("Saving...")
            g_engine.save_changes()
            print("Saved.")
        else:
            print("Save canceled.")

    elif command_type in command_types["create_tags"]:
        fail_msg = "Cannot create tag."
        try:
            verify_args("tags")
            create_tags(list(args))
        except DoNotProceedException:
            print(fail_msg)
            
    elif command_type in command_types["discard"]:
        inp = raw_input("Are you sure you want to discard all changes?" + YN)
        if inp in g_yes_choices:
            inp = raw_input("Are you absolutely positive?" + YN)
            if inp in g_yes_choices:
                print("Reloading all data from disk...")
                g_engine.load_settings()
                print("Changes reset.")
                
    elif command_type in command_types["scan_content_dir"]:
        print("Scanning content directory for new files... ")
        g_engine.add_content_to_records()
    
    elif command_type in command_types["browse"]:
        get_all_records()
        print_search_results()
        
    elif command_type in command_types["exit"]:
        inp = raw_input("Are you sure you want to exit?" + YN)
        if inp in g_yes_choices:
            exit()
    
    elif command_type in command_types["print_selected_record"]:
        fail_msg = "Could not print selected record."
        try:
            verify_record_selected()
            print_selected_record()
        except DoNotProceedException:
            print(fail_msg)
        
    
    elif command_type in command_types["play_selected_record"]:
        fail_msg = "Could launch selected record."
        try:
            verify_record_selected()
            print("Launching file: %s" % g_selected_record["name"])
            g_engine.play_record_file(g_selected_record)
        except DoNotProceedException:
            print(fail_msg)
    
    elif command_type in command_types["print_avail_tags"]:
        print("AVAIL TAGS ARE:")
        g_engine.print_avail_tags()
    else:
        print("Unrecognized command type \"%s\"" % command_type)
    

        
def intro():
    global g_engine
    print("Welcome to the interactive Video Tagging Tool.")
    print("Copyright 2014-2016 Paul Bellamy")
    print("Loading VTT Engine...")
    g_engine = FileTagger()
    print("You settings are the following:")
    print("Content Directory: %s" % g_engine.CONTENT_DIRECTORY)
    print("Records Path: %s" % g_engine.RECORDS_PATH)
    print("Available tags path: %s" % g_engine.AVAIL_TAGS_PATH)
    inp = raw_input("Would you like to scan for new content?" + YN)
    if inp in g_yes_choices:
        run_command("scan")
        
intro()
while True:
    inp = raw_input("CMD >> ")
    inp_sequence = inp.split(" ")
    cmd_type = inp_sequence[0]
    args = inp_sequence[1:]
    run_command(cmd_type, args)
    