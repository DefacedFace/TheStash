import customtkinter as ctk
import json
from CTkMessagebox import CTkMessagebox
from CTkTable import CTkTable
from tkcalendar import DateEntry
import datetime
from datepicker import open_datepicker
from views.calendarview import CalendarView
from views.stashview import StashView
from pint import UnitRegistry
import os


class NewPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller, calendar_view, stash_view):
        super().__init__(parent)
        self.current_stash = None
        self.controller = controller
        self.calendar_view = calendar_view
        self._stash_view = stash_view
        self.ureg = UnitRegistry()

        self.stash_frame = ctk.CTkFrame(self, corner_radius=10)
        self.stash_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.stash_title_frame = ctk.CTkFrame(self.stash_frame, corner_radius=10)
        self.stash_title_frame.pack(pady=10, padx=10)

        self.stash_stats_frame = ctk.CTkFrame(self.stash_frame, corner_radius=10)
        self.stash_stats_frame.pack(pady=10, padx=10)

        self.stash_entry_frame = ctk.CTkFrame(self.stash_frame, corner_radius=10)
        self.stash_entry_frame.pack(pady=10, padx=10)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(side=ctk.BOTTOM, fill="x", pady=10)

        self.reup_frame = ctk.CTkFrame(self.stash_frame, corner_radius=10)
        self.reup_frame.pack(
            pady=10,
            padx=10,
        )

        self.reup_title_label = ctk.CTkLabel(
            self.reup_frame,
            font=ctk.CTkFont(size=20),
            text="Add to Stash",
            anchor="n",
        )
        self.reup_title_label.pack(pady=5, padx=10, anchor="n")

        self.reup_unit_label = ctk.CTkLabel(
            self.reup_frame,
            text="Unit",
            font=ctk.CTkFont(size=13),
            anchor="w",
        )
        self.reup_unit_label.pack(pady=5, padx=10, anchor="w")

        self.reup_unit_menu = ctk.CTkOptionMenu(
            self.reup_frame,
            values=["grams", "milligrams", "micrograms", "pounds", "ounces"],
        )
        self.reup_unit_menu.pack(pady=5, padx=10, anchor="w", fill="x")

        self.reup_unit_menu.set("grams")

        self.Reup_amount_label = ctk.CTkLabel(
            self.reup_frame,
            text="Amount",
            font=ctk.CTkFont(size=13),
            anchor="w",
        )
        self.Reup_amount_label.pack(pady=5, padx=10, anchor="w")

        self.Reup_amount = ctk.CTkEntry(
            self.reup_frame,
            placeholder_text="Enter Amount",
            width=500,
        )
        self.Reup_amount.pack(pady=5, padx=10, anchor="w", fill="x")

        self.Reup_button = ctk.CTkButton(
            self.reup_frame,
            text="Update Stash",
        )
        self.Reup_button.pack(pady=5, padx=10, anchor="n")

        home_button = ctk.CTkButton(
            self.button_frame, text="Back", command=lambda: controller.stash_selector()
        )
        home_button.pack(side=ctk.LEFT, padx=10, anchor="sw")

        destroy_button = ctk.CTkButton(
            self.button_frame, text="Delete Stash", command=self.destroy_stash_event
        )
        destroy_button.pack(side=ctk.RIGHT, padx=10, anchor="se")

    def destroy_stash_event(self):
        msg = CTkMessagebox(
            title="Delete Stash?",
            message="Are you sure you want to delete this stash?",
            icon="warning",
            option_1="No",
            option_2="Yes",
            cancel_button_color="transparent",
            justify="center",
        )
        response = msg.get()

        if response == "Yes":
            if self.current_stash:
                try:
                    file_path = "stash.json"
                    if os.path.exists(file_path):
                        with open(file_path, "r") as f:
                            stash_data = json.load(f)

                        for stash in stash_data:
                            if stash["substance"] == self.current_stash["substance"]:
                                stash_data.remove(stash)
                                break

                        with open(file_path, "w") as f:
                            json.dump(stash_data, f, indent=4)

                    self.controller.stash_selector()

                except Exception as e:
                    print(f"Error deleting stash: {e}")
                # self._stash_view.config_stash_data()
        else:
            return

    def open_datepicker(self):
        open_datepicker(self.entry)

    def update_data(self, stash):
        self.current_stash = stash

        for widget in self.stash_title_frame.winfo_children():
            widget.destroy()

        for widget in self.stash_stats_frame.winfo_children():
            widget.destroy()

        for widget in self.stash_entry_frame.winfo_children():
            widget.destroy()
        #
        # for widget in self.Reup_frame.winfo_children():
        #     widget.destroy()

        stash_amount = self.current_stash["stash_amount"]
        stash_unit = self.current_stash["stash_unit"]

        thresholds = {
            "milligrams": 1000,  # 1000 mg = 1 g
            "micrograms": 1000000,  # 1,000,000 µg = 1 g
            "ounces": 16,  # 16 ounces = 1 pound
            "pounds": 1,  # convert to grams if it's a whole pound
        }

        # Check the current amount and convert if needed
        stash_amount_converted = self.ureg.Quantity(stash_amount, stash_unit)

        if stash_unit in thresholds:
            threshold = thresholds[stash_unit]

            if stash_amount < threshold:
                stash_amount_converted = stash_amount_converted.to(self.ureg.grams)
                stash_unit_display = "grams"
            else:
                stash_unit_display = stash_unit
        else:
            stash_unit_display = stash_unit

        if stash_unit_display == "grams":
            stash_amount_display = (
                f"{stash_amount_converted.magnitude:.2f} {stash_unit_display}"
            )
        else:
            stash_amount_display = f"{stash_amount} {stash_unit_display}"

        table_values = [
            ["Stash Amount", "Source Cost", "Total Used"],
            [
                stash_amount_display,
                f"${stash['source_cost']}",
                f"{stash['total_used']}",
            ],
        ]

        stash_usage_title_label = ctk.CTkLabel(
            self.stash_stats_frame,
            font=ctk.CTkFont(size=20),
            text="Stash Usage",
            anchor="n",
        )
        stash_usage_title_label.pack(pady=5, padx=10, anchor="n")

        table = CTkTable(self.stash_stats_frame, row=2, column=3, values=table_values)
        table.pack(pady=10, padx=10, expand=True)

        stash_title_label = ctk.CTkLabel(
            self.stash_title_frame,
            font=ctk.CTkFont(size=20),
            text=f"{stash['substance']}",
        )
        stash_title_label.pack(pady=5, padx=10, anchor="w")

        stash_entry_title = ctk.CTkLabel(
            self.stash_entry_frame,
            text="Add Dose",
            font=ctk.CTkFont(size=20),
            anchor="n",
        )
        stash_entry_title.pack(pady=5, padx=10, anchor="n")

        stash_unit_dose_label = ctk.CTkLabel(
            self.stash_entry_frame,
            text="Dose Unit",
            font=ctk.CTkFont(size=13),
            anchor="sw",
        )
        stash_unit_dose_label.pack(pady=5, padx=10, anchor="w")

        self.stash_unit_menu = ctk.CTkOptionMenu(
            self.stash_entry_frame,
            values=["grams", "milligrams", "micrograms", "pounds", "ounces"],
        )
        self.stash_unit_menu.pack(pady=5, padx=10, anchor="w", fill="x")

        stash_entry_amount_label = ctk.CTkLabel(
            self.stash_entry_frame,
            text="Amount",
            font=ctk.CTkFont(size=13),
            anchor="sw",
        )
        stash_entry_amount_label.pack(pady=5, padx=10, anchor="w")

        self.stash_entry_amount = ctk.CTkEntry(
            self.stash_entry_frame,
            placeholder_text="Enter Amount",
        )
        self.stash_entry_amount.pack(pady=5, padx=10, anchor="w", fill="x")

        stash_roa_label = ctk.CTkLabel(
            self.stash_entry_frame,
            text="ROA",
            font=ctk.CTkFont(size=13),
            anchor="sw",
        )
        stash_roa_label.pack(pady=5, padx=10, anchor="w")

        stash_roa_entry = ctk.CTkOptionMenu(
            self.stash_entry_frame,
            values=["Oral", "Sublingual", "Inhalation", "Intravenous", "Boof"],
        )
        stash_roa_entry.pack(pady=5, padx=10, anchor="w", fill="x")

        stash_notes_label = ctk.CTkLabel(
            self.stash_entry_frame,
            text="Note",
            font=ctk.CTkFont(size=13),
            anchor="sw",
        )
        stash_notes_label.pack(pady=5, padx=10, anchor="w")

        stash_notes_entry = ctk.CTkEntry(
            self.stash_entry_frame,
            placeholder_text="Why are you dosing this substance? What's the purpose?",
            width=500,
        )
        stash_notes_entry.pack(pady=5, padx=10, anchor="w", fill="x")

        stash_taken_date_label = ctk.CTkLabel(
            self.stash_entry_frame,
            text="Taken At",
            font=ctk.CTkFont(size=13),
            anchor="sw",
        )
        stash_taken_date_label.pack(pady=5, padx=10, anchor="w")

        self.entry = ctk.CTkEntry(self.stash_entry_frame)
        self.entry.pack(pady=5, padx=10, anchor="w", fill="x")

        self.open_datepicker_button = ctk.CTkButton(
            self.stash_entry_frame,
            text="Select Date",
            command=self.open_datepicker,
        )
        self.open_datepicker_button.pack(pady=5, padx=10, anchor="w")

        initial_date = datetime.date.today().strftime("%Y-%m-%d")
        self.entry.insert(0, initial_date)

        self.add_entry_button = ctk.CTkButton(
            self.stash_entry_frame, text="Create Entry", command=self.add_entry_event
        )
        self.add_entry_button.pack(pady=5, padx=10, anchor="n")

    def add_entry_event(self):
        date_taken_str = self.entry.get()
        try:
            dose_taken = datetime.datetime.strptime(date_taken_str, "%Y-%m-%d").date()
        except ValueError:
            CTkMessagebox(
                message="Invalid date format. Please use YYYY-MM-DD.",
                icon="warning",
                option_1="OK",
                justify="center",
            )
            return

        # Retrieve and convert the amount
        amount_str = self.stash_entry_amount.get()
        print(f"Amount entered: {amount_str}")
        try:
            amount = float(amount_str)
        except ValueError:
            CTkMessagebox(
                message="Invalid amount. Please enter a numeric value.",
                icon="warning",
                option_1="OK",
                justify="center",
            )
            return

        stash_unit = self.current_stash[
            "stash_unit"
        ]  # Corrected retrieval of stash unit
        print(f"Stash unit: {stash_unit}")  # Debug message

        # Convert the amount to grams for consistency in storage
        try:
            amount_converted = self.ureg.Quantity(amount, stash_unit).to(
                self.ureg.grams
            )
        except Exception as e:
            CTkMessagebox(
                message=f"Error in unit conversion: {e}",
                icon="warning",
                option_1="OK",
                justify="center",
            )
            return

        create_event = {
            "substance": f"{self.current_stash['substance']}",
            "amount": amount_converted.magnitude,
            "unit": "grams",
            "taken_at": dose_taken.isoformat(),
        }

        file_path = "cal_events.json"

        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    events = json.load(f)
            except FileNotFoundError:
                events = []

        events.append(create_event)

        try:
            with open(file_path, "w") as f:
                json.dump(events, f, indent=4)
        except Exception as e:
            print(f"Error saving event: {e}")

        self.amount_calculation(int(amount_converted.magnitude))

        CTkMessagebox(
            title="Stash Updated",
            message="Calendar Event Added.",
            icon="check",
            option_1="Awesome",
            justify="center",
            cancel_button_color="transparent",
        )
        self.calendar_view.update_events()
        def open_datepicker(self):
            open_datepicker(self.entry)


    def amount_calculation(self, entered_amount_grams):
        # Load stash data from file
        if os.path.exists("stash.json"):
            try:
                with open("stash.json", "r") as f:
                    stash_data = json.load(f)
            except FileNotFoundError:
                stash_data = []
        else:
            stash_data = []

        for stash in stash_data:
            if stash["substance"] == self.current_stash["substance"]:
                stash_amount_grams = self.current_stash["stash_amount"]
                new_stash_amount_grams = stash_amount_grams - entered_amount_grams

                if new_stash_amount_grams < 0:
                    new_stash_amount_grams = 0

                total_used = stash.get("total_used", 0)
                new_total_used = total_used + entered_amount_grams

                stash["stash_amount"] = new_stash_amount_grams
                stash["total_used"] = new_total_used

                try:
                    with open("stash.json", "w") as f:
                        json.dump(stash_data, f, indent=4)
                except Exception as e:
                    print(f"Error writing to file: {e}")

                self.update_display(stash)

                break
        else:
            CTkMessagebox(
                title="Error",
                message="Stash not found.",
                cancel_button_color="transparent",
                justify="center",
            )

    def update_display(self, stash):
        for widget in self.stash_stats_frame.winfo_children():
            widget.destroy()

        table_values = [
            ["Stash Amount", "Source Cost", "Total Used"],
            [
                f"{stash['stash_amount']} grams",
                f"${stash['source_cost']}",
                f"{stash['total_used']} grams",
            ],
        ]

        table = CTkTable(self.stash_stats_frame, row=2, column=3, values=table_values)
        table.pack(pady=10, padx=10, expand=True)
