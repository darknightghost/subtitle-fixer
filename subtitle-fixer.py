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

import sys

def main(argv):
    usage()
    return 0

def usage():
    print("Usage:")
    print("    subtitle-fixer.py [options] -i input -o output")
    print("Options:")
    print("    --encoding=encoding-format\tSet the encoding format of input file.Default utf-8.")
    print("    --help\t\t\tShow this help.")
    print("    --offset=offset\t\tChange the begining time of the subtitle.")
    print("    -speed=rate\t\t\tChange the speed of the subtitle.")
    print("        --speed=time-in-video/time-in-subtitle")
    print("The format of time is like H:MM:SS:PP")
    return

ret = main(sys.argv)
exit(ret)
