"""
    :Description: 获取AT AP AF事件发生的事件，如创建track\record\device connected.
    :Author: lxw
    :File: EventTimestamp.py
    :Version: V1.0
    :Date: 2021-01-09 8:02 PM
    :CopyRight: all rights is reversed.
"""

from LogReader import LogReader, LineLog
import os

class LogEventTimeStamp:
    def __init__(self, logFiles: [str]) -> None:
        super().__init__()
        self.logFiles = logFiles
        self.reader = None
        self.loggerEvent = ["AT", "AR", "Device"]

    def getAudioTrackEvent(self) -> [LineLog]:
        if self.reader is None:
            return
        return self.reader.findByTag("AudioTrack")

    def getAudioRecordEvent(self) -> [LineLog]:
        if self.reader is None:
            return
        return self.reader.findByTag("AudioRecord")

    def getAudioDevicePlugEvent(self) -> [LineLog]:
        if self.reader is None:
            return
        all = self.reader.findByTag("APM_AudioPolicyManager")
        res = []

        for item in all:
            if "setDeviceConnectionState" in item.log:
                res.append(item)

        return res

    def toFile(self):
        eventsForAt = []
        eventsForAr = []
        eventsForAudioDevice = []

        for logFile in self.logFiles:
            self.reader = LogReader(logFile)
            for item in self.loggerEvent:
                if item == "AT":
                    eventsForAt = eventsForAt + self.getAudioTrackEvent()
                elif item == "AR":
                    eventsForAr = eventsForAr + self.getAudioRecordEvent()
                elif item == "Device":
                    eventsForAudioDevice = eventsForAudioDevice + self.getAudioDevicePlugEvent()
                else:
                    continue

        events = ["="*50+"AudioTrack Event Begin"+"="*50] + \
                 eventsForAt + \
                 ["="*50+"AudioTrack Event end"+"="*50, "\n"] + \
                 ["=" * 50 + "AudioRecord Event Begin" + "=" * 50] + \
                 eventsForAr + \
                 ["=" * 50 + "AudioRecord Event end" + "=" * 50, "\n"] + \
                 ["=" * 50 + "AudioDevicePlug Event Begin" + "=" * 50] + \
                 eventsForAudioDevice + \
                 ["=" * 50 + "AudioDevicePlug Event end" + "=" * 50, "\n"]

        strings = ""
        for item in events:
            strings = strings + str(item) + "\n"

        if strings == "":
            return

        fd = open("result", "w+")
        fd.write(strings)
        fd.close()

def getMainLogPath(path):
    mainLogs = []
    files = os.listdir(path)

    for file in files:
        if os.path.isdir(path+"/"+file):
            mainLogs = mainLogs + getMainLogPath(path+"/"+file)
        else:
            if file.startswith("main_log"):
                mainLogs.append(path+"/"+file)

    return mainLogs


mainLog = getMainLogPath(os.getcwd())
mainLog.sort(reverse=False)


logReader = LogEventTimeStamp(mainLog)
res = logReader.toFile()
print("finished.")