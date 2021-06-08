##
# @file   Parser.py
# @author Xiaohan Gao
# @date   Jun 2021
#

from gui.Action import *
from gui.Process import *
from gui.Lamport import *

import os
import re

def parse_logs(lamport, filedir):
    # get all processes
    log_files = list(map(lambda fname: os.path.join(filedir, fname), os.listdir(filedir)))
    processes = set(map(lambda fname: int(re.findall(r'\d+', fname)[0]), os.listdir(filedir)))

    aid_cnt = 0
    for log_file in log_files:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            pid = int(lines[0].split()[1])

            proc = Process(pid)

            for line in lines[1:]:
                segs = line.split()
                if len(segs) < 1:
                    continue
                timestamp = int(segs[0])
                action = segs[1]
                arguments = {}
                arguments['action'] = action
                arguments['processes'] = processes.copy()
                if action == 'start':
                    arguments['message'] = None
                elif action == 'run':
                    arguments['message'] = None
                elif action == 'request':
                    msg = re.split('<|>|,', segs[2])
                    arguments['message'] = (int(msg[1]), int(msg[2]))
                elif action == 'reply':
                    arguments['message'] = ('reply', int(segs[2]))
                    msg = re.split('<|>|,', segs[4])
                    arguments['replyto'] = (int(msg[1]), int(msg[2]))
                elif action == 'recv':
                    # recv request
                    if len(segs) == 3:
                        msg = re.split('<|>|,', segs[2])
                        arguments['message'] = (int(msg[1]), int(msg[2]))
                    # recv reply
                    elif len(segs) == 4:
                        arguments['message'] = ('reply', int(segs[3]))
                else:
                    print("[WARNING] Unknown action")
                aid = aid_cnt
                proc.add_action(aid, Action(aid, pid, timestamp, **arguments))
                aid_cnt += 1

            lamport.processes[pid] = proc

    return
