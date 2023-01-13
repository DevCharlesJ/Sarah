#!/usr/bin/python3
import os
DATABASE = 'DATABASE.JSON'

if __name__ == '__main__':
    import COMMUNICATION
else:
    from . import COMMUNICATION

import json

def extract(collection, isdict=False):
    a = list()
    if isdict:
        for _ in collection.values():
            if isinstance(_, (int, str)):
                a.append(_)
            elif isinstance(_, (list, tuple, set, dict)):
                a = a + extract(_, isinstance(_, dict))
    else:
        for _ in collection:
            if isinstance(_, (int, str)):
                a.append(_)
            if isinstance(_, (list, tuple, set, dict)):
                a = a + extract(_, isinstance(_, dict))
    return a

class DATA:
    @staticmethod
    def convert_topath(collection):
        return collection.split('.')

    @staticmethod
    def get(request=None,all=False):
        with open(DATABASE,"r") as database:
            data = json.load(database)
            if request is None:
                return data
            elif all:
                return extract(data,True)
            else:
                try:
                    path = DATA.convert_topath(request)

                    path_cpy = path.copy()
                    requested_data = data
                    while len(path_cpy) > 0:
                        requested_data = requested_data[path_cpy.pop(0)]

                    return requested_data
                except:
                    return None

    @staticmethod
    def create_directory(p=None,dir_name=None,l_data=None):
        if dir_name is None:
            COMMUNICATION.FORMAT.to_error(f'Name not given',True)
            return
        fresh = {f'{dir_name}': l_data or dict()}
        with open(DATABASE,'r') as r_database:
            data = json.load(r_database)
            if p is not None:
                path = DATA.convert_topath(p)
                path_cpy = path.copy()
                area = data
                while len(path_cpy) > 1:
                    area = area[path_cpy[0]]
                    path_cpy.pop(0)

                section = path_cpy[0]

                if area.get(section, False) == False: # result could be None
                    print(f'{section} not found')
                    return

                if isinstance(area[section],dict):
                    area[section].update({dir_name: l_data or dict()})
                else:
                    COMMUNICATION.FORMAT.to_error(f'{dir_name} could not be created',True)
                    return
            else:
                data.update(fresh)
            with open(DATABASE,"w") as w_database:
                json.dump(data,w_database,indent=4)

    @staticmethod
    def add_data(p,new_data=None):
        if new_data is not None:
            with open(DATABASE,"r") as r_database:
                data = json.load(r_database)

                path = DATA.convert_topath(p)
                path_cpy = path.copy()
                area = data
                while len(path_cpy) > 1:
                    area = area[path_cpy[0]]
                    path_cpy.pop(0)

                section = path_cpy[0]

                if area.get(section, False) == False: # result could be None
                    print(f'{section} not found')
                    return

                if isinstance(area[section],list):
                    area[section].append(new_data)
                elif isinstance(area[section],dict):
                    area[section].update(new_data)
                else:
                    area[section] = [area[section],new_data]
                with open(DATABASE, 'w') as w_database:
                    json.dump(data, w_database, indent=4)

        else:
            return f'No data given!'

    @staticmethod
    def remove_data(p,specific_data=None):
        with open(DATABASE,'r') as r_database:
            data = json.load(r_database)

            path = DATA.convert_topath(p)
            path_cpy = path.copy()
            global area
            area = data
            while len(path_cpy) > 1:
                area = area[path_cpy[0]]
                path_cpy.pop(0)

            section = path_cpy[-1]


            if area.get(section, False) == False: # result could be None
                return f'{section} not found'

            if area[section] is None:
                return f'No Data in {section}'

            if specific_data and isinstance(area.get(section,None), list):
                try:
                    area[section].remove(specific_data)
                    if len(area[section]) == 0:
                        area[section] = None
                except:
                    return f'{specific_data} not found in {section}'

            elif specific_data and  isinstance(area.get(section,None), dict):
                try:
                    area[section].pop(specific_data)
                    if len(area[section]) == 0:
                        area[section] = None
                except:
                    return f'{specific_data} not found in {section}'
            else:
                try:
                    area.pop(section)
                except:
                    return f'{section} not found'

            with open(DATABASE,'w') as w_database:
                json.dump(data,w_database,indent=4)


    @staticmethod
    def edit_directory(p,name=None,clear=False,new_value=None):
        if name is not None:
            pass
        if new_value is not None:
            with open(DATABASE, 'r') as r_database:
                data = json.load(r_database)

                path = DATA.convert_topath(p)
                path_cpy = path.copy()
                global area
                area = data
                while len(path_cpy) > 1:
                    area = area[path_cpy[0]]
                    path_cpy.pop(0)

                section = path_cpy[0]

                if area.get(section, False) == False: # result could be None
                    print(f'{section} not found')
                    return

                area[section] = new_value
                with open(DATABASE,'w') as w_database:
                    json.dump(data,w_database,indent=4)

        elif clear:
            # TODO
            pass