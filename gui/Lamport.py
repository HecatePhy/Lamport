##
# @file   Lamport.py
# @author Xiaohan Gao
# @date   Jun 2021
#

from gui.Process import *

import networkx as nx

class Lamport():
    def __init__(self):
        self.graph = nx.DiGraph()
        self.aid2pid = {}
        self.processes = {}
        self.sorted_actions = []
        self.message_pairs = {}
        pass

    # edge <aid1, aid2> means action1 is earlier than action2
    def construct_graph(self):
        # all actions in the same process have an order
        for _, process in self.processes.items():
            for i in range(len(process.actions)-1):
                self.graph.add_edge(process.actions[i].aid, process.actions[i+1].aid)
                self.aid2pid[process.actions[i].aid] = process.pid
                self.aid2pid[process.actions[i+1].aid] = process.pid

        # traverse the message channels to find an order between <send, recv>
        for _, process in self.processes.items():
            for action in process.actions:
                if action.action != 'recv':
                    continue
                pid = action.recv_from()
                proc = self.processes[pid]
                aid, _ = proc.channels[process.pid].pop(0)
                self.message_pairs[action.aid] = aid 
                self.graph.add_edge(aid, action.aid)
        
        return

    # topo sort for an order of actions
    def sort_actions(self):
        self.sorted_actions = list(nx.topological_sort(self.graph))

        return

    # show the actions in a logical order
    def show_sorted_actions(self):
        for aid in self.sorted_actions:
            pid = self.aid2pid[aid]
            print(self.processes[pid].find_action(aid))
