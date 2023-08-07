# Remaining time - current time function
import datetime as dt
import pytz


def timeleft_function(datestart):
    start = dt.datetime.strftime(datestart, "%Y-%m-%d")
    # start = "2021-05-09"
    # print("start"*10, type(start))
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    IST = pytz.timezone('Asia/Kolkata')
    _now = dt.datetime.now(IST)
    __now = dt.datetime.strftime(_now, "%Y-%m-%d")
    now = dt.datetime.strptime(__now,"%Y-%m-%d")
    delta = now - start
    if delta.days == 0:
        timeleft = "Today"
        timeleft = ''.join(timeleft) 
        return timeleft
    elif delta.days == 1:
        timeleft = "Yesterday"
        timeleft = ''.join(timeleft) 
        return timeleft
    elif delta.days > 1 and delta.days <= 30:
        timeleft = str(delta.days) +" days ago" 
        timeleft = ''.join(timeleft) 
        return timeleft
    else:
        if delta.days // 30 == 1:
            timeleft = "a month  ago"
            return timeleft
        elif ((delta.days // 30) > 1) and ((delta.days // 30) < 12):
            timeleft = str(delta.days // 30) +" months ago" 
            timeleft = ''.join(timeleft) 
            return timeleft
        else:
            days = delta.days // 30
            day = days//12
            if day == 1:
               timeleft = "a year ago"
               return timeleft 
            else:
                timeleft = str(day) + " years ago"
                return timeleft
            

def working_time_function(order_start_date, order_end_date):
    delta = order_end_date - order_start_date
    if delta.days == 0:
        if delta.seconds // 3600 == 0:
            if delta.seconds // 60 == 0:
                timeleft = str(delta.seconds) + " s"
                timeleft = ''.join(timeleft)
                return timeleft
            else: 
                timeleft = str(delta.seconds // 60) + " m ", str(delta.seconds % 60) + " s"
                timeleft = ''.join(timeleft)
                return timeleft
        else:           
            timeleft = str(delta.seconds // 3600) +" h " + str(delta.seconds // 60 % 60)+ " m"
            timeleft = ''.join(timeleft)
            return timeleft
    elif delta.days == 1:
        timeleft = str(delta.days) +" day " + str(delta.seconds // 3600) +" h"
        timeleft = ''.join(timeleft) 
        return timeleft
    elif delta.days > 1:
        timeleft = str(delta.days) +" days"
        timeleft = ''.join(timeleft) 
        return timeleft
    else:
        timeleft = "0"
        return timeleft