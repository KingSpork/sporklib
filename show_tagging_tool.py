import sporklib_utils
import sporklib
import argparse
from show_tagger import ShowTagger
from random import randrange

g_engine = None
g_selected_record = None
g_search_results = []
g_yes_choices = ["yes", "y"]
YN = " Y/N\n"

class DoNotProceedException(Exception):
    def __init__(self):
        Exception.__init__(self,"Command received signal to not proceed.") 

def get_tags():
    return g_selected_record["tags"]
    
def get_actors():
    print g_selected_record
    return g_selected_record["actors"]
    
def verify_args(args_list=None, arg_type=None):
    if not args_list:
        print("Must supply args.")
        raise DoNotProceedException
    if arg_type:
        for a in args_list:
            try:
                arg_type(a)
            except ValueError:
                print("Arg %s not of type %s." % (a, arg_type.__name__))
                raise DoNotProceedException

    
    

def verify_record_selected():
    if not g_selected_record:
        print("No record selected.")
        raise DoNotProceedException

def get_record_count():
    return len(g_engine.get_records())
            
def get_tag_from_int(n):
    return g_engine.get_avail_tags()[n-1]

def get_actor_from_int(n):
    return g_engine.get_avail_actors()[n-1]
    
def create_new_actor(actor):
    g_engine.add_actor_to_avail(actor)
    print("Successfully added %s to available actors..." % actor)

def create_new_tag(tag):
    g_engine.add_tag_to_avail(tag)
    print("Successfully added %s to available tags..." % tag)
    
def add_tags(tags):
    for t in tags:
        print tags #DEBUG
        tag_to_add = get_tag_from_int(int(t))
        g_engine.add_tag_to_record(g_selected_record, tag_to_add)
        print("Successfully added tag: %s to record: %s" % (tag_to_add, g_selected_record["name"]))


def remove_tags(tags):
    for t in tags:
        tag_to_remove = get_tag_from_int(int(t))
        g_engine.remove_tag_from_record(g_selected_record, tag_to_remove)
        print("Successfully remove tag: %s to record: %s" % (tag_to_remove, g_selected_record["name"]))


def add_actor(actors):
    actor_to_add = get_actor_from_int(int(actors))
    print "tag to add: " + str(actor_to_add)
    g_engine.add_actor_to_record(g_selected_record, actor_to_add)
    print("Successfully added actor: %s to record: %s" % (actor_to_add, g_selected_record["name"]))


def remove_actor(actor):
    actor_to_remove = get_actor_from_int(int(actor))
    g_engine.remove_actor_from_record(g_selected_record, actor_to_remove)
    print("Successfully remove actor: %s to record: %s" % (actor_to_remove, g_selected_record["name"]))
        
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
    key = records.keys()[rando]
    g_selected_record = records[key]
    
def search_records_by_tags(tags):
    global g_search_results
    search_results = g_engine.get_tag_matches(tags)
    i = 0
    for r in search_results.keys():
        g_search_results[i] = r


def filter_records_by_tags(tags):
    global g_search_results
    search_results = g_engine.filter_by_tags(tags)
    i = 0
    for r in search_results.keys():
        g_search_results[i] = r


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
        "add_tags": ["add", "a", "+t"],
        "add_actor": ["adda", "ada", "+a"],
        "remove_actor": ["rema", "ra"],
        "create_actor": ["na"],
        "remove_tags": ["remove", "rem", "rt"],
        "select_record_by_name": ["selectname", "sn"],
        "select_random_record": ["random", "sr", "r"],
        "search_records_by_tags": ["search", "s","t"],
        "filter_records_by_tags": ["filter", "f",],
        "get_tags": ["gt", "g"],
        "get_actors": ["ga"],
        "save": ["save"],
        "discard": ["discard"],
        "print_search_results": ["show","results", "u"],
        "create_tag": ["create", "c", "new"],
        "scan_content_dir": ["scan", "refresh"],
        "exit": ["exit", "quit", "x"],
        "browse":["browse", "b"],
        "print_selected_record":["printselected", "p"],
        "play_selected_record":["play", "y"],
        "print_avail_tags": ["avail", "tags", "at"],
        "print_avail_actors": ["availa", "aa"]
    }
    
    if args:
        args = args[0]
        while "" in args:
            args.remove("")
    
    if command_type == "":
        return
    
    elif command_type in command_types["help"]:
        print("COMMANDS ARE AS FOLLOWS:")
        for k in command_types.keys():
            print(k + ": " + str(command_types[k]))
    
    elif command_type in command_types["get_tags"]:
        try:
            fail_msg = "Could not get tags for selected record"
            verify_record_selected()
            ps = ""
            for r in get_tags():
                ps += r + ", "
            ps = ps[:-2]
            print("Tags are: %s" % ps)
        except DoNotProceedException:
            print(fail_msg)
            
    elif command_type in command_types["get_actors"]:
        try:
            fail_msg = "Could not get actors for selected record."
            verify_record_selected()
            s = ""
            for r in get_actors():
                s += r + ", "
            s = s[:-2]
            print s
            print("Actors are: %s" % s)
        except DoNotProceedException:
            print(fail_msg)

    elif command_type in command_types["add_tags"]:
        fail_msg = "Cannot add tag(s). "
        try:
            verify_args(args, int)
            verify_record_selected()
            add_tags(list(args))
        except DoNotProceedException:
            print(fail_msg)
        
        
    elif command_type in command_types["remove_tags"]:
        fail_msg = "Cannot remove tag(s). "
        try:
            verify_args(args)
            verify_record_selected()
            remove_tags(list(args))
        except DoNotProceedException:
            print(fail_msg)
    
    elif command_type in command_types["add_actor"]:
        fail_msg = "Cannot add actor(s). "
        try:
            verify_args(args, int)
            verify_record_selected()
            add_actor(args[0])
        except DoNotProceedException:
            print(fail_msg)
        
        
    elif command_type in command_types["remove_actor"]:
        fail_msg = "Cannot remove actor(s). "
        try:
            verify_args(args)
            verify_record_selected()
            remove_actor(args[0])
        except DoNotProceedException:
            print(fail_msg)
    
    elif command_type in command_types["select_record_by_name"]:
        fail_msg = "Cannot select record by name."
        try:
            verify_args(args)
            select_record_by_name(args[0])
        except DoNotProceedException:
            print(fail_msg)
            
    elif command_type in command_types["select_random_record"]:
        select_random_record()
        
    elif command_type in command_types["search_records_by_tags"]:
        fail_msg = "Cannot search by tags."
        try:
            verify_args(args)
            search_records_by_tags(list(args))
            print_search_results()
        except DoNotProceedException:
            print(fail_msg)
    
    elif command_type in command_types["filter_records_by_tags"]:
        fail_msg = "Cannot filter by tags."
        try:
            verify_args(args)
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

    elif command_type in command_types["create_tag"]:
        fail_msg = "Cannot create tag."
        try:
            verify_args(args)
            tag = args[0].lower()
            if tag not in g_engine.get_avail_tags():
                create_new_tag(tag)
        except DoNotProceedException:
            print(fail_msg)
            
    elif command_type in command_types["create_actor"]:
        fail_msg = "Cannot create actor."
        try:
            verify_args(args)
            actor = " ".join(n for n in args)
            actor = actor.lower()
            if actor not in g_engine.get_avail_actors():
                create_new_actor(actor)
        except DoNotProceedException:
            print(fail_msg)
            
         
    elif command_type in command_types["discard"]:
        inp = raw_input("Are you sure you want to reload settings from disk and discard all changes?" + YN)
        if inp in g_yes_choices:
            inp = raw_input("Are you absolutely positive? All changes will be lost." + YN)
            if inp in g_yes_choices:
                print("Reloading all data from disk...")
                g_engine.load_settings()
                print("Changes reset.")
                
    elif command_type in command_types["scan_content_dir"]:
        print("Scanning content directory for new files... ")
        print("Before: %d records" % get_record_count())
        g_engine.add_content_to_records()
        print("After: %d records" % get_record_count())
    
    elif command_type in command_types["browse"]:
        get_all_records()
        print_search_results()
        
    elif command_type in command_types["exit"]:
        inp = ""
        while inp == "":
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
            g_engine.start_file(g_selected_record["name"])
        except DoNotProceedException:
            print(fail_msg)
    
    elif command_type in command_types["print_avail_tags"]:
        print("AVAIL TAGS ARE:")
        g_engine.print_avail_tags()
        
    elif command_type in command_types["print_avail_actors"]:
        print("AVAIL ACTORS ARE:")
        g_engine.print_avail_actors()
        
    else:
        print("Unrecognized command type \"%s\"" % command_type)
    

        
def intro():
    global g_engine
    print("Welcome to the interactive Video Tagging Tool.")
    print("Copyright 2014-2016 Paul Bellamy")
    print("Loading VTT Engine...")
    g_engine = ShowTagger()
    print("You settings are the following:")
    print("Content Directory: %s" % g_engine.CONTENT_DIRECTORY)
    print("Records Path: %s" % g_engine.RECORDS_PATH)
    print("Available items path: %s" % g_engine.AVAIL_ITEMS_PATH)
    inp = ""
    while inp == "":
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
    