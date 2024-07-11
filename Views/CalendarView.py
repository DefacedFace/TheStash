import json
import customtkinter as ctk
import agenda
from tkinter import ttk
import datetime
import os


class CalendarView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.calendar = agenda.Agenda(
            self,
            foreground="white",
            background="#1f1f1f",
            headersforeground="#1F6BA5",
            weekendforeground="#ffffff",
            weekendbackground="#2a2a2a",
            font=12,
            bordercolor="#1F6BA5",
        )
        self.update_events()  # Initial loading of events

    def update_events(self):
        try:
            with open("cal_events.json", "r") as f:
                events = json.load(f)

                # Clear existing events to prevent duplicates
                self.calendar.calevent_remove(tag="reminder")

                for event in events:
                    self.calendar.calevent_create(
                        datetime.datetime.strptime(
                            event["taken_at"], "%Y-%m-%d"
                        ).date(),
                        event["substance"],
                        tags=("reminder",),
                    )
        except FileNotFoundError:
            events = []

        style = ttk.Style()
        style.theme_use("clam")

        self.calendar.tag_config("reminder", background="#191970", foreground="white")
        self.calendar.pack(expand=True, fill="both", padx=10, pady=20)
