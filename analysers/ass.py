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
        return data

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
        print(self.start_index)
        print(self.end_index)

    def __str__(self):
        return data

class DialogueLine(Line):
    def __init__(self, data, format_line):
        self.data = data

    def __str__(self):
        return data


class analyser(base_analyser):
    def __init__(self, path, encoding):
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
        pass

    def offset(self, offset):
        pass

    def save(self, path):
        pass
