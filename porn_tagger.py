import os

class pornTagger(object):
    
    #prn tag structure:
    #{"name":"", "tags":{}, "whores":{}, "notes":"", "favorite":False}
    
    __record_template = {"name":"", "tags":[], "whores":[], "notes":"", "favorite":False}
    __avail_tags = ["anal",
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
    
    __default_path = "/records.json"
    
    __RECORDS = None
    __RECORDS_PATH = None
      
    def __init__(self, data_path=__default_path):
        __RECORDS = __load_tags(data_path)
        __RECORDS_PATH = __default_path
        if
      
    def __load_tags(self, data_path=self.__default_path):
        if 
        f = open(json_path, "r")
        tags = json.loads(f.read(), "ascii")
        f.close()
        return tags
    
    def get_record_template(self):
        return __record_template
    
    def get_records(self):
        return __RECORDS
    
    def get_avail_tags(self):
        return __avail_tags
    
    def print_tags(self):
        spacers = ""
        spacer_char = "."
        prefix = "TAG: "
        bracket_l = "["
        bracket_r = "]"
        
        used_chars = len(prefix + bracket_l + bracket_r)
        term_width = 80
        
        for tag in __avail_tags:
            n = term_width - (used_chars + len(tag))
            for s in xrange(0,n):
                spacers += spacer_char
            print(prefix + tag + spacers + bracket_l + bracket_r)

        
    def filter_by_tags(self, tag_list):
        tag_set = set(tag_list)
        records = self.get_records()
        matches = {}
        for record in records:
            if len(tag_set - set(records[record][tags])) == 0:
                
            
    
    @staticmethod
    def 