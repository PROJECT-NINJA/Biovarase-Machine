# -*- coding: utf-8 -*-
""" This is the main module of Biovarase."""
import sys
import inspect
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as nav_tool
except:
    from matplotlib.backends.backend_tkagg import  NavigationToolbar2TkAgg as nav_tool

import matplotlib.ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib.figure import Figure
from matplotlib import gridspec

from engine import Engine

import frames.license
import frames.tests
import frames.batch
import frames.data
import frames.units
import frames.actions
import frames.rejections
import frames.result
import frames.analytical
import frames.export_rejections
import frames.plots
import frames.youden
import frames.elements
import frames.tea
import frames.analytical_goals
import frames.counts
import frames.zscore
import frames.set_zscore
import frames.quick_data_analysis


class Biovarase(ttk.Frame):

    def __init__(self, parent):
        super().__init__(name="biovarase")

        self.parent = parent
        self.status_bar_text = tk.StringVar()
        self.average = tk.DoubleVar()
        self.bias = tk.DoubleVar()
        self.westgard = tk.StringVar()
        self.calculated_sd = tk.DoubleVar()
        self.cva = tk.DoubleVar()
        self.range = tk.DoubleVar()
        self.elements = tk.IntVar()
        self.target = tk.DoubleVar()
        self.sd = tk.DoubleVar()
        self.expiration = tk.StringVar()
        self.te = tk.DoubleVar()
        self.ddof = tk.IntVar()
        self.show_error_bar = tk.IntVar()
        self.zscore = tk.DoubleVar()
        self.enable_rejections = tk.BooleanVar()

        self.set_style()
        self.init_menu()
        self.init_ui()
        self.init_status_bar()
        self.center_ui()

    def set_style(self):

        s = ttk.Style()

        s.configure('Target.TLabel',
                    foreground=self.nametowidget(".").engine.get_rgb(255, 69, 0),
                    background=self.nametowidget(".").engine.get_rgb(255, 255, 255))

        ##1966BC Color Hex  (25,102,188)
        s.configure('Average.TLabel',
                    foreground=self.nametowidget(".").engine.get_rgb(25, 102, 188),
                    background=self.nametowidget(".").engine.get_rgb(255, 255, 255))

        s.configure('westgard_violation.TLabel',
                    background=self.nametowidget(".").engine.get_rgb(255, 106, 106),)

        s.configure('westgard_ok.TLabel',
                    background=self.nametowidget(".").engine.get_rgb(152, 251, 152))

        s.configure('Statusbar.TLabel',
                    foreground='blue',)

        s.configure('black_and_withe.TLabel',
                    background=self.nametowidget(".").engine.get_rgb(255, 255, 255),
                    foreground=self.nametowidget(".").engine.get_rgb(77, 77, 77),)

    def center_ui(self):

        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        # calculate position x, y
        d = self.nametowidget(".").engine.get_dimensions()
        w = int(d['w'])
        h = int(d['h'])
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def init_menu(self):

        m_main = tk.Menu(self, bd=1)

        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        s_menu = tk.Menu(m_file)
        s_databases = tk.Menu(m_file)
        m_edit = tk.Menu(m_main, tearoff=0, bd=1)
        m_batches = tk.Menu(m_main, tearoff=0, bd=1)
        m_results = tk.Menu(m_main, tearoff=0, bd=1)
        m_about = tk.Menu(m_main, tearoff=0, bd=1)

        m_main.add_cascade(label="File", underline=0, menu=m_file)
        m_main.add_cascade(label="Edit", underline=0, menu=m_edit)
        m_main.add_cascade(label="Batches", underline=0, menu=m_batches)
        m_main.add_cascade(label="Results", underline=0, menu=m_results)
        m_main.add_cascade(label="?", underline=0, menu=m_about)


        #m_file.add_separator()

        m_file.add_cascade(label="Database", menu=s_databases, underline=0)
        s_databases.add_command(label="Dump",
                                underline=0,
                                command=self.on_dump)

        s_databases.add_command(label="Vacuum",
                                underline=0,
                                command=self.on_vacuum)

        s_databases.add_command(label="Reset database",
                                underline=6,
                                command=self.on_reset_database)


        items = (("Plots", self.on_plots),
                 ("Youden", self.on_youden),
                 ("Tea", self.on_tea),
                 ("Reset", self.on_reset),
                 ("Analytica", self.on_analitical),
                 ("Z Score", self.on_zscore),)

        for i in items:
            m_file.add_command(label=i[0], underline=0, command=i[1])

        #keep this here
        m_file.add_cascade(label='Export', menu=s_menu, underline=0)

        items = (("Quick Data Analysis", self.on_quick_data_analysis),
                 ("Rejections", self.on_export_rejections),
                 ("Analytical Goals", self.on_analytical_goals),
                 ("Counts", self.on_export_counts),)

        for i in items:
            s_menu.add_command(label=i[0], underline=0, command=i[1])

        m_file.add_separator()
        m_file.add_command(label="Log", underline=0, command=self.on_log)
        m_file.add_command(label="Exit", underline=0, command=self.parent.on_exit)

        items = (("Tests", self.on_tests),
                 ("Data", self.on_data),
                 ("Units", self.on_units),
                 ("Actions", self.on_actions),
                 ("Set Elements", self.on_elements),
                 ("Set Z Score", self.on_set_zscore),)

        for i in items:
            m_edit.add_command(label=i[0], underline=0, command=i[1])

        
        items = (("Add batch", self.on_add_batch),
                 ("Update batch", self.on_update_batch))

        for i in items:
            m_batches.add_command(label=i[0], underline=0, command=i[1])

        items = (("Add result", self.on_add_result),
                 ("Update result", self.on_update_result))

        for i in items:
            m_results.add_command(label=i[0], underline=0, command=i[1])

        m_about.add_command(label="About", underline=0, command=self.on_about)
        m_about.add_command(label="License", underline=0, command=self.on_license)
        m_about.add_command(label="Python", underline=0, command=self.on_python_version)
        m_about.add_command(label="Tkinter", underline=0, command=self.on_tkinter_version)

        self.parent.config(menu=m_main)

    def init_ui(self):

        f0 = self.nametowidget(".").engine.get_frame(self, 8)
        f1 = ttk.Frame(f0,)

        ttk.Label(f1, text='Tests').pack(side=tk.TOP, fill=tk.X, expand=0)
        #self.cbTests =  ttk.Combobox(f1,state='readonly')
        self.cbTests = ttk.Combobox(f1,)
        self.cbTests.bind("<<ComboboxSelected>>", self.on_selected_test)
        self.cbTests.pack(side=tk.TOP, fill=tk.X, pady=5, expand=0)

        w = ttk.LabelFrame(f1, text='Batches')
        self.lstBatches = self.nametowidget(".").engine.get_listbox(w, height=5)
        self.lstBatches.selectmode=tk.MULTIPLE
        self.lstBatches.bind("<<ListboxSelect>>", self.on_selected_batch)
        self.lstBatches.bind('<Double-Button-1>', self.on_update_batch)
        w.pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        f2 = ttk.Frame(f1,)
        
        w = tk.LabelFrame(f2, text='Batch data', font=self.nametowidget(".").engine.set_font("Helvetica", 10, "bold"))

        ttk.Label(w, text="Target").pack()
        ttk.Label(w,
                  style='Target.TLabel',
                  anchor=tk.CENTER,
                  textvariable=self.target).pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(w, text="SD").pack()
        ttk.Label(w,
                  style='black_and_withe.TLabel',
                  anchor=tk.CENTER,
                  textvariable=self.sd).pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(w, text="TE%").pack()
        ttk.Label(w, style='black_and_withe.TLabel',
                  anchor=tk.CENTER, textvariable=self.te).pack(fill=tk.X, padx=2, pady=2)

        w.pack(side=tk.LEFT, fill=tk.X, expand=0)

        w = tk.LabelFrame(f2, text='Cal data', font=self.nametowidget(".").engine.set_font("Helvetica", 10, "bold"))

        ttk.Label(w, text="Average").pack()
        ttk.Label(w, style='Average.TLabel', anchor=tk.CENTER,
                  textvariable=self.average).pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(w, text="sd").pack()
        ttk.Label(w, style='black_and_withe.TLabel', anchor=tk.CENTER,
                  textvariable=self.calculated_sd).pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(w, text="CV%").pack()
        ttk.Label(w, style='black_and_withe.TLabel', anchor=tk.CENTER,
                  textvariable=self.cva).pack(fill=tk.X, padx=2, pady=2)

        w.pack(side=tk.LEFT, fill=tk.X, expand=0)

        w = tk.LabelFrame(f2, text='Other data', font=self.nametowidget(".").engine.set_font("Helvetica", 10, "bold"))

        ttk.Label(w, text="Westgard").pack()

        self.lblWestgard = ttk.Label(w,
                                     style='black_and_withe.TLabel',
                                     anchor=tk.CENTER,
                                     textvariable=self.westgard)
        self.lblWestgard.pack(fill=tk.X, padx=2, pady=2)

        ttk.Label(w, text="Range").pack()
        ttk.Label(w, style='black_and_withe.TLabel',
                  anchor=tk.CENTER,
                  textvariable=self.range).pack(fill=tk.X, padx=2, pady=2)

        ttk.Label(w, text="Bias%").pack()
        ttk.Label(w,
                  style='black_and_withe.TLabel',
                  anchor=tk.CENTER,
                  textvariable=self.bias).pack(fill=tk.X, padx=2, pady=2)

        w.pack(side=tk.RIGHT, fill=tk.X, expand=0)

        w = ttk.LabelFrame(f1, text='Results')
        self.lstResults = self.nametowidget(".").engine.get_listbox(w,)
        self.lstResults.bind("<<ListboxSelect>>", self.on_selected_result)
        self.lstResults.bind('<Double-Button-1>', self.on_update_result)
        w.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        #create graph!
        f3 = ttk.Frame(f0,)
        #Figure: The top level container for all the plot elements.
        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        fig = Figure()
        #fig.suptitle(self.engine.title, fontsize=16)
        fig.subplots_adjust(bottom=0.10, right=0.96, left=0.08, top=0.95, wspace=0.10)
        self.lj = fig.add_subplot(gs[0], facecolor=('xkcd:light grey'))
        self.frq = fig.add_subplot(gs[1], facecolor=('xkcd:light grey'))
        self.canvas = FigureCanvasTkAgg(fig, f3)
        toolbar = nav_tool(self.canvas, f3)
        toolbar.update()
        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)
        
        f0.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        f1.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        f2.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        f3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    
    def init_status_bar(self):

        f = self.nametowidget(".").engine.set_font("TkDefaultFont", 12, "bold")

        self.status_bar_text.set("Ready Player One!")

        w = ttk.Frame(self,)

        self.status = ttk.Label(w, font=f,
                                textvariable=self.status_bar_text,
                                relief=tk.FLAT,
                                style='Statusbar.TLabel',
                                anchor=tk.W)

        ttk.Label(w, font=f,
                  textvariable=self.elements,
                  relief=tk.FLAT,
                  anchor=tk.W).pack(side=tk.RIGHT, fill=tk.X)
        ttk.Label(w, text="Elements").pack(side=tk.RIGHT, fill=tk.X)


        ttk.Label(w, font=f,
                  textvariable=self.zscore,
                  relief=tk.FLAT,
                  anchor=tk.W).pack(side=tk.RIGHT, fill=tk.X)
        ttk.Label(w, text="Z Score").pack(side=tk.RIGHT, fill=tk.X)

        ttk.Checkbutton(w,
                        text="Enable Rejections",
                        onvalue=1,
                        offvalue=0,
                        variable=self.enable_rejections,).pack(side=tk.RIGHT, fill=tk.X)

        ttk.Checkbutton(w,
                        text="Show Error Bar",
                        onvalue=1,
                        offvalue=0,
                        variable=self.show_error_bar,
                        command=self.on_show_error_bar).pack(side=tk.RIGHT, fill=tk.X)

        ttk.Checkbutton(w,
                        text="Delta Degree of Freedom",
                        onvalue=1,
                        offvalue=0,
                        variable=self.ddof,
                        command=self.on_ddof).pack(side=tk.RIGHT, fill=tk.X)


        self.status.pack(side=tk.LEFT, fill=tk.X, expand=1)

        w.pack(side=tk.BOTTOM, fill=tk.X)

    def on_open(self):

        self.elements.set(self.nametowidget(".").engine.get_elements())
        self.set_tests()
        self.enable_rejections.set(False)
        self.ddof.set(self.nametowidget(".").engine.get_ddof())
        self.show_error_bar.set(self.nametowidget(".").engine.get_show_error_bar())
        self.set_zscore()

    def set_elements(self):
        self.elements.set(self.nametowidget(".").engine.get_elements())

    def set_zscore(self):
        self.zscore.set(self.nametowidget(".").engine.get_zscore())

    def on_reset(self):

        self.cbTests.set('')
        self.lstBatches.delete(0, tk.END)
        self.lstResults.delete(0, tk.END)
        self.set_elements()
        self.set_tests()
        self.reset_batch_data()
        self.reset_cal_data()
        self.reset_graph()

    def reset_graph(self):

        self.lj.clear()
        self.frq.clear()
        self.lj.grid(True)
        self.frq.grid(True)
        self.canvas.draw()

    def reset_batch_data(self):

        self.expiration.set("")
        self.target.set(0)
        self.sd.set(0)

    def reset_cal_data(self):

        self.average.set(0)
        self.calculated_sd.set(0)
        self.cva.set(0)
        self.bias.set(0)
        self.range.set(0)
        self.te.set(0)
        self.westgard.set("")
        self.set_westgard_alarm()

    def set_batch_data(self):

        self.expiration.set(self.selected_batch[3])
        self.target.set(self.selected_batch[4])
        self.sd.set(self.selected_batch[5])

    def set_calculated_data(self, mean, sd, cv, bias, crange):

        self.average.set(mean)
        self.calculated_sd.set(sd)
        self.cva.set(cv)
        self.bias.set(bias)
        self.range.set(crange)

        if self.target.get() != 0:
            et = self.nametowidget(".").engine.get_te(self.target.get(), self.average.get(), self.cva.get())
            self.te.set(et)
        else:
            self.te.set(0)

    def set_westgard(self, series):

        if len(series) > 9:
            rule = self.nametowidget(".").engine.get_westgard_violation_rule(self.selected_batch[4],
                                                           self.selected_batch[5],
                                                           series)
        else:
            rule = "No data"

        self.westgard.set(rule)
        self.set_westgard_alarm()

    def set_westgard_alarm(self):

        if self.westgard.get() == "Accept":
            self.lblWestgard.configure(style='westgard_ok.TLabel',)
        elif self.westgard.get() in("No Data", ""):
            self.lblWestgard.configure(style='black_and_withe.TLabel',)
        else:
            self.lblWestgard.configure(style='westgard_violation.TLabel',)


    def set_tests(self):

        index = 0
        self.dict_tests = {}
        voices = []

        sql = "SELECT tests.test_id,tests.test||' '||samples.sample\
               FROM tests\
               INNER JOIN samples ON tests.sample_id = samples.sample_id\
               WHERE tests.enable=1\
               ORDER BY tests.test"

        rs = self.nametowidget(".").engine.read(True, sql, ())

        for i in rs:
            self.dict_tests[index] = i[0]
            index += 1
            voices.append(i[1])

        self.cbTests['values'] = voices
        self.reset_batch_data()

    def set_batches(self):

        self.lstBatches.delete(0, tk.END)
        self.lstResults.delete(0, tk.END)

        index = 0
        self.dict_batchs = {}
        sql = "SELECT * FROM lst_batches WHERE test_id = ?"
      
        rs = self.nametowidget(".").engine.read(True, sql, (self.selected_test[0],))
        
        if rs:
            
            for i in rs:
                
                x = self.nametowidget(".").engine.get_expiration_date(i[2])
                s = "{0:12} {1}".format(i[1], i[2])
                self.lstBatches.insert(tk.END, (s))
                
                if x <= 0:
                    self.lstBatches.itemconfig(index, {"bg":"red"})
                elif x <= 15:
                    self.lstBatches.itemconfig(index, {"bg":"yellow"})
                    
                self.dict_batchs[index] = i[0]
                index += 1

            self.lstBatches.select_set(0)
            self.lstBatches.event_generate("<<ListboxSelect>>")
        else:

            self.reset_cal_data()
            self.reset_graph()

    def set_results(self,):

        try:
            if self.lstBatches.curselection():
                
                self.lstResults.delete(0, tk.END)
                index = 0
                self.dict_results = {}

                sql = "SELECT * FROM lst_results WHERE batch_id =? LIMIT?"
                rs = self.nametowidget(".").engine.read(True, sql, (self.selected_batch[0], int(self.elements.get())))

                target = float(self.selected_batch[4])
                sd = float(self.selected_batch[5])

                if rs:

                    for i in rs:

                        s = "{0}{1:12}".format(i[2], i[1])
                        self.lstResults.insert(tk.END, s)

                        result = float(round(i[1], 2))

                        is_enabled = i[4]

                        self.set_results_row_color(index, result, is_enabled, target, sd)

                        self.dict_results[index] = i[0]

                        index += 1

                    self.get_values(rs)

                else:
                    self.reset_cal_data()
                    self.reset_graph()

        except:
            print(self, inspect.stack()[0][3], sys.exc_info()[1],
                  sys.exc_info()[0], sys.modules[__name__])


    def on_selected_test(self, event):

        if self.cbTests.current() != -1:
            index = self.cbTests.current()
            pk = self.dict_tests[index]
            self.selected_test = self.nametowidget(".").engine.get_selected("lst_tests", "test_id", pk)
            self.reset_batch_data()
            self.reset_cal_data()
            self.set_batches()

    def on_selected_batch(self, event):

        if self.lstBatches.curselection():

            index = self.lstBatches.curselection()[0]
            pk = self.dict_batchs.get(index)
            self.selected_batch = self.nametowidget(".").engine.get_selected("batches", "batch_id", pk)

            self.set_batch_data()
            self.set_results()

    def on_selected_result(self, event):

        if self.lstResults.curselection():

            index = self.lstResults.curselection()[0]
            pk = self.dict_results.get(index)
            self.selected_result = self.nametowidget(".").engine.get_selected("results", "result_id", pk)

    def on_update_result(self, event=None):

        if self.lstResults.curselection():

            index = self.lstResults.curselection()[0]

            if self.enable_rejections.get() == False:
                obj = frames.result.UI(self, index)
            else:
                obj = frames.rejections.UI(self)

            obj.on_open(self.selected_test,
                        self.selected_batch,
                        self.selected_result)

        else:
            msg = "Attention please.\nSelect a result."
            messagebox.showinfo(self.parent.title(), msg, parent=self)

    def set_results_row_color(self, index, result, is_enabled, target, sd):

        if is_enabled == 0:
            self.lstResults.itemconfig(index, {"bg":"light gray"})
        else:
            d = {}
            if result >= target:
                #result > 3sd
                if result >= (target + (sd*3)):
                    d["bg"] = "red"
                #if result is > 2sd and < +3sd
                elif result >= (target + (sd*2)) and result <= (target + (sd*3)):
                    d["bg"] = "yellow"

            elif result <= target:
                #result < 3sd
                if result <= (target - (sd*3)):
                    d["bg"] = "red"
                #if result is > -2sd and < -3sd
                elif result <= (target - (sd*2)) and result >= (target - (sd*3)):
                    d["bg"] = "yellow"

            self.lstResults.itemconfig(index, d)

    def get_um(self,):

        sql = "SELECT unit FROM lst_tests WHERE test_id =?"
        return self.nametowidget(".").engine.read(False, sql, (self.selected_test[0],))


    def get_values(self, rs):

        target = self.selected_batch[4]
        sd = self.selected_batch[5]
        series = self.nametowidget(".").engine.get_series(self.selected_batch[0], int(self.nametowidget(".").engine.get_elements()))
        mean = self.nametowidget(".").engine.get_mean(series)
        cv = self.nametowidget(".").engine.get_cv(series)
        bias = self.nametowidget(".").engine.get_bias(mean, target)
        crange = self.nametowidget(".").engine.get_range(series)
        x_labels = self.get_x_labels(rs)
        computed_sd = self.nametowidget(".").engine.get_sd(series)
        self.set_calculated_data(mean, computed_sd, cv, bias, crange)
        self.set_westgard(series)

        self.set_lj(len(rs), target, sd, series,
                    len(series), mean, computed_sd,
                    cv, x_labels[0], x_labels[1],)

        self.set_histogram(series, target, mean,)

        self.canvas.draw()


    def get_x_labels(self, rs):

        x_labels = []
        dates = []

        rs = tuple(i for i in rs if i[4] != 0)

        if rs:
            for i in reversed(rs):
                x_labels.append(i[2])
                dates.append(i[3])

        return (x_labels, dates)



    def set_lj(self, count_rs, target, sd, series, count_series,
               compute_average, compute_sd, compute_cv, x_labels, dates):

        if self.nametowidget(".").engine.get_show_error_bar() != 0:
            show_error_bar = True
            et = self.nametowidget(".").engine.get_te(target, compute_average, compute_cv)
        else:
            show_error_bar = False

        self.lj.clear()
        self.lj.grid(True)
        um = self.get_um()
        lines = ([], [], [], [], [], [], [])

        for i in range(len(series)+1):

            lines[0].append(target + (sd*3))
            lines[1].append(target + (sd*2))
            lines[2].append(target + sd)

            lines[3].append(target)

            lines[4].append(target - sd)
            lines[5].append(target - (sd*2))
            lines[6].append(target - (sd*3))

        #it's show time
        self.lj.set_xticks(range(0, len(series)+1))
        self.lj.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(21))
        self.lj.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        self.lj.set_xticklabels(x_labels, rotation=70, size=6)
        self.lj.plot(series, marker="8", label="data")

        for x, y in enumerate(series):
            self.lj.text(x, y, str(y),)
            if show_error_bar:
                self.lj.errorbar(x, y, yerr=self.nametowidget(".").engine.percentage(et, y),
                                 uplims=True, lolims=True, ecolor="green")


        self.lj.plot(lines[0], color="red", label="+3 sd", linestyle="--")
        self.lj.plot(lines[1], color="yellow", label="+2 sd", linestyle="--")
        self.lj.plot(lines[2], color="green", label="+1 sd", linestyle="--")
        self.lj.plot(lines[3], label='target', linewidth=2)
        self.lj.plot(lines[4], color="green", label="-1 sd", linestyle="--")
        self.lj.plot(lines[5], color="yellow", label="-2 sd", linestyle="--")
        self.lj.plot(lines[6], color="red", label="-3 sd", linestyle="--")

        if um is  not None:
            self.lj.set_ylabel(str(um[0]))
        else:
            self.lj.set_ylabel("No unit assigned yet")


        s = "{0} {1}".format(self.selected_test[1], self.selected_batch[2],)

        self.lj.set_title(s, weight="bold", loc="center")


        bottom_text = ("from %s to %s"%(dates[0].strftime("%Y-%m-%d"),
                                        dates[-1].strftime("%Y-%m-%d")),
                       count_series, count_rs)

        self.lj.text(0.95, 0.01,
                     '%s computed %s on %s results'%bottom_text,
                     verticalalignment='bottom',
                     horizontalalignment='right',
                     transform=self.lj.transAxes,
                     color='black',
                     weight='bold')



    def set_histogram(self, series, target, avg):

        #histogram of frequency distribuition
        self.frq.clear()
        self.frq.grid(True)
        self.frq.hist(series, color="g")
        self.frq.axvline(target, color="orange", linewidth=2)
        self.frq.axvline(avg, color="b", linewidth=2)
        self.frq.set_ylabel('Results Frequency')
        self.frq.yaxis.set_label_position("right")
        um = self.get_um()
        if um is  not None:
            self.frq.set_xlabel(str(um[0]))
        else:
            self.frq.set_xlabel("No unit assigned yet")

    def on_ddof(self,):

        if self.ddof.get() == True:
            self.nametowidget(".").engine.set_ddof(1)
        else:
            self.nametowidget(".").engine.set_ddof(0)

        self.ddof.set(self.nametowidget(".").engine.get_ddof())

        self.set_results()

    def on_show_error_bar(self,):

        if self.show_error_bar.get() == True:
            self.nametowidget(".").engine.set_show_error_bar(1)
        else:
            self.nametowidget(".").engine.set_show_error_bar(0)

        self.show_error_bar.set(self.nametowidget(".").engine.get_show_error_bar())

        self.set_results()

    def on_analytical_goals(self):
        frames.analytical_goals.UI(self).on_open()

    def on_tests(self,):
        frames.tests.UI(self).on_open()

    def on_units(self,):
        frames.units.UI(self).on_open()

    def on_elements(self,):
        frames.elements.UI(self).on_open()

    def on_set_zscore(self,):
        frames.set_zscore.UI(self).on_open()

    def on_zscore(self,):
        frames.zscore.UI(self).on_open()

    def on_data(self,):
        frames.data.UI(self).on_open()

    def on_actions(self,):
        frames.actions.UI(self).on_open()

    def on_analitical(self,):
        frames.analytical.UI(self).on_open()

    def on_quick_data_analysis(self,):
        frames.quick_data_analysis.UI(self).on_open()

    def on_export_rejections(self,):
        frames.export_rejections.UI(self).on_open()

    def on_export_counts(self,):
        frames.counts.UI(self).on_open()

    def on_plots(self,):

        if self.cbTests.current() != -1:
            index = self.cbTests.current()
            pk = self.dict_tests[index]
            selected_test = self.nametowidget(".").engine.get_selected("tests", "test_id", pk)
            frames.plots.UI(self).on_open(selected_test)
        else:
            msg = "Not enough data to plot.\nSelect a test."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

    def on_youden(self,):

        if self.cbTests.current() != -1:
            index = self.cbTests.current()
            pk = self.dict_tests[index]
            selected_test = self.nametowidget(".").engine.get_selected("tests", "test_id", pk)
            items = self.lstBatches.curselection()
            
            pks = []
            batches = []

            if len(items)==2:

                for index in items:
                    pk = self.dict_batchs.get(index)
                    pks.append(pk)

                for pk in pks:
                    batch = self.nametowidget(".").engine.get_selected("batches", "batch_id", pk)
                    batches.append(batch)

                sql = "SELECT * FROM lst_results WHERE batch_id = ? LIMIT ?"
        
                data = []
                
                for batch in batches:
                    rs = self.nametowidget(".").engine.read(True, sql, ((batch[0], int(self.nametowidget(".").engine.get_elements()))))
                    series = self.nametowidget(".").engine.get_series(batch[0], int(self.nametowidget(".").engine.get_elements()))
                    data.append(series)

                if len(data[0]) != len(data[1]):
                    msg = "Selected batches data have diffen size.\nIt's impossible to draw Youden plot."
                    messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

                else:
                    frames.youden.UI(self).on_open(selected_test, batches, data)

            else:
                msg = "Not data to plot a Youden chart.\nYou need to select at least two batches."
                messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)                
        else:
            msg = "Not enough data to plot.\nSelect a test."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)
            

    def on_tea(self,):

        if self.cbTests.current() != -1:
            index = self.cbTests.current()
            pk = self.dict_tests[index]
            selected_test = self.nametowidget(".").engine.get_selected("tests", "test_id", pk)
            frames.tea.UI(self).on_open(selected_test)
        else:
            msg = "Not enough data to plot.\nSelect a test."
            messagebox.showwarning(self.nametowidget(".").title(), msg, parent=self)

    def on_add_batch(self):

        if self.cbTests.current() != -1:
            obj = frames.batch.UI(self)
            obj.on_open(self.selected_test)

        else:
            msg = "Attention please.\nBefore add a batch you must select a test."
            messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

    def on_update_batch(self, evt=None):

        if self.lstBatches.curselection():
            index = self.lstBatches.curselection()[0]
            obj = frames.batch.UI(self, index)
            obj.on_open(self.selected_test, self.selected_batch)
        else:
            msg = "Attention please.\nSelect a batch."
            messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

    def on_add_result(self,):

        if self.lstBatches.curselection():
            obj = frames.result.UI(self)
            obj.on_open(self.selected_test, self.selected_batch)
        else:
            msg = "Attention please.\nBefore add a result you must select a batch."
            messagebox.showinfo(self.nametowidget(".").title(), msg, parent=self)

    def on_dump(self):
        self.nametowidget(".").engine.dump_db()
        messagebox.showinfo(self.nametowidget(".").title(), "Dump executed.", parent=self)

    def on_vacuum(self):
        sql = "VACUUM;"
        self.nametowidget(".").engine.write(sql)
        messagebox.showinfo(self.nametowidget(".").title(), "Vacuum executed.", parent=self)

    def on_reset_database(self, evt=None):

        msg = "You are about to delete the entire database.\nAre you sure? "

        if messagebox.askyesno(self.master.title(), msg, default='no', parent=self) == True:

            try:
                self.nametowidget(".").nametowidget("data").on_cancel()
                self.nametowidget(".").nametowidget("tests").on_cancel()
                self.nametowidget(".").nametowidget("rejections").on_cancel()
            except:
                pass

            self.nametowidget(".").engine.dump_db()

            sql = ("DELETE FROM tests",
                   "DELETE FROM batches",
                   "DELETE FROM results",
                   "DELETE FROM rejections",)

            for statement in sql:
                self.nametowidget(".").engine.write(statement, ())

            self.on_reset()
        else:
            messagebox.showinfo(self.master.title(), self.nametowidget(".").engine.abort, parent=self)        

    def on_log(self,):
        self.nametowidget(".").engine.get_log_file()

    def on_license(self):
        frames.license.UI(self).on_open()

    def on_python_version(self):
        s = self.nametowidget(".").engine.get_python_version()
        messagebox.showinfo(self.nametowidget(".").title(), s, parent=self)

    def on_tkinter_version(self):
        s = "Tkinter patchlevel\n{0}".format(self.nametowidget(".").tk.call("info", "patchlevel"))
        messagebox.showinfo(self.nametowidget(".").title(), s, parent=self)        


    def on_about(self,):
        messagebox.showinfo(self.nametowidget(".").title(),
                            self.nametowidget(".").info,
                            parent=self)

class App(tk.Tk):
    """Biovarase Main Application start here"""
    def __init__(self):
        super().__init__()

        self.engine = Engine()
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.set_style()
        self.set_title("Biovarase")
        self.set_icon()
        self.set_info()
        self.engine.title = self.title()
        
        w = Biovarase(self)
        w.on_open()
        w.pack(fill=tk.BOTH, expand=1)

    def set_title(self, title):
        s = "{0}".format(title)
        self.title(s)

    def set_info(self,):
        msg = "{0}\nauthor: {1}\ncopyright: {2}\ncredits: {3}\nlicense: {4}\nversion: {5}\
               \nmaintainer: {6}\nemail: {7}\ndate: {8}\nstatus: {9}"
        info = msg.format(self.title(), __author__, __copyright__, __credits__, __license__, __version__, __maintainer__, __email__, __date__, __status__)
        self.info = info                

    def set_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=self.engine.get_rgb(240, 240, 237))

    def set_icon(self):
        icon = tk.PhotoImage(data=self.engine.get_icon())
        self.call("wm", "iconphoto", self._w, "-default", icon)

    def on_exit(self):
        """Close all"""
        if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
            self.engine.con.close()
            self.quit()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
