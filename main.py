##
# @file   main.py
# @author Xiaohan Gao
# @date   Jun 2021
#

from gui.Lamport import *
from gui.Parser import *

import sys

def main(filedir):
    lamport = Lamport()
    parse_logs(lamport, filedir)
    lamport.construct_graph()
    lamport.sort_actions()
    print(lamport.sorted_actions)
    pass

if __name__ == "__main__":
    assert len(sys.argv) > 1, "[ERROR] No input case"
    main(sys.argv[1])
