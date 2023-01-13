#!/usr/bin/python3
DATABASE = 'DATABASE.JSON'

if __name__ == '__main__':
    import DBManager
else:
    from . import DBManager

from datetime import datetime
from random import randint

# update time info
def updatetime(USER):
    morning,evening,afternoon,night = False,False,False,False

    dt = datetime.now()
    h, m = dt.hour, dt.minute

    # set morning, evening, afternoon, and night
    if h>= 0 and h < 5:
        night = True
    elif h >= 5 and h <= 9: # is evening
        evening = True
    elif h > 9 and h < 12: # is morning
        morning = True
    elif h >= 12 and h < 18: # is afternoon
        afternoon = True
    elif h >= 18 and h < 24: # is night
        night = True

    # then properly set database attributes
    # meridiem being a [] is uneccessary, and is only for decorative purposes
    if morning:
        DBManager.DATA.edit_directory(f'{USER}.morning', new_value='yes')
        DBManager.DATA.edit_directory(f'{USER}.meridiem',new_value='am')
        meridiem = ['am', 'in the morning']
    else:
        DBManager.DATA.edit_directory(f'{USER}.morning', new_value='no')
    if evening:
        DBManager.DATA.edit_directory(f'{USER}.evening', new_value='yes')
        DBManager.DATA.edit_directory(f'{USER}.meridiem', new_value='am')
        meridiem = ['am', 'in the evening']
    else:
        DBManager.DATA.edit_directory(f'{USER}.evening', new_value='no')
    if afternoon:
        DBManager.DATA.edit_directory(f'{USER}.afternoon', new_value='yes')
        DBManager.DATA.edit_directory(f'{USER}.meridiem', new_value='pm')
        meridiem = ['pm', 'in the afternoon']
    else:
        DBManager.DATA.edit_directory(f'{USER}.afternoon', new_value='no')
    if night:
        DBManager.DATA.edit_directory(f'{USER}.night', new_value='yes')
        DBManager.DATA.edit_directory(f'{USER}.meridiem', new_value='pm')
        meridiem = ['pm']
    else:
        DBManager.DATA.edit_directory(f'{USER}.night', new_value='no')

    # Set properly format hour and minute
    if int(h) > 12:
        h = f"{int(h) - 12}"
    if int(m) == 0:
        m = "o clock"
    elif int(m) < 10:
        m = f'0{m}'

    # finally set the time
    time = "{} : {} {}".format(h, m,meridiem[randint(0, len(meridiem)-1)])
    DBManager.DATA.edit_directory(f'{USER}.time', new_value=time)

# Update date info
def updatedate(USER):
    # dictionary of numbers corresponding to a month
    month_dict = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August",
                  "9":"September","10":"October","11":"November","12":"December"
    }

    # get month, day, and year
    dt = datetime.now()
    m,d,y = dt.month, dt.day, dt.year

    # Set date, today, day, month, year
    DBManager.DATA.edit_directory(f'{USER}.date',new_value="{} {}, {}".format(month_dict[str(m)], d, y))
    DBManager.DATA.edit_directory(f'{USER}.today',new_value="{} {}".format(month_dict[str(m)], d))
    DBManager.DATA.edit_directory(f'{USER}.day', new_value="{} {}".format(month_dict[str(m)], d))
    DBManager.DATA.edit_directory(f'{USER}.month',new_value=month_dict[str(m)])
    DBManager.DATA.edit_directory(f'{USER}.year',new_value=str(y))


# Update all info
def all(USER):
    updatetime(USER)
    updatedate(USER)