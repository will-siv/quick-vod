#!/bin/python3

from tkinter import *
from tkinter import ttk
import os

def main():
    def addRow():
        next_row = len(row_entries) + 1
        ind_entries = [] # empty list to hold each of the five boxes
        for i in range(5):
            ent = Entry(frame_for_boxes)
            ent.grid(row=next_row, column=i)
            ind_entries.append( ent )
        row_entries.append(ind_entries)

    def writeToCsv():
        name = tournament_name.get()
        with open("matches.csv", 'w+') as w:
            w.seek(0)
            w.write(name + '\n')
            for ent in row_entries:
                for i,item in enumerate(ent):
                    w.write(item.get())
                    if i != 4:
                        w.write(',')
                w.write('\n')
        print(name)

    def removeRow():
        if len(row_entries) == 1:
            return
        popped = row_entries.pop()
        for i in popped:
            i.destroy()

    root = Tk()
    root.title("Vod And Game Interval/Name Adjuster")

    row_entries = []

    top_frame = Frame(root)
    tournament_label = Label(top_frame, text="Tournament Name")
    tournament_name = Entry(top_frame)
    tournament_label.grid(column=0, row=0)
    tournament_name.grid(column=0, columnspan=1, row=1)
    top_frame.pack()

    frame_for_boxes = Frame(root)
    frame_for_boxes.pack()

    Label(frame_for_boxes, text="Start Time").grid(column=0,row=0)
    Label(frame_for_boxes, text="Match").grid(column=1,row=0)
    Label(frame_for_boxes, text="Player 1").grid(column=2,row=0)
    Label(frame_for_boxes, text="Player 2").grid(column=3,row=0)
    Label(frame_for_boxes, text="End Time").grid(column=4,row=0)

    addRow()
    frame_for_buttons = Frame(root)
    frame_for_buttons.pack()

    addRowButton = Button(frame_for_buttons, text="[+]", command=addRow)
    addRowButton.grid(column=0,row=0)

    removeRowButton = Button(frame_for_buttons, text="[-]", command=removeRow)
    removeRowButton.grid(column=1,row=0)

    bot_frame = Frame()
    bot_frame.pack(side='right')

    finishButton = Button(bot_frame, text="Save this tournament", command=writeToCsv)
    finishButton.grid(row=0,column=0)

    closeButton = Button(bot_frame, text="Close", command=root.destroy)
    closeButton.grid(row=0,column=1)

    root.mainloop()
    return

if __name__ == "__main__":
    main()
