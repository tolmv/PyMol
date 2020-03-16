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

        self.labels = ['T', 'r0', 'thA', 'thB', 'K_r', 'K_thA',
                       'K_thB', 'K_phiA', 'K_phiB', 'K_phiC']

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
        self.entry3 = Entry(main)
        self.entry4 = Entry(main)
        self.entry5 = Entry(main)
        self.entry6 = Entry(main)
        self.entry7 = Entry(main)
        self.entry8 = Entry(main)
        self.entry9 = Entry(main)

        self.label_answer0 = Label(main, font=15)
        self.label_answer1 = Label(main, font=15)
        self.label_answer2 = Label(main, font=15)
        self.label_answer3 = Label(main, font=15)
        self.label_answer4 = Label(main, font=15)
        self.label_answer5 = Label(main, font=15)
        self.label_answer6 = Label(main, font=15)
        self.label_answer7 = Label(main, font=15)
        self.label_answer8 = Label(main, font=15)
        self.label_answer9 = Label(main, font=15)

        self.entry_all = [self.entry0, self.entry1, self.entry2, self.entry3, self.entry4,
                          self.entry5, self.entry6, self.entry7, self.entry8, self.entry9]

        self.label_all = [self.label_answer0, self.label_answer1,
                          self.label_answer2, self.label_answer3, self.label_answer4,
                          self.label_answer5, self.label_answer6,
                          self.label_answer7, self.label_answer8, self.label_answer9]

        self.button_res = Button(main, text="Result: ")

        for i in range(10):
            self.label_all[i].grid(row=i + 1, column=1)
            self.entry_all[i].grid(row=i + 1, column=2)

        for i in range(len(self.label_all)):
            self.label_all[i]['text'] = self.labels[i]

        self.entry_all_get = [self.entry0.get, self.entry1.get, self.entry2.get,
                              self.entry3.get, self.entry4.get,
                              self.entry5.get, self.entry6.get,
                              self.entry7.get, self.entry8.get, self.entry9.get]

        self.button_res.grid(row=11, column=2)

        self.button_res.bind('<Button-1>', self.__calculate)

        self.destroyProgr = Button(main, text='Exit', bg='red', command=main.destroy)
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

        if self.r_var.get() == 1:

            K = 8.314472 * 0.001 * 0.23885  # Gas constant in kJ/mol/K
            V = 1.66  # standard volume in nm^3

            T = self.help[0]  # Temperature in Kelvin
            r0 = self.help[1]  # Distance in nm
            thA = self.help[2]  # Angle in degrees
            thB = self.help[3]  # Angle in degrees

            K_r = self.help[4] * 0.23885  # force constant for distance (kJ/mol/nm^2)
            K_thA = self.help[5] * 0.23885  # force constant for angle (kJ/mol/rad^2)
            K_thB = self.help[6] * 0.23885  # force constant for angle (kJ/mol/rad^2)
            K_phiA = self.help[7] * 0.23885  # force constant for dihedral (kJ/mol/rad^2)
            K_phiB = self.help[8] * 0.23885  # force constant for dihedral (kJ/mol/rad^2)
            K_phiC = self.help[9] * 0.23885  # force constant for dihedral (kJ/mol/rad^2)

            thA = math.radians(thA)  # convert angle from degrees to radians --> math.sin() wants radians
            thB = math.radians(thB)  # convert angle from degrees to radians --> math.sin() wants radians

            arg = (
                    (8.0 * math.pi ** 2.0 * V) / (r0 ** 2.0 * math.sin(thA) * math.sin(thB))
                    *
                    (
                            ((K_r * K_thA * K_thB * K_phiA * K_phiB * K_phiC) ** 0.5) / (
                                (2.0 * math.pi * K * T) ** (3.0))
                    )
            )

            self.dG = - K * T * math.log(arg)

        else:
            K = 8.314472 * 0.001  # Gas constant in kJ/mol/K
            V = 1.66  # standard volume in nm^3

            T = self.help[0]  # Temperature in Kelvin
            r0 = self.help[1]  # Distance in nm
            thA = self.help[2]  # Angle in degrees
            thB = self.help[3]  # Angle in degrees

            K_r = self.help[4]  # force constant for distance (kJ/mol/nm^2)
            K_thA = self.help[5]  # force constant for angle (kJ/mol/rad^2)
            K_thB = self.help[6]  # force constant for angle (kJ/mol/rad^2)
            K_phiA = self.help[7]  # force constant for dihedral (kJ/mol/rad^2)
            K_phiB = self.help[8]  # force constant for dihedral (kJ/mol/rad^2)
            K_phiC = self.help[9]  # force constant for dihedral (kJ/mol/rad^2)

            thA = math.radians(thA)  # convert angle from degrees to radians --> math.sin() wants radians
            thB = math.radians(thB)  # convert angle from degrees to radians --> math.sin() wants radians

            arg = (
                    (8.0 * math.pi ** 2.0 * V) / (r0 ** 2.0 * math.sin(thA) * math.sin(thB))
                    *
                    (
                            ((K_r * K_thA * K_thB * K_phiA * K_phiB * K_phiC) ** 0.5) / (
                                (2.0 * math.pi * K * T) ** (3.0))
                    )
            )

            self.dG = - K * T * math.log(arg)

        self.rt = App(self.main, self.dG, self.r_varr)


class App():
    def __init__(self, main, dG, r_varr):
        self.res_top = Toplevel(main)
        self.label_res_top1 = Label(self.res_top, font=15)
        self.label_res_top2 = Label(self.res_top, font=15)
        if r_varr.get() == 1:
            self.label_res_top1['text'] = "dG_off = {:.3f} kJ/mol".format(dG)
            self.label_res_top2['text'] = "dG_on  = {:.3f} kJ/mol".format(-dG)
        else:
            self.label_res_top1['text'] = "dG_off = {:.3f} kCal/mol".format(dG * 4.1868)
            self.label_res_top2['text'] = "dG_on  = {:.3f} kCal/mol".format(-dG * 4.1868)
        self.label_res_top1.grid(row=0, column=0)
        self.label_res_top2.grid(row=0, column=1)


def main():
    root = Tk()
    app = Restraints(root)
    root.mainloop()


if __name__ == '__main__':
    main()
