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
        self.action_interval = 50
        self.action_count = 0

        self.action_positions = {}
        self.action_tag = "ACTION"

        # animation parameters
        self.animate_interval = 500
        self.animate_suspend_flag = False
        self.animate_suspend_seconds = 3
        self.animate_halt_flag = False
        self.animate_halt_x = -1
        self.animate_refresh_flag = False
        self.animate_refresh_threshold = 1420
        self.animate_refresh_interval = 10

        # bind mouth click
        self.canvas.bind(sequence="<Button-1>", func=self.mouth_click_handler)
        self.canvas.bind(sequence="<Button-3>", func=self.mouth_click_handler2)

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
        if self.animate_halt_flag:
            self.animate_halt_x = x
            return

        aid = self.lamport.sorted_actions[self.action_count]
        self.action_count += 1
        action = self.lamport.processes[self.lamport.aid2pid[aid]].find_action(aid)
        y = self.process_height - self.process_stride * action.pid - self.action_diameter / 2

        self.canvas.create_oval(x, y, x+self.action_diameter, y+self.action_diameter, tags=self.action_tag, fill="pink")
        self.canvas.create_text(x, y-15, tags=self.action_tag, text=action.action)
        self.action_positions[action.aid] = [x+self.action_diameter/2, y+self.action_diameter/2]

        # plot message
        if action.action == "recv":
            sid = self.lamport.message_pairs[action.aid]
            sx, sy = self.action_positions[sid]
            self.canvas.create_line(sx, sy, x+self.action_diameter/2, y+self.action_diameter/2, arrow=tkinter.LAST, tags=self.action_tag)

        # refresh
        if not self.animate_refresh_flag and x > self.animate_refresh_threshold:
            self.animate_refresh_flag = True
        if self.animate_refresh_flag:
            for i in range(50):
                self.root.after(i*10, self.refresh_action_move)

        if self.animate_refresh_flag:
            self.root.after(self.animate_interval, self.draw_action, x+self.action_interval-50)
        else:
            self.root.after(self.animate_interval, self.draw_action, x+self.action_interval)

        #self.root.after(self.animate_interval, self.draw_action, x+self.action_interval)

    def mouth_click_handler(self, mouth_click_event):
        self.animate_suspend_flag = True
        print("suspend", self.animate_suspend_seconds, "s!")

    def mouth_click_handler2(self, mouth_click_event):
        if self.animate_halt_flag == False:
            self.animate_halt_flag = True
            print("halt!")
        elif self.animate_halt_flag == True:
            self.animate_halt_flag = False
            self.draw_action(self.animate_halt_x)
            print("Resume!")

    def refresh_action_move(self):
        self.canvas.move(self.action_tag, -1, 0)
        for aid in self.action_positions:
            self.action_positions[aid][0] -= 1
