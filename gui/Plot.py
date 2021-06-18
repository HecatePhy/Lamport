##
# @file   Plot.py
# @author Xiaohan Gao
# @date   Jun 2021
#

import tkinter
import turtle
from time import sleep

def draw_processes(lamport, root, canvas):
    h = 600
    for process in lamport.processes:
        height = h - 100 * process
        line = canvas.create_line(100, height, 900, height, fill="blue")
        canvas.create_text(50, height, text="Process"+str(process))

def draw_action(action, root, canvas, x):
    y = 600 - 100 * action.pid - 5 
    canvas.create_oval(x, y, x+10, y+10, fill="pink")

def draw_actions(lamport, root, canvas):
    interval = 800 / len(lamport.sorted_actions) 
    sleep_time = 0.05
    x = 100
    cnt = 0
    for aid in lamport.sorted_actions:
        action = lamport.processes[lamport.aid2pid[aid]].find_action(aid)
        #draw_action(action, root, canvas, x)
        root.after(200*cnt, draw_action, action, root, canvas, x)
        x += interval
        cnt += 1
    pass

def animate_logs(lamport):
    root = tkinter.Tk()

    canvas = tkinter.Canvas(root, width=1000, height=1000, bg="wheat")
    canvas.pack()

    draw_processes(lamport, root, canvas)

    draw_actions(lamport, root, canvas)

    root.mainloop()
