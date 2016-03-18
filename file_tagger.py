import os
import sporklib
import json
import ast
from abc import abstractmethod

class FileTagger(object):

    CWD = sporklib.normalize_path(os.getcwd())
    
    DEFAULT_RECORD_TEMPLATE = {"name":"", "ext":""}
    DEFAULT_SETTINGS_PATH = CWD + "/settings.json"
    DEFAULT_CONTENT_DIRECTORY = CWD + "/content"
    DEFAULT_AVAIL_ITEMS_PATH = CWD + "/items.json"
    DEFAULT_RECORDS_PATH = CWD + "/records.json"

    RECORD_TEMPLATE = DEFAULT_RECORD_TEMPLATE
    SETTINGS_PATH = DEFAULT_SETTINGS_PATH
    CONTENT_DIRECTORY = DEFAULT_CONTENT_DIRECTORY
    AVAIL_ITEMS_PATH = DEFAULT_AVAIL_ITEMS_PATH
    RECORDS_PATH = DEFAULT_RECORDS_PATH
    
    RECORDS = {}
    AVAIL_ITEMS = {}
    
    def __init__(self):
        #pdb.set_trace()
        self.load_settings()
        self.load_custom_settings()
        self.load_records()
        self._vet_recorded_items_to_avail()
        self._load_avail_items()
        print("INSTANCE") #DEBUG
    
    '''
    init and admin
    '''
    
    def save_changes(self):
        data_dict = {}
        if self.SETTINGS_PATH != self.DEFAULT_SETTINGS_PATH:
            data_dict["settingsPath"] = self.SETTINGS_PATH

        if self.CONTENT_DIRECTORY != self.DEFAULT_CONTENT_DIRECTORY:
            data_dict["contentDirectory"] = self.CONTENT_DIRECTORY
            
        if self.RECORD_TEMPLATE != self.DEFAULT_RECORD_TEMPLATE:
            data_dict["recordSchema"] = self.RECORD_TEMPLATE

        if self.AVAIL_ITEMS_PATH != self.DEFAULT_AVAIL_ITEMS_PATH:
            data_dict["availItemsPath"] = self.AVAIL_ITEMS_PATH

        if self.RECORDS_PATH != self.DEFAULT_RECORDS_PATH:
            data_dict["recordsPath"] = self.RECORDS_PATH

        with open(self.SETTINGS_PATH, "w") as f:
            json.dump(data_dict, f, ensure_ascii=True)

        with open(self.RECORDS_PATH, "w") as f:
            json.dump(self.get_records(), f, ensure_ascii=True)

        with open(self.AVAIL_ITEMS_PATH, "w") as f:
            json.dump(self.AVAIL_ITEMS, f, ensure_ascii=True)
    
    def _load_avail_items(self, data_path=None):
        data_path = data_path or self.DEFAULT_AVAIL_ITEMS_PATH
        avail_items = {}
        if os.path.isfile(data_path):
            with open(data_path) as f:
                self.AVAIL_ITEMS = sporklib.byteify(json.loads(f.read(), "ascii"))
        else:
            raise IOError("Did not find items data file at: %s" % data_file)
    
    def _load_setting(self, setting, data):
        try:
            return data[setting]
        except KeyError:
            return None
                
    def load_settings(self, data_path=None):
        data_path = data_path or self.SETTINGS_PATH
        if os.path.isfile(data_path):
            f = open(data_path, "r")
            data = sporklib.byteify(json.loads(f.read(), "ascii"))
            try:
                self.load_custom_settings_path(sporklib.normalize_path(data["settingsPath"]))
                self.load_settings()
                return None #end loop here
            except (IOError,KeyError):
                pass
            try:
                self.RECORD_TEMPLATE = data["recordSchema"]
            except KeyError:
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
                self.AVAIL_ITEMS_PATH = data["availItemsPath"]
            except KeyError:
                pass
        #you finished working here, you need to institute an abstract load_settings method that _load_settings will take
                
    def load_records(self, data_path=None):
        data_path = data_path or self.DEFAULT_RECORDS_PATH
        if os.path.isfile(data_path):
            with open(data_path, "r") as f:
                data = sporklib.byteify(json.loads(f.read(), "ascii"))
            self.RECORDS = data
        else:
            raise IOError("Did not find records file at: %s" % data_path)
    
    @abstractmethod
    def load_custom_settings(self, data_path=None):
        '''
        Abstract method.
        '''
        return
    
    def create_new_record(self, name, ext):
        records = self.get_records()
        new_record = self.get_record_template()
        new_record["name"] = name
        new_record["ext"] = ext
        return new_record
    
    def add_content_to_records(self, data_path=None):
        data_path = data_path or self.CONTENT_DIRECTORY
        content_files = sporklib.list_files(data_path, True, False)
        record_keys = self.get_records().keys()
        for file in content_files:
            fn = os.path.basename(file).split(".")
            name = fn[0]
            ext = fn[1]
            if name not in record_keys:
                self.RECORDS[name] = self.create_new_record(name, ext)
    
    
    def _vet_recorded_items_to_avail(self, records=None, avail_items=None, add_items=False):
        for item_key in self.AVAIL_ITEMS.keys():
            avails = self.get_avail_items(item_key)
            records = records or self.RECORDS
            avail_items = avail_items or avails
            avail_items = set(avail_items)
            for key in records.keys():
                new_items = set(records[key][item_key]) - avail_items
                if len(new_items) > 0:
                    for item in list(new_items):
                        if add_items:
                            self._add_item_to_avail(item)
                        else:
                            self._remove_item_from_record(item_key, item, records[key])

    def get_avail_items(self, item_key):
        return self.AVAIL_ITEMS[item_key]

    @abstractmethod
    def _validate_record(self, item_key, record):
        avails = self.get_avail_items(item_key)
        avail_items = self.get_avail_items(item_key)
        if record.keys() != avail_items.keys():
            avails = self.get_avail_items(item_key)
            return False
        if type(record["name"]).name != "str":
            return False
        if type(record["ext"]).name != "str":
            return False
        return True


    def _strip_unavail_items(self, item_key, items):
        avails = self.get_avail_items(item_key)
        stripped_items = []
        for item in items:
            if self.get_is_item_avail(item_key, item):
                stripped_items.append(item)
        return stripped_items
        
    def _print_avail_items(self, item_key, title=""):
        sporklib.print_list_of_items(self.get_avail_items(item_key), title)


    def load_custom_settings_path(new_settings_path):
        self.SETTINGS_PATH = new_settings_path
    
    '''
    Working with items
    '''
    def _get_is_item_avail(self, item_key, item):
        if item in self.AVAIL_ITEMS[item_key]:
            return True
        return False

    def get_record_file_path(self, record):
        return sporklib.normalize_path(self.CONTENT_DIRECTORY + "/" + record["name"] + "." + record["ext"])
        
    def _get_item_index(self, item_key, item):
        avails = self.get_avail_items(item_key)
        i = 0
        avail_items = self.get_avail_items(item_key)

        for t in avail_items:
            if item == t:
                return i
            else:
                i += 1
        return -1

    def _select_item_by_index(self, item_key, i):
        avail_items = self.get_avail_items(item_key)
        return avail_items[i]

    def _add_item_to_avail(self, item_key, item):
        if not self._get_is_item_avail(item_key, item):
            items = list(self.get_avail_items(item_key))
            items.append(item)
            self.AVAIL_ITEMS[item_key] = tuple(items)

    def _add_item_to_record(self, record, item_key, item):
        records = self.get_records()
        if self._get_is_item_avail(item_key, item):
            if record["name"] in records:
                if item not in record[item_key]:
                    records[record["name"]][item_key].append(item)

    def _remove_item_from_record(self, record, item_key, item):
        records = self.get_records()
        if self._get_is_item_avail(item_key, item):
            if record in records:
                old_set = set(records[record][item_ley])
                new_set = old_set - set(item)
                records[record][item_key] = list(new_set)
    
    '''
    Working with records
    '''
    #Takes a dict of records and returns those that DON'T include item_list
    def _filter_by_items(self, item_key, items, records=None):
        records = records or self.get_records()
        item_set = set(items)
        matches = {}
        for record in records:
            records_item_set = set(records[record][item_key])
            len_records_item_set = len(records_item_set)
            if len(records_item_set - item_set) == len_records_item_set:
                matches[record] = records[record]
        return matches

    #Takes a dict of records that match all items in a list exactly
    def _get_item_matches(self, item_key, items, records=None):
        records = records or self.get_records()
        item_set = set(items)
        matches = {}
        for record in records:
            if len(item_set - set(records[record][item_key])) == 0:
                matches[record] = records[record]
        return matches
    
    
    def get_record_path(self, name):
        return self.CONTENT_DIRECTORY + "/" + name + "." + self.get_records()[name]["ext"]

    def start_file(self, name):
        path = self.get_record_path(name)
        os.startfile(path)
    
    def get_records(self):
        return self.RECORDS
    
    def get_record_template(self):
        return dict(self.RECORD_TEMPLATE)
