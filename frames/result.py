# -*- coding: utf-8 -*-
""" This is the result module of Biovarase."""
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from calendarium import Calendarium




class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name='result')

        self.parent = parent
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)

        self.test = tk.StringVar()
        self.batch = tk.StringVar()
        self.result = tk.DoubleVar()
        self.recived_time = tk.StringVar()
        self.enable = tk.BooleanVar()

        self.vcmd = self.nametowidget(".").engine.get_validate_float(self)
        self.set_style()
        self.init_ui()
        self.nametowidget(".").engine.center_me(self)


    def set_style(self):

        s = ttk.Style()

        s.configure('Data.TLabel', font=('Helvetica', 12, 'bold'))


    def init_ui(self):

        w = self.nametowidget(".").engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, text="Test:").grid(row=r, sticky=tk.W)
        lbl = ttk.Label(w, style='Data.TLabel', textvariable=self.test)
        lbl.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Batch:").grid(row=r, sticky=tk.W)
        lbl = ttk.Label(w, style='Data.TLabel', textvariable=self.batch)
        lbl.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Result:").grid(row=r, sticky=tk.W)
        self.txtResult = ttk.Entry(w, width=8, justify=tk.CENTER, validate='key', validatecommand=self.vcmd, textvariable=self.result)
        self.txtResult.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Recived:").grid(row=r, sticky=tk.N+tk.W)

        self.recived_date = Calendarium(self, "")
        self.recived_date.get_calendarium(w, r, c)

        r += 1
        lbl = ttk.Label(w, text="Time:").grid(row=r, sticky=tk.W)
        lbl = ttk.Label(w, style='Data.TLabel', textvariable=self.recived_time)
        lbl.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Enable:").grid(row=r, sticky=tk.W)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.enable,)
        chk.grid(row=r, column=c, sticky=tk.W)

        if self.index is not None:
            self.nametowidget(".").engine.get_save_cancel_delete(self, w)
        else:
            self.nametowidget(".").engine.get_save_cancel(self, w)


    def on_open(self, selected_test, selected_batch, selected_result=None):

        self.selected_batch = selected_batch
        self.test.set(selected_test[1])
        self.batch.set(self.selected_batch[2])


        if self.index is not None:
            self.selected_result = selected_result
            msg = "Update {0} for {1}".format(self.winfo_name(), selected_test[1])
            self.set_values()
        else:
            msg = "Insert {0} for {1}".format(self.winfo_name(), selected_test[1])
            self.enable.set(1)
            self.result.set('')
            self.recived_date.set_today()

        self.title(msg)
        self.txtResult.focus()

    def on_save(self, evt=None):

        if self.nametowidget(".").engine.on_fields_control(self) == False: return
        if self.recived_date.get_date(self) == False: return

        if messagebox.askyesno(self.nametowidget(".").title(),
                               self.nametowidget(".").engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.nametowidget(".").engine.get_update_sql('results', 'result_id')

                args = (*args, self.selected_result[0])

            else:
                sql = self.nametowidget(".").engine.get_insert_sql('results', len(args))

            last_id = self.nametowidget(".").engine.write(sql, args)
            self.parent.set_results()

            if self.index is not None:
                self.parent.lstResults.focus()
                self.parent.lstResults.see(self.index)
                self.parent.lstResults.selection_set(self.index)
            else:
                self.parent.lstResults.see(last_id)
                self.parent.lstResults.selection_set(last_id)

            if self.parent.winfo_name() == "data":
                self.nametowidget(".").nametowidget("biovarase").set_results()
                
                
            self.on_cancel()


    def on_delete(self, evt=None):

        if self.index is not None:
            if messagebox.askyesno(self.nametowidget(".").title(),
                                   self.nametowidget(".").engine.delete,
                                   parent=self) == True:
                sql = "DELETE FROM results WHERE result_id =?"
                args = (self.selected_result[0],)
                self.nametowidget(".").engine.write(sql, args)
                sql = "DELETE FROM rejections WHERE result_id =?"
                args = (self.selected_result[0],)
                self.nametowidget(".").engine.write(sql, args)
                self.parent.set_results()

                if self.parent.winfo_name() == "data":    
                    self.nametowidget(".").nametowidget("biovarase").set_results()
                
                
                    
                    
                    
                self.on_cancel()
            else:
                messagebox.showinfo(self.master.title(),
                                    self.nametowidget(".").engine.abort,
                                    parent=self)

    def get_values(self,):

        return (self.selected_batch[0],
                self.result.get(),
                self.recived_date.get_timestamp(),
                self.enable.get())

    def set_values(self,):

        try:
            self.recived_date.year.set(int(self.selected_result[3].year))
            self.recived_date.month.set(int(self.selected_result[3].month))
            self.recived_date.day.set(int(self.selected_result[3].day))

            t = "{0}:{1}:{0}".format(self.selected_result[3].hour,
                                     self.selected_result[3].minute,
                                     self.selected_result[3].second)

            self.recived_time.set(t)

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print(sys.exc_info()[2])

        self.result.set(self.selected_result[2])
        self.enable.set(self.selected_result[4])

    def on_cancel(self, evt=None):
        self.destroy()

