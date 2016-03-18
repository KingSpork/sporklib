import os
import sporklib
import pdb
from file_tagger import FileTagger

class ShowTagger(FileTagger):

    #RECORD_TEMPLATE = {"name":"", "tags":[], "actors":[], "notes":"", "favorite":False, "ext":""}

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


    def _validate_record(self, record):
        if not super()._validate_record(record):
            return False
        if type(record["items"]).name != "list":
            return False
        if type(record["actors"]).name != "list":
            return False
        if type(record["notes"]).name != "str":
            return False
        if type(record["favorite"]).name != "bool":
            return False
        return True
            
    def add_tag_to_avail(self, tag):
        self._add_item_to_avail("tags", tag)
        
    def add_actor_to_avail(self, actor):
        self._add_item_to_avail("actors", actor)



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
        return self.get_avail_items("tags")
        
    def get_avail_actors(self):
        return self.get_avail_items("actors")

    def strip_unavail_tags(self, tags):
        stripped_tags = []
        for tag in tags:
            if self.get_is_tag_avail(tag):
                stripped_tags.append(tag)
        return stripped_tags


    def print_avail_tags(self):
        self._print_avail_items("tags", "TAG: ")
        
    def print_avail_actors(self):
        self._print_avail_items("actors", "ACTOR: ")

    #Takes a dict of records and returns those that DON'T include tag_list
    def filter_by_tags(self, tags):
        return self._filter_by_items("tags", tags)

    #Takes a dict of records that match all tags in a list exactly
    def get_tag_matches(self, tags):
        return self._get_item_matches("tags", tags)
        
    #Takes a dict of records and returns those that DON'T include tag_list
    def filter_by_tags(self, actors):
        return self._filter_by_items("actors", actors)

    #Takes a dict of records that match all tags in a list exactly
    def get_actor_matches(self, actors):
        return self._get_item_matches("actors", actors)

  
    def select_tag_by_index(self, i):
        return self._select_item_by_index("tags", i)
        
    def select_actor_by_index(self, i):
        return self._select_actor_by_index("actors", i)


    def add_tag_to_record(self, record, tag):
        self._add_item_to_record(record, "tags", tag)

    def remove_tag_from_record(self, record, tag):
        self._remove_item_from_record(record, "tags", tag)
        
    def add_actor_to_record(self, record, actor):
        self._add_item_to_record(record, "actors", actor)

    def remove_tag_from_record(self, record, actor):
        self._remove_item_from_record(record, "actors", actor)

    # you need to rework this method, maybe override an abstractr method from base class
    def create_new_record(self, name, ext, tags=None, actors=None, favorite=None, notes=None):
        tags = tags or self.RECORD_TEMPLATE["tags"]
        actors = actors or self.RECORD_TEMPLATE["actors"]
        favorite = favorite or self.RECORD_TEMPLATE["favorite"]
        notes = notes or self.RECORD_TEMPLATE["notes"]
        
        new_record = super(ShowTagger, self).create_new_record(name, ext)
        
        new_record["tags"] = tags
        new_record["actors"] = actors
        new_record["favorite"] = favorite
        new_record["notes"] = notes
        return new_record