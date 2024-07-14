import customtkinter as ctk
import json
import os


class NotesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        if os.path.exists("notes.json") and os.path.getsize("notes.json") > 0:
            with open("notes.json", "r") as f:
                self.notes = json.load(f)
        else:
            notes_empty_frame = ctk.CTkFrame(self, corner_radius=10)
            notes_empty_frame.pack(expand=True, padx=20, pady=300, fill="x")

            notes_empty_label = ctk.CTkLabel(
                notes_empty_frame, text="No notes yet", font=(ctk.CTkFont, 30)
            )
            notes_empty_label.pack(fill="both", expand=True)
