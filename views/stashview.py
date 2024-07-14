import customtkinter as ctk
import os
import json
from functools import partial
from pint import UnitRegistry


class StashView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.ureg = UnitRegistry()
        self.stash_data = []
        self.config_stash_data()

    def config_stash_data(self):
        file_path = "stash.json"

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                with open(file_path, "r") as f:
                    self.stash_data = json.load(f)
            except json.JSONDecodeError:
                self.stash_data = []
        else:
            self.stash_data = []
        self.update_ui()

    def update_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        if len(self.stash_data) == 0:
            empty_frame = ctk.CTkFrame(self)
            empty_frame.pack(expand=True, padx=20, pady=300, fill="x")
            empty_label = ctk.CTkLabel(
                empty_frame,
                text="Empty Stash \n Click the Add Stash button to add a new stash entry",
                font=ctk.CTkFont(size=20),
            )
            empty_label.pack(padx=20, pady=20, fill="x")
            return
        else:
            for stash in self.stash_data:
                drug_frame = ctk.CTkFrame(self, corner_radius=10, width=500, height=70)
                drug_frame.pack(expand=True, padx=20, pady=10, fill="x")

                substance_label = ctk.CTkLabel(
                    drug_frame,
                    text=f"{stash['substance']}",
                    font=ctk.CTkFont(size=20),
                    anchor="center",
                    pady=20,
                )
                substance_label.place(relx=0, rely=0, x=20, y=5)

                drug_class_label = ctk.CTkLabel(
                    drug_frame,
                    text=f"{stash['drug_class']}",
                    font=ctk.CTkFont(size=15),
                    anchor="w",
                    width=200,
                )
                drug_class_label.place(relx=1.0, rely=0, anchor="ne", x=-70, y=5)

                # Convert the amount back to the original unit for display
                stash_amount_quantity = self.ureg.Quantity(
                    stash["stash_amount"], "grams"
                )
                stash_amount_converted = stash_amount_quantity.to(stash["stash_unit"])
                amount = f"{stash_amount_converted.magnitude:.2f}"

                amount_label = ctk.CTkLabel(
                    drug_frame,
                    text=f"{amount} {stash['stash_unit']}",
                    font=ctk.CTkFont(size=15),
                    anchor="w",
                    width=200,
                )
                amount_label.place(relx=1.0, rely=0, anchor="ne", x=-70, y=30)

                stash_button = ctk.CTkButton(
                    drug_frame,
                    text="Stash",
                    command=partial(self.go_to_new_page, stash),
                    width=80,
                )
                stash_button.pack(padx=20, pady=20, anchor="e")

    def go_to_new_page(self, stash):
        self.controller.new_page_selector(stash)
