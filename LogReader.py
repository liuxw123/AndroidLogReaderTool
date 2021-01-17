"""
    :Description: 将log文件中，每行log读取封装，仅对外提供查询
    :Author: lxw
    :File: LogReader.py
    :Version: V1.0
    :Date: 2021-01-09 8:05 PM
    :CopyRight: all rights is reversed.
"""

from datetime import datetime


class LineLog:

    def __init__(self, line: int, time: datetime, pid: int, tid: int, debugLevel: str, tag: str, log: str) -> None:
        """
        每一行log封装成的对象
        :param line: 该行log所在源文件的行数
        :param time: 该行log发生的时间
        :param pid:  pid
        :param tid:  tid
        :param debugLevel:
        :param tag:
        :param log: log内容
        """
        super().__init__()
        self.line = line
        self.time = time
        self.pid = pid
        self.tid = tid
        self.debugLevel = debugLevel
        self.tag = tag
        self.log = log

    def __str__(self) -> str:
        return "{:6d} {:s} {:5d} {:5d} {:s} {:s}: {:s}".format(self.line, self.time.strftime("%m-%d %H:%M:%S.%f"),
                                                               self.pid, self.tid,
                                                               self.debugLevel, self.tag, self.log)


class LogReader:

    def __init__(self, logFile: str) -> None:
        """
        构造函数
        :param logFile: log文件路径
        """
        super().__init__()
        self.logFile = logFile
        self.allLog = []
        self.__parse()

    def __parse(self):
        fd = open(self.logFile, "r")
        contents = fd.readlines()
        fd.close()

        def readLine(line: str) -> LineLog:
            if len(line) < 40:
                return None

            timeStr = line[0:21]
            pid = int(line[22:27])
            tid = int(line[28:33])
            debugLevel = line[34]
            pos = line[36:].index(" ")
            tag = line[36:pos + 35]
            log = line[pos + 37:].strip("\r\n").strip(" ").strip("\n").strip(" ")
            time = datetime.strptime(timeStr, "%m-%d %H:%M:%S.%f")
            return LineLog(0, time, pid, tid, debugLevel, tag, log)

        for i, line in enumerate(contents):
            obj = readLine(line)

            if obj is None:
                continue

            obj.line = i + 1
            self.allLog.append(obj)

    def get(self) -> [LineLog]:
        return self.allLog

    def findByTag(self, dstTag: str) -> [LineLog]:
        res = []
        for log in self.allLog:
            if log.tag == dstTag:
                res.append(log)

        return res
