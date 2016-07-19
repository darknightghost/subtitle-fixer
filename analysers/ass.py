#! /usr/bin/python3
# -*- coding: utf-8 -*-

'''
	Copyright 2016,暗夜幽灵 <darknightghost.cn@gmail.com>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from analysers.analyser import analyser as base_analyser

def time_to_sec(t):
    t = t.strip().split(".")[0].split(":")
    return int(t[0]) * 60 * 60 + int(t[1]) * 60 + int(t[2])

def sec_to_time(sec):
    return "%d:%.2d:%.2d"%(sec // 3600, sec % 3600 // 60, sec % 60)

class Line:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data + "\n"

class FormatLine(Line):
    def __init__(self, data):
        self.data = data
        n = 0
        for w in data.strip("Format:").strip().split(","):
            if w.strip() == "Start":
                self.start_index = n
            elif w.strip() == "End":
                self.end_index = n
            n = n + 1

    def __str__(self):
        return self.data + "\n"

class DialogueLine(Line):
    def __init__(self, data, format_line):
        self.start_index = format_line.start_index
        self.end_index = format_line.end_index

        n = len("Dialogue:")
        i = 0

        while data[n].isspace():
            n = n + 1

        if self.start_index < self.end_index:
            #Get str1
            while i < self.start_index:
                if data[n] == ',':
                    i = i + 1
                n = n + 1
            self.str1 = data[: n]
            data = data[n :]
            
            #Get start time string
            n = 0
            while data[n] != ",":
                n = n + 1
            time_str = data[: n].strip()
            data = data[n :]
            n = 0

            #Get start time
            self.start = time_to_sec(time_str.split(".")[0])
            self.p_start = int(time_str.split(".")[1])

            #Get str2
            while i < self.end_index:
                if data[n] == ',':
                    i = i + 1
                n = n + 1
            self.str2 = data[: n]
            data = data[n :]

            #Get end time string
            n = 0
            while data[n] != ",":
                n = n + 1
            time_str = data[: n].strip()
            data = data[n :]
            self.str3 = data

            #Get end time
            self.end = time_to_sec(time_str.split(".")[0])
            self.p_end = int(time_str.split(".")[1])

        else:
            #Get str1
            while i < self.end_index:
                if data[n] == ',':
                    i = i + 1
                n = n + 1
            self.str1 = data[: n]
            data = data[n :]
            
            #Get end time string
            n = 0
            while data[n] != ",":
                n = n + 1
            time_str = data[: n].strip()
            data = data[n :]
            n = 0

            #Get end time
            self.end = time_to_sec(time_str.split(".")[0])
            self.p_end = int(time_str.split(".")[1])

            #Get str2
            while i < self.start_index:
                if data[n] == ',':
                    i = i + 1
                n = n + 1
            self.str2 = data[: n]
            data = data[n :]

            #Get start time string
            n = 0
            while data[n] != ",":
                n = n + 1
            time_str = data[: n].strip()
            data = data[n :]
            self.str3 = data

            #Get start time
            self.start = time_to_sec(time_str.split(".")[0])
            self.p_start = int(time_str.split(".")[1])


    def __str__(self):
        if self.start_index < self.end_index:
            return self.str1 + sec_to_time(self.start) + ".%.2d"%(self.p_start) \
                    + self.str2 + sec_to_time(self.end) + ".%.2d"%(self.p_end) \
                    + self.str3 + "\n"
        else:
            return self.str1 + sec_to_time(self.end) + ".%.2d"%(self.p_end) \
                    + self.str2 + sec_to_time(self.start) + ".%.2d"%(self.p_start) \
                    + self.str3 + "\n"

class analyser(base_analyser):
    def __init__(self, path, encoding):
        self.encoding = encoding
        f = open(path, "r",  encoding = encoding)
        lines = f.readlines()
        f.close()

        self.lines = []
        event_flag = False
        for l in lines:
            l = l.strip()
            if l == "[Events]":
                event_flag = True
                self.lines.append(Line(l))

            elif l[: len("Format:")] == "Format:" \
                    and event_flag:
                self.format = FormatLine(l)
                self.lines.append(self.format)
            elif l[: len("Dialogue:")] == "Dialogue:" \
                    and event_flag:
                self.lines.append(DialogueLine(l, self.format))
            else:
                self.lines.append(Line(l))

        return

    def speed(self, rate):
        for l in self.lines:
            if type(l) == DialogueLine:
                l.start = l.start * rate
                l.end = l.end * rate
        return

    def offset(self, offset):
        for l in self.lines:
            if type(l) == DialogueLine:
                l.start = l.start + offset
                l.end = l.end + offset
        return

    def save(self, path):
        f = open(path, "w", encoding = self.encoding)
        for l in self.lines:
            f.write(str(l))
        f.close()
