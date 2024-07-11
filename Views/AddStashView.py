import customtkinter as ctk
from DrugTypes import subTypes
from pint import UnitRegistry
import json
import os
import uuid
from CTkMessagebox import CTkMessagebox


class AddStashView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

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
            substance_optionmenu.configure(values=subTypes[choice])
            substance_optionmenu.set(subTypes[choice][0])

        selected_drug_class = ctk.StringVar(value=list(subTypes.keys())[0])

        # 1st dropdown menu (Drug Class)
        drug_class_optionmenu = ctk.CTkOptionMenu(
            drug_class_frame,
            variable=selected_drug_class,
            values=list(subTypes.keys()),
            command=optionmenu_callback,
        )
        drug_class_optionmenu.pack(padx=20, pady=10, anchor="n")

        substance_frame = ctk.CTkFrame(frame)
        substance_frame.pack(padx=100, pady=(20, 10), fill="x")

        Substance_label = ctk.CTkLabel(
            substance_frame, text="Substance", anchor="w", font=ctk.CTkFont(size=30)
        )
        Substance_label.pack(padx=20, pady=10, anchor="n")

        selected_substance = ctk.StringVar(value=subTypes[list(subTypes.keys())[0]][0])

        # 2nd dropdown menu (Substance)
        substance_optionmenu = ctk.CTkOptionMenu(
            substance_frame,
            variable=selected_substance,
            values=subTypes[list(subTypes.keys())[0]],
        )
        substance_optionmenu.pack(padx=20, pady=10, anchor="n")

        # Initialize the substance dropdown based on the initial drug class selection
        optionmenu_callback(list(subTypes.keys())[0])

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
                "stash_unit": "grams",  # Store in grams for consistency
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
