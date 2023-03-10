# -*- coding: utf-8 -*-
""" This is the action module of Biovarase."""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="action")

        self.parent = parent
        self.index = index
        self.attributes("-topmost", True)
        self.transient(parent)
        self.resizable(0, 0)

        self.action = tk.StringVar()
        self.enable = tk.BooleanVar()

        self.init_ui()
        self.nametowidget(".").engine.center_me(self)

    def init_ui(self):

        w = self.nametowidget(".").engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, text="Action:").grid(row=r, sticky=tk.W)
        self.txtAction = ttk.Entry(w, textvariable=self.action)
        self.txtAction.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.enable,)
        chk.grid(row=r, column=c, sticky=tk.W)

        self.nametowidget(".").engine.get_save_cancel(self, w)

    def on_open(self, selected_item=None):

        if self.index is not None:
            self.selected_item = selected_item
            what = "Edit {0}"
            self.set_values()
        else:
            what = "Add {0}"
            self.enable.set(1)

        msg = what.format(self.winfo_name().title())
        self.title(msg)
        self.txtAction.focus()

    def set_values(self,):

        self.action.set(self.selected_item[1])
        self.enable.set(self.selected_item[2])

    def get_values(self,):

        return [self.action.get(),
                self.enable.get(),]


    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql(self.parent.table, self.parent.field)

                args.append(self.selected_item[0])

            else:

                sql = self.nametowidget(".").engine.get_insert_sql(self.parent.table, len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
            self.parent.on_open()

            if self.index is not None:
                self.parent.lstItems.see(self.index)
                self.parent.lstItems.selection_set(self.index)
            else:
                #force focus on listbox
                idx = list(self.parent.dict_items.keys())[list(self.parent.dict_items.values()).index(last_id)]
                self.parent.lstItems.see(idx)
                self.parent.lstItems.selection_set(idx)

            self.on_cancel()


    def on_cancel(self, evt=None):
        self.destroy()
