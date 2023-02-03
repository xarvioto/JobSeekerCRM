import datetime

current_user_id = 1
current_date_string = datetime.datetime.now().date().strftime('%Y-%m-%d')


default_vacancy_dict = {'id': None,
     'creation_date': current_date_string,
     'status': 1,
     'company': 'default company',
     'contacts_ids': [],
     'description': 'default description',
     'position_name': 'default position name',
     'comment': 'default comment',
     'user_id': current_user_id
     }

default_event_dict = {'id': None,
     'vacancy_id': None,
     'description': 'default event',
     'event_date': current_date_string,
     'title': 'default event title',
     'due_to_date': None,
     'status': 1
     }

vacancies_database_dict = [
    {'id': 1,
     'creation_date': current_date_string,
     'status': 1,
     'company': 'Company 1',
     'contacts_ids': [1, 2],
     'description': 'vacancy description 1',
     'position_name': 'Python Jr. 1',
     'comment': 'Comment 1',
     'user_id': 1
     },
    {'id': 2,
     'creation_date': current_date_string,
     'status': 1,
     'company': 'Company 1',
     'contacts_ids': [2, 3],
     'description': 'vacancy description 2',
     'position_name': 'Python Jr. 2',
     'comment': 'Comment 2',
     'user_id': 1
     },
    {'id': 3,
     'creation_date': current_date_string,
     'status': 1,
     'company': 'Company 2',
     'contacts_ids': [4],
     'description': 'vacancy description 3',
     'position_name': 'Python Jr. 3',
     'comment': 'Comment 3',
     'user_id': 2
     },
    {'id': 4,
     'creation_date': current_date_string,
     'status': 1,
     'company': 'Company 2',
     'contacts_ids': [4, 5],
     'description': 'vacancy description 4',
     'position_name': 'Python Jr. 4',
     'comment': 'Comment 4',
     'user_id': 2
     },
]


events_database_dict = [
    {'id': 1,
     'vacancy_id': 1,
     'description': 'event description 1',
     'event_date': current_date_string,
     'title': 'event title 1',
     'due_to_date': current_date_string,
     'status': 1
     },
    {'id': 2,
     'vacancy_id': 1,
     'description': 'event description 2',
     'event_date': current_date_string,
     'title': 'event title 2',
     'due_to_date': current_date_string,
     'status': 1
     },
    {'id': 3,
     'vacancy_id': 2,
     'description': 'event description 3',
     'event_date': current_date_string,
     'title': 'event title 3',
     'due_to_date': current_date_string,
     'status': 1
     },
    {'id': 4,
     'vacancy_id': 3,
     'description': 'event description 3',
     'event_date': current_date_string,
     'title': 'event title 3',
     'due_to_date': current_date_string,
     'status': 1
     },
]


class DataBaseDummy:
    last_used_id: int
    database: [{}]
    default_keys_and_values: {}

    def __init__(self, list_of_dicts: [{}], default_keys_and_values: {} = {}):
        self.database = list_of_dicts
        self.default_keys_and_values = default_keys_and_values

        self.last_used_id = max(element.get('id', 0) for element in self.database)

    @property
    def next_id(self):
        return self.last_used_id + 1

    def get_entry_by_id(self, entry_id):
        for dict_entry in self.database:
            if dict_entry.get('id', None) == entry_id:
                return dict_entry
        return None

    def filter_by_key_and_value(self, parameter_name, parameter_value):
        filtered_entries = []
        for dict_entry in self.database:
            if dict_entry.get(parameter_name, None) == parameter_value:
                filtered_entries.append(dict_entry)
        return filtered_entries

    def filter_by_kwargs(self, **kwargs):
        filtered_entries = []
        for dict_entry in self.database:
            for key, value in kwargs.items():
                if dict_entry.get(key, None) != value:
                    break
            else:
                filtered_entries.append(dict_entry)
        return filtered_entries

    def add_entry(self, **kwargs):
        new_dict_entry = self.default_keys_and_values.copy()
        for key, value in kwargs.items():
            if key in new_dict_entry.keys():
                new_dict_entry.update({key: value})

        new_dict_entry.update({'id': self.next_id})

        self.database.append(new_dict_entry)
        self.last_used_id = self.next_id

        return new_dict_entry

    def update_entry(self, entry_id, **kwargs):
        updated_dict_entry = self.get_entry_by_id(entry_id)

        for key, value in kwargs.items():
            if key == 'id':
                continue

            # updates only keys, that are already present in entry -> Does not create new keys in entry
            if key in updated_dict_entry.keys():
                updated_dict_entry.update({key: value})

        return updated_dict_entry

    def _delete_entry(self, entry_id):
        entry_to_delete = self.get_entry_by_id(entry_id)
        print(entry_to_delete)

        if entry_to_delete:
            self.database.remove(entry_to_delete)
            return f'entry_id:{entry_id} deleted successfully'
        else:
            print(f'Cannot delete, entry_id:{entry_id} not found')

    def __getitem__(self, entry_id: int):
        item_to_get = self.get_entry_by_id(entry_id)

        if item_to_get:
            return item_to_get
        else:
            return print(f'Database contains no entry with id:{entry_id})')

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __str__(self):
        return str(self.database)


vacancies_database = DataBaseDummy(vacancies_database_dict, default_vacancy_dict)

events_database = DataBaseDummy(events_database_dict, default_event_dict)