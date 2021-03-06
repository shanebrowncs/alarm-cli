import calendar
import time
import json
#import wx // Temporarily remove wx dependency
from json.decoder import JSONDecodeError
import datetime
import time

class Alarm:
    timestamp = ""
    description = ""

    def __init__(self, epoch, description):
        self.timestamp = epoch
        self.description = description

#    @staticmethod
#    def playAlarm():
#        sound = wx.Sound('assets/alarm.wav')
#        sound.Play(wx.SOUND_ASYNC)


    @staticmethod
    def timeToEpoch(h, m, s):
        seconds = ((int(h) * 60) * 60) + (int(m) * 60) + int(s)

        seconds = seconds + int(calendar.timegm(time.gmtime()))
        return seconds

    @staticmethod
    def alarmFromTime(h, m, s, description):
        epoch = Alarm.timeToEpoch(h, m, s)
        al = Alarm(epoch, description)
        return al

    @staticmethod
    def alarmFromEpoch(epoch, description):
        al = Alarm(epoch, description)
        return al

    @staticmethod
    def loadAlarms(jsonFile):
        alarms = list()

        try:
            with open(jsonFile) as rFile:
                data = rFile.read()
        except FileNotFoundError:
            return None

        try:
            jsonData = json.loads(data)
        except JSONDecodeError:
            return None

        for item in jsonData:
            curAlarm = Alarm.alarmFromEpoch(item['timestamp'], item['description'])
            alarms.append(curAlarm)
        return alarms

    @staticmethod
    def saveAlarms(alarms, outFile):
        jsonFile = json.dumps([ob.__dict__ for ob in alarms], indent=4)
        with open(outFile, "w") as wFile:
            wFile.write(jsonFile)

    @staticmethod
    def listAlarms(alarms):
        curTime = datetime.datetime.now() 
        for index, item in enumerate(alarms):
            timeLeft = ""

            # If time < now: set timer text to "Passed"
            futureTime = datetime.datetime.fromtimestamp(item.timestamp)
            if datetime.datetime.now() > futureTime:
                timeLeft = "Passed"
            else:
                diff = futureTime - curTime

                # Get time difference in h,m,s format
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                timeLeft = timeLeft + str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"

            print("Alarm " + str(index + 1) + ": " + time.strftime('%I:%M %p', time.localtime(item.timestamp)) + " (" + timeLeft + ") : " + str(item.description))

    @staticmethod
    def checkAlarms(alarms):
        retAlarms = list()
        curTime = datetime.datetime.now()
        for item in alarms:
            alarmTime = datetime.datetime.fromtimestamp(int(item.timestamp))
            if alarmTime <= curTime:
                retAlarms.append(item)

        return retAlarms
