import datetime
import time

def datetime_to_timestamp(datetime_obj):
    local_timestamp = int(time.mktime(datetime_obj.timetuple()))
    return local_timestamp


def timestamp_to_datetime(timestamp):
    local_dt_time = datetime.datetime.fromtimestamp(timestamp)
    return local_dt_time

def time2str(day, month, year, hours, minutes, seconds):
    day = str(day) if day >= 10 else "0" + str(day)
    month = num2Month[month]
    year = str(year)
    hours = str(hours) if hours >= 10 else "0" + str(hours)
    minutes = str(minutes) if minutes >= 10 else "0" + str(minutes)
    seconds = str(seconds) if seconds >= 10 else "0" + str(seconds)
    return day + "/" + month + "/" + year + ":" + hours + ":" + minutes + ":" + seconds
    
month2Num = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, \
              "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,\
              "Nov": 11, "Dec": 12}

num2Month = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", \
                6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",\
              11: "Nov", 12: "Dec"}
