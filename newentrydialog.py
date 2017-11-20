from newdialog import SpecificDialog
from tkinter import *


class NewEntryDialog(SpecificDialog):
    def body(self, parent):
        self.result = []
        self.entries = []

        for i in range(6):
            self.entries.append(Entry(parent))
            self.entries[i].grid(row=1, column=i, sticky=W+E)

        for i in range(6):
            Label(parent, text=str(i+1)).grid(row=0, column=i, sticky=E+W)

        # Return an initial focus to [name] entry.
        return self.entries[0]

    def apply(self):
        self.result = []
        for entry in self.entries:
            self.result.append(entry.get())

