##
# @file   Action.py
# @author Xiaohan Gao
# @date   Jun 2021
#

class Action():
    def __init__(self, aid, pid, timestamp, **args):
        self.aid = aid
        self.pid = pid
        self.timestamp = timestamp
        self.processes = args['processes'] # set of ids of all processes
        self.processes.discard(self.pid)
        self.action = args['action']
        self.message = args['message']
        self.args = args

    # recv msg from this process
    def recv_from(self):
        assert self.action == 'recv', "[ERROR] Not a recv action"
        # message: '<tt, pid>' or 'reply pid'
        #self.message = self.args['message']
        return self.message[1]

    # send msg to those processes
    def send_to(self):
        assert self.action in {'request', 'reply', 'release'}, "[ERROR] Not a send action"
        if self.action == 'request':
            return self.processes
        elif self.action == 'reply':
            # 'replyto': a tuple <tt, pid> representing the original message
            return [self.args['replyto'][1]]
        elif self.action == 'release':
            return self.processes

    def __str__(self):
        return "PID " + str(self.pid) + " AID " + str(self.aid) + " TIMESTAMP " + str(self.timestamp) + " ACTION " + self.action

    def __repr__(self):
        return self.__str__()
