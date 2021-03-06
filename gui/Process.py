##
# @file   Process.py
# @author Xiaohan Gao
# @date   Jun 2021
#

class Process():
    def __init__(self, pid):
        self.pid = pid
        #self.actions = {}
        self.actions = []
        self.channels = {}

    def add_action(self, aid, action):
        #self.actions[aid] = action
        self.actions.append(action)
        if action.action in {'reply', 'request', 'release'}:
            for proc in action.send_to():
                if proc not in self.channels:
                    self.channels[proc] = []
                self.channels[proc].append((action.aid, action.message))
        else:
            pass
        return

    # find action by aid
    def find_action(self, aid):
        for action in self.actions:
            if action.aid == aid:
                return action
        return None
