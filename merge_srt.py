#!/usr/bin/python
import string
import sys
import re

class Block:
    def __init__(self, id, start_time, end_time, text):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.text = text
    
    def __add__(block1, block2):
        first = block1
        second = block2
        if block1.start_time > block2.start_time:
            first = block2
            second = block1
        rst = Block.__init__(first.id, first.end_time, second.end_time, first.text + second.text)
        return rst

def parse_time(str_time):
    vals = string.split(str_time, ':')
    rst = 0.0
    for v in vals:
        v = string.replace(v, ',', '.')
        rst = rst * 60.0 + float(v)
    return rst

def parse_time_range(str_time):
    strs = string.split(str_time, '-->')
    rst = []
    for s in strs:
        rst.append(parse_time(s))
    return rst

#print parse_time('00:00:31,040')
#print parse_time_range('00:00:31,040 --> 00:00:33,120')

def process(file_name, start_time, end_time):
    blocks = []
    with open(file_name) as f:
        str_id, str_time, text = None, None, None
        for line in f:
            line = line.strip()
            if line == '':
                str_id, str_time, text = None, None, None
                continue
            elif line.isdigit():
                str_id = line
            elif re.match('[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9] --> [0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]', line):
                str_time = line
            else:
                text = line
                 
            if str_id and str_time and text:
                s_time, e_time = parse_time_range(str_time)
                blocks.append(Block(int(str_id), s_time, e_time, text))
    # merge & sort
    with open(file_name + 'm.srt', mode = 'rw'):
        for b in blocks:
            #write back
            pass

USAGE = 'usage \n [source_file] [start_time] [end_time]'
if len(sys.argv) < 4:
    print USAGE
else:
    file_name = str(sys.argv[1])
    start_time = str(sys.argv[2])
    end_time = str(sys.argv[3])
    process(file_name, start_time, end_time)







