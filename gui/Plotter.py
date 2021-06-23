##
# @file   Plotter.py
# @author Xiaohan Gao
# @date   Jun 2021
#

import tkinter
from time import sleep

class Plotter():
    def __init__(self, lamport):
        self.lamport = lamport
        self.root = tkinter.Tk()
        self.root.title("Lamport Visualization")

        # canvas parameters
        self.width = 1600
        self.height = 1000
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, bg="misty rose")

        # plot parameters
        self.process_height = 600
        self.process_stride = 100
        self.process_startx = 100
        self.process_endx = 1500
        self.process_namex = 50

        self.action_startx = self.process_startx
        self.action_diameter = 10
        self.action_interval = 45
        self.action_count = 0

        self.action_positions = {}

        # animation parameters
        self.animate_interval = 200
        self.animate_suspend_flag = False
        self.animate_suspend_seconds = 3

        # bind mouth click
        self.canvas.bind(sequence="<Button-1>", func=self.mouth_click_handler)

    def animate(self):
        self.canvas.pack()

        self.draw_processes()

        action = self.lamport.processes[self.lamport.aid2pid[0]].find_action(0)
        self.action_count = 0
        self.draw_action(self.action_startx)

        self.root.mainloop()
        pass

    def draw_processes(self):
        for process in self.lamport.processes:
            height = self.process_height - self.process_stride * process
            line = self.canvas.create_line(self.process_startx, height, self.process_endx, height, fill="blue")
            self.canvas.create_text(self.process_namex, height, text="Process"+str(process))

    def draw_action(self, x):
        # suspend if set animate_suspend
        if self.animate_suspend_flag:
            sleep(self.animate_suspend_seconds)
            self.animate_suspend_flag = False

        aid = self.lamport.sorted_actions[self.action_count]
        self.action_count += 1
        action = self.lamport.processes[self.lamport.aid2pid[aid]].find_action(aid)
        y = self.process_height - self.process_stride * action.pid - self.action_diameter / 2
        self.canvas.create_oval(x, y, x+self.action_diameter, y+self.action_diameter, fill="pink")
        self.canvas.create_text(x, y-15, text=action.action)
        self.action_positions[action.aid] = (x+self.action_diameter/2, y+self.action_diameter/2)

        # plot message
        if action.action == "recv":
            sid = self.lamport.message_pairs[action.aid]
            sx, sy = self.action_positions[sid]
            self.canvas.create_line(sx, sy, x+self.action_diameter/2, y+self.action_diameter/2, arrow=tkinter.LAST)

        self.root.after(self.animate_interval, self.draw_action, x+self.action_interval)

    def mouth_click_handler(self, mouth_click_event):
        self.animate_suspend_flag = True
        print("suspend", self.animate_suspend_seconds, "s")
