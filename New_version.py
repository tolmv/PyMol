import sys
import math
from Tkinter import *
import tkMessageBox as mb
import numpy as np


class Restraints():

    def __init__(self, main):
        self.help = []
        self.bol = True
        self.error = 0
        self.dG = 0
        self.main = main

        self.labels = ['Gas constant', 'Temperature', 'Standard volume']

        self.r_var = BooleanVar()
        self.r_var.set(1)
        self.rcal1 = Radiobutton(text="kCal", variable=self.r_var, value=0)
        self.rj1 = Radiobutton(text='kJ', variable=self.r_var, value=1)
        self.r_varr = BooleanVar()
        self.r_varr.set(1)
        self.rcal2 = Radiobutton(text="kCal", variable=self.r_varr, value=0)
        self.rj2 = Radiobutton(text='kJ', variable=self.r_varr, value=1)

        self.rj1.grid(row=0, column=0)
        self.rcal1.grid(row=0, column=1)
        self.rj2.grid(row=11, column=0)
        self.rcal2.grid(row=11, column=1)

        self.entry0 = Entry(main)
        self.entry1 = Entry(main)
        self.entry2 = Entry(main)


        self.label_answer0 = Label(main, font=15)
        self.label_answer1 = Label(main, font=15)
        self.label_answer2 = Label(main, font=15)


        self.entry_all = [self.entry0, self.entry1, self.entry2 ]

        self.label_all = [self.label_answer0, self.label_answer1,
                          self.label_answer2]

        self.button_res = Button(main, text="Result: ")

        for i in range(3):
            self.label_all[i].grid(row=i + 1, column=1)
            self.entry_all[i].grid(row=i + 1, column=2)

        for i in range(len(self.label_all)):
            self.label_all[i]['text'] = self.labels[i]

        self.entry_all_get = [self.entry0.get, self.entry1.get, self.entry2.get]

        self.button_res.grid(row=11, column=2)

        self.button_res.bind('<Button-1>', self.__calculate)

        self.destroyProgr = Button(main, text='Exit', bg='black', command=main.destroy)
        self.destroyProgr.grid(row=0, column=3)

        self.helpProgr = Button(main, text=' ? ', bg='#ffb3fe')
        self.helpProgr.grid(row=12, column=0)

    def __calculate(self, event):

        for i, k in enumerate(self.entry_all_get):
            try:
                f = float(k())
                if f <= 0:
                    raise ValueError
            except ValueError:
                mb.showerror("ERROR", "Error, please check your line {}".format(i + 1))
                return
            self.help.append(f)

        self.K = self.help[0]  # Gas constant in kJ/mol/K
        self.V = self.help[2]  # standard volume in nm^3
        self.T = self.help[1]  # Temperature in Kelvin
        if self.r_var == 0:

            self.K = self.help[0] * 4.1868 # Gas constant in kJ/mol/K
            self.V = self.help[2] # standard volume in nm^3
            self.T = self.help[1] # Temperature in Kelvin


        self.rt = App(self.main)


class App():
    def __init__(self, main):
        self.res_top = Toplevel(main)
        self.now_do = Label(self.res_top, font=15)
        self.now_do['text'] = 'Now choose the atoms you need'
        self.now_do.config(bd=20, bg='#aaffff')
        self.now_do.pack()

def main():
    root = Tk()
    app = Restraints(root)
    root.mainloop()


if __name__ == '__main__':
    main()
