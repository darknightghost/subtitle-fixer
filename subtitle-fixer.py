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
import analysers

def main(argv):
    i = 1
    cmd_list = []
    encoding = "utf-8"
    in_path = ""
    out_path = ""
    file_type = ""

    #Analyse args
    if len(argv) < 5:
        usage()
        return 0
    while i < len(argv):
        if argv[i] == "--help":
            usage()
            return 0

        elif argv[i] == "-i":
            i = i + 1
            in_path = argv[i]

        elif argv[i] == "-o":
            i = i + 1
            out_path = argv[i]

        elif argv[i][:len("--encoding")] == "--encoding":
            encoding = argv[i][len("--encoding") + 1 :]

        elif argv[i][:len("--type")] == "--type":
            file_type = argv[i][len("--type") + 1:]

        elif argv[i][:len("--speed")] == "--speed":
            cmd_list.append(["speed", argv[i][len("--speed") + 1:]])


        elif argv[i][:len("--offset")] == "--offset":
            cmd_list.append(["offset", argv[i][len("--offset") + 1:]])

        else:
            print("Unknow option \"%s\""%(argv[i]))
            usage()
            return -1

        i = i + 1

    if in_path == "" or out_path == "" or file_type == "":
        usage()
        return -1

    #Print args
    print("Input file : \"%s\"."%(in_path))
    print("Output file : \"%s\"."%(out_path))
    print("File type : \"%s\"."%(file_type))
    print("Encoding : \"%s\"."%(encoding))

    #Load file
    try:
        exec("from analysers import %s"%(file_type))
        analyser = getattr(sys.modules["analysers.ass"], "analyser")
    except ImportError:
        print("Unsupported file type : \"%s\""%(file_type))
        return -1

    a = analyser(in_path, encoding)
    run_command(a, cmd_list)
    a.save(out_path)
    
    print("Finished.")
    return 0

def run_command(a, cmd):
    #Compute offset
    offset = 0
    for l in cmd:
        if l[0] == "offset":
            try:
                if l[1][0] == '-':
                    offset = offset - time_to_seconds(l[1][1 :])
                elif l[1][0].isnumeric():
                    offset = offset + time_to_seconds(l[1])
                else:
                    print("Unknow time format \"%s\"."%(l[1]))
                    exit(-1)
            except Exception:
                print("Unknow time format \"%s\"."%(l[1]))
                exit(-1)
            break

    #Speed
    rate = 1
    for l in cmd:
        if l[0] == "speed":
            try:
                l[1].index("/")
                video_time = time_to_seconds(l[1].split("/")[0])
                subtitle_time = time_to_seconds(l[1].split("/")[1])
                subtitle_time = subtitle_time + offset
                start_time = a.start_time()
                rate = (video_time - start_time) / (subtitle_time - start_time)
            except ValueError:
                try:
                    rate = int(l[1])
                except SyntaxError:
                    print("Unknow speed value \"%s\"."%(l[1]))
                    exit(-1)
            except SyntaxError:
                print("Unknow speed value \"%s\"."%(l[1]))
                exit(-1)

            break

    print("Offset : %d second(s)."%(offset))
    print("Speed : %f."%(rate))
    a.offset(offset)
    a.speed(rate)

def time_to_seconds(t):
    return int(t.split(':')[2]) \
            + int(t.split(':')[1]) * 60\
            + int(t.split(':')[0]) * 60 * 60

def usage():
    print("Usage:")
    print("    subtitle-fixer.py [options] --type=file-type -i input -o output")
    print("Options:")
    print("    --encoding=encoding-format\tSet the encoding format of input file.Default utf-8.")
    print("    --help\t\t\tShow this help.")
    print("    --offset=[-]offset\t\tChange the begining time of the subtitle.")
    print("    --speed=rate\t\t\tChange the speed of the subtitle.")
    print("        --speed=time-in-video/time-in-subtitle")
    print("The format of time is like H:MM:SS")
    return

ret = main(sys.argv)
exit(ret)
