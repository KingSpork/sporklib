import os
import sporklib
import json
import pdb

class FileTagger(object):

    #prn record structure:
    #{"name":"", "tags":[], "actors":[], "notes":"", "favorite":False}

    record_template = {"name":"", "tags":[], "actors":[], "notes":"", "favorite":False, "ext":""}

    '''
    AVAIL_TAGS = ("anal",
                    "ass-to-mouth",
                    "cum drink",
                    "rough",
                    "gangbang",
                    "fucking",
                    "lesbian",
                    "cum sharing",
                    "anal cum",
                    "dp"
                    )
                    
                    
     [
        "anal",
        "ass-to-mouth",
        "cum drink",
        "rough",
        "gangbang",
        "fucking",
        "lesbian",
        "cum sharing",
        "anal cum",
        "dp"
    ]
    '''

    CWD = sporklib.normalize_path(os.getcwd())
    
    DEFAULT_SETTINGS_PATH = CWD + "/settings.json"
    DEFAULT_CONTENT_DIRECTORY = CWD + "/content"
    DEFAULT_AVAIL_TAGS_PATH = CWD + "/tags.json"
    DEFAULT_RECORDS_PATH = CWD + "/records.json"

    SETTINGS_PATH = DEFAULT_SETTINGS_PATH
    CONTENT_DIRECTORY = DEFAULT_CONTENT_DIRECTORY
    AVAIL_TAGS_PATH = DEFAULT_AVAIL_TAGS_PATH
    RECORDS_PATH = DEFAULT_RECORDS_PATH
    
    
    
    AVAIL_ACTORS = ()
    AVAIL_TAGS = ()
    RECORDS = {}
    
    AVAILS_DICT = {"actors":AVAIL_ACTORS, "tags":AVAIL_TAGS}

    def __init__(self):
        #pdb.set_trace()
        self.load_settings()
        self.load_records()
        #pdb.set_trace()
        self.load_avail_tags()
        print("INSTANCE") #DEBUG
        
    def load_avail_tags(self, data_path=None):
        data_path = data_path or self.DEFAULT_AVAIL_TAGS_PATH
        if os.path.isfile(data_path):
            with open(data_path) as f:
                data = json.loads(f.read(), "ascii")
            self.AVAIL_TAGS = tuple(data["tags"])
            self.AVAIL_ACTORS = tuple(data["actors"])
        else:
            raise IOError("Did not find tags file at: %s" % data_file)

    def load_settings(self, data_path=None):
        data_path = data_path or self.SETTINGS_PATH
        if os.path.isfile(data_path):
            f = open(data_path, "r")
            data = json.loads(f.read(), "ascii")
            try:
                self.SETTINGS_PATH = sporklib.normalize_path(data["settingsPath"])
                self.load_settings(self.SETTINGS_PATH)
                return None #end loop here
            except (IOError,KeyError):
                pass
            try:
                self.CONTENT_DIRECTORY = sporklib.normalize_path(data["contentDirectory"])

            except KeyError:
                pass
            try:
                self.RECORDS_PATH = data["recordsPath"]
            except KeyError:
                pass
            try:
                self.AVAIL_TAGS_PATH = data["availTagsPath"]
            except KeyError:
                pass
                
            f.close()
        if not os.path.isfile(self.RECORDS_PATH):
            with open(self.RECORDS_PATH, "w") as f:
                f.writelines("{}")
        if not os.path.isfile(self.AVAIL_TAGS_PATH):
            with open(self.CONTENT_DIRECTORY, "w") as f:
                f.writelines("[]")

    def load_custom_settings_path(new_settings_path):
        self.SETTINGS_PATH = new_settings_path
        self.load_settings()



    def save_changes(self):
        data_dict = {}
        if self.SETTINGS_PATH != self.DEFAULT_SETTINGS_PATH:
            data_dict["settingsPath"] = self.SETTINGS_PATH

        if self.CONTENT_DIRECTORY != self.DEFAULT_CONTENT_DIRECTORY:
            data_dict["contentDirectory"] = self.CONTENT_DIRECTORY

        if self.AVAIL_TAGS_PATH != self.DEFAULT_AVAIL_TAGS_PATH:
            data_dict["availTagsPath"] = self.AVAIL_TAGS_PATH

        if self.RECORDS_PATH != self.DEFAULT_RECORDS_PATH:
            data_dict["recordsPath"] = self.RECORDS_PATH

        with open(self.SETTINGS_PATH, "w") as f:
            json.dump(data_dict, f)

        with open(self.RECORDS_PATH, "w") as f:
            json.dump(self.get_records(), f)

        with open(self.AVAIL_TAGS_PATH, "w") as f:
            json.dump(self.get_avail_tags(), f)



    def add_content_to_records(self, data_path=None):
        data_path = data_path or self.CONTENT_DIRECTORY
        content_files = sporklib.list_files(data_path, True, False)
        record_keys = self.get_records().keys()
        for file in content_files:
            fn = os.path.basename(file).split(".")
            name = fn[0]
            ext = fn[1]
            #print("name: %s" + name); raw_input()
            #pdb.set_trace()
            if name not in record_keys:
                new_record = self.get_record_template()
                new_record["name"] = name
                new_record["ext"] = ext
                #print("new_record: %s" % new_record);raw_input()
                #print("records: %s" % self.RECORDS);raw_input()
                self.RECORDS[name] = new_record
                #print("STOPPING")
                #pdb.set_trace()
        #pdb.set_trace()
        
    def load_records(self, data_path=None):
        data_path = data_path or self.DEFAULT_RECORDS_PATH
        if os.path.isfile(data_path):
            with open(data_path, "r") as f:
                data = json.loads(f.read(), "ascii")
            self.RECORDS = data
        else:
            raise IOError("Did not find records file at: %s" % data_path)

    def get_record_file_path(self, record):
        return sporklib.normalize_path(self.CONTENT_DIRECTORY + "/" + record["name"] + "." + record["ext"])
            
            
    def play_record_file(self, record):
        path = self.get_record_file_path(record)
        os.startfile(path)
        
    def _add_item_to_avail(self, item, item_key, dict):
        if item_key = "tag":
            avails = self.AVAIL_TAGS
        if item_key = "actor":
            avails = self.AVAIL_ACTORS
        items = list(avails)
        items.append(item)
        avails = tuple(items)
        
    def add_tag_to_avail(self, tag, avail_tags=None):
        avail_tags = avail_tags or self.AVAIL_TAGS
        self._add_item_to_avail(tag, "tag", avail_tags)
        
    def add_actor_to_avail(self, actor, avail_actors=None):
        avail_actors = avail_actors or self.AVAIL_ACTORS
        self._add_item_to_avail(actor, "actor", avail_actors)
        
    def vet_recorded_tags_to_avail(self, records=None, avail_tags=None, add_tags=False):
        records = records or self.RECORDS
        avail_tags = avail_tags or self.AVAIL_TAGS
        for key in records.keys():
            new_tags = set(records[key]["tags"]) - set(self.get_avail_tags)
            if len(new_tags) > 0:
                for tag in list(new_tags):
                    if add_tags:
                        self.add_tag_to_avail(tag)
                    else:
                        self.remove_tag_from_record(tag, records[key])

    def get_full_path(self, name):
        return self.CONTENT_DIRECTORY + "/" + name

    def start_file(self, name):
        path = get_full_path(name)
        os.startfile(path)

    def write_records(self, data_path=None):
        data_path = data_path or self.DEFAULT_RECORDS_PATH
        with open(data_path, "w") as f:
            json.dump(self.RECORDS, f)


    def validate_record(self, record):
        avail_tags = self.get_avail_tags()
        if record.keys() != avail_tags.keys():
            return False
        if type(record["name"]).name != "str":
            return False
        if type(record["tags"]).name != "list":
            return False
        if type(record["actors"]).name != "list":
            return False
        if type(record["notes"]).name != "str":
            return False
        if type(record["favorite"]).name != "bool":
            return False
        return True


    def get_record_template(self):
        return dict(self.record_template)


    def get_records(self):
        return self.RECORDS


    def get_is_tag_avail(self, tag):
        if tag in self.get_avail_tags():
            return True
        return False

    def add_record(self, record):
        if record not in self.RECORDS.keys():
            self.RECORDS[record["name"]] = record
            return True
        else:
            return False


    def get_avail_tags(self):
        return self._get_avail_items("tags")
        
    def get_avail_actors(self):
        return self._get_avail_items("actors")

    def strip_unavail_tags(self, tags):
        stripped_tags = []
        for tag in tags:
            if self.get_is_tag_avail(tag):
                stripped_tags.append(tag)
        return stripped_tags


    def print_avail_tags(self):
        sporklib.print_list_of_items(self.get_avail_tags(), "TAG: ")

    #Takes a dict of records and returns those that DON'T include tag_list
    def filter_by_tags(self, tag_list, records=None):
        records = records or self.get_records()
        tag_set = set(tag_list)
        matches = {}
        for record in records:
            records_tag_set = set(records[record][tags])
            len_records_tag_set = len(records_tag_set)
            if len(records_tag_set - tag_set) == len_records_tag_set:
                matches[record] = records[record]

        return matches

    #Takes a dict of records that match all tags in a list exactly
    def get_tag_matches(self, tag_list, records=None):
        records = records or self.get_records()
        tag_set = set(tag_list)
        matches = {}
        for record in records:
            if len(tag_set - set(records[record][tags])) == 0:
                matches[record] = records[record]

        return matches


    def get_tag_index(self, tag):
        i = 0
        avail_tags = self.get_avail_tags()

        for t in avail_tags:
            if tag == t:
                return i
            else:
                i += 1
        return -1


    def select_tag_by_index(self, i):
        avail_tags = self.get_avail_tags()
        return avail_tags[i]


    def add_tag_to_record(self, tag, record):
        records = self.get_records()
        if self.get_is_tag_avail(tag):
            if record in records:
                records[record][tags].append(tag)

    def remove_tag_from_record(self, tag, record):
        records = self.get_records()
        if self._get_is_tag_avail(tag):
            if record in records:
                old_set = set(records[record][tags])
                new_set = old_set - set(tag)
                records[record][tags] = list(new_set)

    def create_new_record(self, name, tags, actors, favorite=False, notes=""):
        records = self.get_records()
        new_record = self.get_record_template()
        new_record["name"] = name
        new_record["tags"] = self.strip_unavail_tags(tags)
        new_record["actors"] = actors
        return record
