# datepicker.py
import tkinter as tk
from tkinter import Button
import datetime


class DatePicker(tk.Toplevel):
    def __init__(self, master, entry):
        super().__init__(master)
        self.entry = entry
        self.calendar = Calendar(self, self.get_date())
        self.calendar.pack()
        Button(self, text="Select", command=self.on_select).pack()

    def get_date(self):
        try:
            return datetime.datetime.strptime(self.entry.get(), "%Y-%m-%d").date()
        except ValueError:
            return datetime.date.today()

    def on_select(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.calendar.selection.strftime("%Y-%m-%d"))
        self.destroy()


class Calendar(tk.Frame):
    def __init__(self, master, date):
        super().__init__(master)
        self.date = date
        self.selection = date
        self.create_widgets()

    def create_widgets(self):
        self.month_var = tk.IntVar(value=self.date.month)
        self.year_var = tk.IntVar(value=self.date.year)
        self.create_header()
        self.create_body()

    def create_header(self):
        header = tk.Frame(self)
        header.pack()
        prev_button = Button(header, text="<", command=self.prev_month)
        prev_button.pack(side=tk.LEFT)
        self.month_label = tk.Label(header, text=self.date.strftime("%B"))
        self.month_label.pack(side=tk.LEFT)
        self.year_label = tk.Label(header, text=self.date.year)
        self.year_label.pack(side=tk.LEFT)
        next_button = Button(header, text=">", command=self.next_month)
        next_button.pack(side=tk.LEFT)

    def create_body(self):
        self.body = tk.Frame(self)
        self.body.pack()
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for idx, day in enumerate(days):
            tk.Label(self.body, text=day).grid(row=0, column=idx)
        self.day_buttons = []
        for row in range(1, 7):
            for col in range(7):
                day_button = Button(
                    self.body,
                    text="",
                    width=3,
                    command=lambda r=row, c=col: self.select_day(r, c),
                )
                day_button.grid(row=row, column=col)
                self.day_buttons.append(day_button)
        self.update_calendar()

    def update_calendar(self):
        year, month = self.year_var.get(), self.month_var.get()
        first_day = datetime.date(year, month, 1)
        start_day = first_day.weekday()
        if start_day == 6:
            start_day = 0
        else:
            start_day += 1
        days_in_month = (
            (datetime.date(year, month + 1, 1) - datetime.date(year, month, 1)).days
            if month < 12
            else 31
        )
        for i, day_button in enumerate(self.day_buttons):
            if i < start_day or i >= start_day + days_in_month:
                day_button.config(text="", state=tk.DISABLED)
            else:
                day_button.config(text=str(i - start_day + 1), state=tk.NORMAL)

    def prev_month(self):
        self.date = self.date.replace(day=1) - datetime.timedelta(days=1)
        self.month_var.set(self.date.month)
        self.year_var.set(self.date.year)
        self.update_calendar()
        self.month_label.config(text=self.date.strftime("%B"))
        self.year_label.config(text=self.date.year)

    def next_month(self):
        self.date = self.date.replace(day=28) + datetime.timedelta(days=4)
        self.date = self.date.replace(day=1)
        self.month_var.set(self.date.month)
        self.year_var.set(self.date.year)
        self.update_calendar()
        self.month_label.config(text=self.date.strftime("%B"))
        self.year_label.config(text=self.date.year)

    def select_day(self, row, col):
        day = int(self.day_buttons[(row - 1) * 7 + col].cget("text"))
        self.selection = self.date.replace(day=day)
        self.master.on_select()


def open_datepicker(entry):
    DatePicker(entry.master, entry)
