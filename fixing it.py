
        
    def _vet_recorded_items_to_avail(self, item_key, records=None, avail_items=None, add_items=False):
        avails = self.get_avail_items(item_key)
        records = records or self.RECORDS
        avail_items = avail_items or avails
        for key in records.keys():
        avails = self.get_avail_items(item_key)
            new_items = set(records[key][item_key]) - set(self.get_avail_items)
            if len(new_items) > 0:
                for item in list(new_items):
                    if add_items:
                        self._add_item_to_avail(item)
                    else:
                        self._remove_item_from_record(item, records[key])

    def _get_avail_items(self, item_key):
        return self.AVAILS_DICT[item_key]

    def _validate_record(self, item_key, record):
        avails = self.get_avail_items(item_key)
        avail_items = self._get_avail_items(item_key)
        if record.keys() != avail_items.keys():
        avails = self.get_avail_items(item_key)
            return False
        if type(record["name"]).name != "str":
            return False
        if type(record["items"]).name != "list":
            return False
        if type(record["actors"]).name != "list":
            return False
        if type(record["notes"]).name != "str":
            return False
        if type(record["ext"]).name != "str":
            return False
        if type(record["favorite"]).name != "bool":
            return False
        return True




    def _get_is_item_avail(self, item_key, item):
        if item in self.AVAILS_DICT[item_key]:
            return True
        return False


    def _get_avail_items(self):
        avails = self.get_avail_items(item_key)
        return avails

    def _strip_unavail_items(self, item_key, items):
        avails = self.get_avail_items(item_key)
        stripped_items = []
        for item in items:
            if self.get_is_item_avail(item_key, item):
                stripped_items.append(item)
        return stripped_items


    def _print_avail_items(self, item_key, title=""):
        sporklib.print_list_of_items(self._get_avail_items(item_key), title)

    #Takes a dict of records and returns those that DON'T include item_list
    def _filter_by_items(self, item_key, item_list, records=None):
        avails = self.get_avail_items(item_key)
        records = records or self.get_records()
        item_set = set(item_list)
        matches = {}
        for record in records:
            records_item_set = set(records[record][items])
            len_records_item_set = len(records_item_set)
            if len(records_item_set - item_set) == len_records_item_set:
                matches[record] = records[record]

        return matches

    #Takes a dict of records that match all items in a list exactly
    def _get_item_matches(self, item_key, item_list, records=None):
        avails = self.get_avail_items(item_key)
        records = records or self.get_records()
        item_set = set(item_list)
        matches = {}
        for record in records:
            if len(item_set - set(records[record][items])) == 0:
                matches[record] = records[record]

        return matches


    def _get_item_index(self, item_key, item):
        avails = self.get_avail_items(item_key)
        i = 0
        avail_items = self._get_avail_items(item_key)

        for t in avail_items:
            if item == t:
                return i
            else:
                i += 1
        return -1


    def _select_item_by_index(self, item_key, i):
        avail_items = self.get_avail_items(item_key)
        return avail_items[i]


    def _add_item_to_record(self, item_key, item, record):
        records = self.get_records()
        if self._get_is_item_avail(item_key, item):
            if record in records:
                records[record][items].append(item)

    def _remove_item_from_record(self, item_key, item, record):
        records = self.get_records()
        if self._get_is_item_avail(item_key, item):
            if record in records:
                old_set = set(records[record][item_ley])
                new_set = old_set - set(item)
                records[record][item_key] = list(new_set)
