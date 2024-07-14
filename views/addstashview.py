
import customtkinter as ctk
from drugtypes import drugtypes
from pint import UnitRegistry
import json
import os
import uuid
from CTkMessagebox import CTkMessagebox


class AddStashView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.ureg = UnitRegistry()

        frame = ctk.CTkFrame(self, width=500, height=500, corner_radius=10)
        frame.pack(padx=10, pady=20, fill="x")

        drug_class_frame = ctk.CTkFrame(frame)
        drug_class_frame.pack(padx=100, pady=(20, 10), fill="x")

        Drug_label = ctk.CTkLabel(
            drug_class_frame, text="Drug Class", anchor="w", font=ctk.CTkFont(size=30)
        )
        Drug_label.pack(padx=20, pady=10, anchor="n")

        def optionmenu_callback(choice):
            # Update the substance dropdown based on selected drug class
            substance_optionmenu.configure(values=drugtypes[choice])
            substance_optionmenu.set(drugtypes[choice][0])

        selected_drug_class = ctk.StringVar(value=list(drugtypes.keys())[0])

        # 1st dropdown menu (Drug Class)
        drug_class_optionmenu = ctk.CTkOptionMenu(
            drug_class_frame,
            variable=selected_drug_class,
            values=list(drugtypes.keys()),
            command=optionmenu_callback,
        )
        drug_class_optionmenu.pack(padx=20, pady=10, anchor="n")

        substance_frame = ctk.CTkFrame(frame)
        substance_frame.pack(padx=100, pady=(20, 10), fill="x")

        Substance_label = ctk.CTkLabel(
            substance_frame, text="Substance", anchor="w", font=ctk.CTkFont(size=30)
        )
        Substance_label.pack(padx=20, pady=10, anchor="n")

        selected_substance = ctk.StringVar(value=drugtypes[list(drugtypes.keys())[0]][0])

        # 2nd dropdown menu (Substance)
        substance_optionmenu = ctk.CTkOptionMenu(
            substance_frame,
            variable=selected_substance,
            values=drugtypes[list(drugtypes.keys())[0]],
        )
        substance_optionmenu.pack(padx=20, pady=10, anchor="n")

        # Initialize the substance dropdown based on the initial drug class selection
        optionmenu_callback(list(drugtypes.keys())[0])

        stashAmount_frame = ctk.CTkFrame(frame)
        stashAmount_frame.pack(padx=100, pady=(20, 10), fill="x")

        StashAmount_label = ctk.CTkLabel(
            stashAmount_frame,
            text="Stash Amount",
            anchor="w",
            font=ctk.CTkFont(size=30),
        )
        StashAmount_label.pack(padx=20, pady=10, anchor="n")

        # Create the option menu
        self.stashUnit = ctk.CTkOptionMenu(
            stashAmount_frame,
            values=["grams", "milligrams", "micrograms", "pounds", "ounces"],
        )
        self.stashUnit.pack(padx=20, pady=10, anchor="n")
        self.stashUnit.set("grams")

        self.stashAmount_entry = ctk.CTkEntry(
            stashAmount_frame,
            placeholder_text="Enter Stash Amount",
        )
        self.stashAmount_entry.pack(padx=20, pady=10, anchor="n")

        sourceFrame = ctk.CTkFrame(frame)
        sourceFrame.pack(padx=100, pady=(20, 10), fill="x")

        Source_label = ctk.CTkLabel(
            sourceFrame, text="Source Cost", anchor="w", font=ctk.CTkFont(size=30)
        )
        Source_label.pack(padx=20, pady=10, anchor="n")

        def validate_input(P):
            if P == "":
                return True
            try:
                float(P)
                return True
            except ValueError:
                return False

        validate_cmd = self.register(validate_input)

        source_entry = ctk.CTkEntry(
            sourceFrame,
            placeholder_text="420.69",
            validate="key",
            validatecommand=(validate_cmd, "%P"),
        )
        source_entry.pack(padx=20, pady=10, anchor="n")

        def add_stash_event():
            # Convert source cost to float
            if source_entry.get() == "":
                source_spend = 0.0
            else:
                source_spend = float(source_entry.get())

            # Retrieve user input
            stash_amount = float(self.stashAmount_entry.get())
            stash_unit = self.stashUnit.get()

            # Create a Quantity object for the stash amount
            stash_amount_quantity = self.ureg.Quantity(stash_amount, stash_unit)

            # Convert the stash amount to grams
            if stash_unit == "grams":
                stash_amount_converted = stash_amount_quantity.to(self.ureg.grams)
            elif stash_unit == "milligrams":
                stash_amount_converted = stash_amount_quantity.to(self.ureg.grams)
            elif stash_unit == "micrograms":
                stash_amount_converted = stash_amount_quantity.to(self.ureg.grams)
            elif stash_unit == "pounds":
                stash_amount_converted = stash_amount_quantity.to(self.ureg.grams)
            elif stash_unit == "ounces":
                stash_amount_converted = stash_amount_quantity.to(self.ureg.grams)
            else:
                stash_amount_converted = stash_amount_quantity.to(
                    self.ureg.grams
                )  # Default to grams

            new_stash = {
                "drug_class": selected_drug_class.get(),
                "substance": selected_substance.get(),
                "stash_unit": f"{stash_unit}",  # Store in grams for consistency
                "stash_amount": stash_amount_converted.magnitude,  # Store the magnitude in grams
                "source_cost": source_spend,
                "total_used": float(0),
            }

            file_path = "stash.json"

            # Check if the file exists
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = []  # Handle case where the file is empty or invalid JSON
            else:
                # If file does not exist, initialize an empty list
                data = []

            if new_stash["substance"] in [stash["substance"] for stash in data]:
                CTkMessagebox(
                    title="Error",
                    message=f"{new_stash['substance']} already exists.",
                    cancel_button_color="transparent",
                    justify="center",
                )
                return

            data.append(new_stash)

            # Write updated data back to the file
            try:
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                print(f"Error writing to file: {e}")

            source_entry.delete(0, ctk.END)
            self.stashAmount_entry.delete(0, ctk.END)
            self.controller.stash_selector()

            CTkMessagebox(
                title="Success",
                icon="check",
                message=f"{new_stash['substance']} added to stash.",
                cancel_button_color="transparent",
                justify="center",
            )

        add_stash_button = ctk.CTkButton(
            frame, text="Add Stash", command=add_stash_event
        )
        add_stash_button.pack(padx=100, pady=(5, 10), anchor="n", fill="x")

        def check_entry_state():
            if (
                self.stashAmount_entry.get() == ""
                or not self.stashAmount_entry.get().isdigit()
            ):
                add_stash_button.configure(state="disabled")
            else:
                add_stash_button.configure(state="normal")

            self.after(100, check_entry_state)

        check_entry_state()

import customtkinter as ctk
import os
import json
from functools import partial


class StashView(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
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
        # self.after(200, self.config_stash_data)

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

                amount = f"{float(stash['stash_amount']):.2f}"

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
