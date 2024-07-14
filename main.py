import customtkinter as ctk
import webbrowser
from views.stashview import StashView
from views.calendarview import CalendarView
from views.addstashview import AddStashView
from views.newpage import NewPage
from views.notesview import NotesView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("themes/blue.json")


class App(ctk.CTk):
    frames = {
        "stash": None,
        "calendar": None,
        "add_stash": None,
        "new_page": None,
        "notes": None,
    }

    def stash_selector(self):
        self.hide_all_frames()
        self.frames["stash"].config_stash_data()
        App.frames["stash"].pack(
            in_=self.right_side_container,
            side=ctk.TOP,
            fill=ctk.BOTH,
            expand=True,
        )

    def calendar_selector(self):
        self.hide_all_frames()
        App.frames["calendar"].pack(
            in_=self.right_side_container,
            side=ctk.TOP,
            fill=ctk.BOTH,
            expand=True,
        )

    def add_stash_slider(self):
        self.hide_all_frames()
        App.frames["add_stash"].pack(
            in_=self.right_side_container,
            side=ctk.TOP,
            fill=ctk.BOTH,
            expand=True,
        )

    def new_page_selector(self, stash):
        self.hide_all_frames()
        new_page_frame = App.frames["new_page"]
        new_page_frame.pack(
            in_=self.right_side_container,
            side=ctk.TOP,
            fill=ctk.BOTH,
            expand=True,
        )
        new_page_frame.update_data(stash)

    def Notes_selector(self):
        self.hide_all_frames()
        App.frames["notes"].pack(
            in_=self.right_side_container,
            side=ctk.TOP,
            fill=ctk.BOTH,
            expand=True,
        )

    def hide_all_frames(self):
        for frame in self.frames.values():
            if frame is not None:
                frame.pack_forget()

    def __init__(self):
        super().__init__()
        self.title("ChemStash")
        self.geometry("900x900")
        self.resizable(True, True)

        main_container = ctk.CTkFrame(self)
        main_container.pack(
            fill=ctk.BOTH,
            expand=True,
        )

        left_side_panel = ctk.CTkFrame(main_container, width=150, fg_color="#161925")
        left_side_panel.pack(
            side=ctk.LEFT,
            fill=ctk.Y,
            expand=False,
        )

        left_side_panel.grid_rowconfigure(0, weight=0)
        left_side_panel.grid_rowconfigure(1, weight=0)
        left_side_panel.grid_rowconfigure(2, weight=0)
        left_side_panel.grid_rowconfigure(3, weight=0)
        left_side_panel.grid_rowconfigure(4, weight=0)
        left_side_panel.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(
            left_side_panel, text="ChemStash", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.stash_button = ctk.CTkButton(
            left_side_panel, text="Stash", command=self.stash_selector
        )
        self.stash_button.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.calendar_button = ctk.CTkButton(
            left_side_panel, text="Calendar", command=self.calendar_selector
        )
        self.calendar_button.grid(row=2, column=0, padx=20, pady=(20, 10))

        self.Notes_button = ctk.CTkButton(
            left_side_panel, text="Notes", command=self.Notes_selector
        )

        self.add_stash_button = ctk.CTkButton(
            left_side_panel, text="Add Stash", command=self.add_stash_slider
        )
        self.add_stash_button.grid(row=3, column=0, padx=20, pady=(20, 10))

        self.psychonaut_button = ctk.CTkButton(
            left_side_panel, text="PsychonautWiki", command=self.psychonaut_button_event
        )

        self.Notes_button.grid(row=4, column=0, padx=20, pady=(20, 10))

        self.psychonaut_button.grid(row=5, column=0, padx=20, pady=(20, 10), sticky="s")

        self.right_side_panel = ctk.CTkFrame(main_container)
        self.right_side_panel.pack(
            side=ctk.LEFT,
            fill=ctk.BOTH,
            expand=True,
        )

        self.right_side_container = ctk.CTkFrame(self.right_side_panel)
        self.right_side_container.pack(
            side=ctk.LEFT,
            fill=ctk.BOTH,
            expand=True,
        )

        # Create the frames
        self.frames["stash"] = StashView(self.right_side_container, self)
        self.frames["calendar"] = CalendarView(self.right_side_container)
        self.frames["add_stash"] = AddStashView(
            self.right_side_container, self
        )  # Pass self as controller
        self.frames["new_page"] = NewPage(
            self.right_side_container,
            self,
            self.frames["calendar"],
            self.frames["stash"],
        )
        self.frames["notes"] = NotesView(self.right_side_container)

        self._stash_view = self.frames["stash"]
        self._add_stash_view = self.frames["add_stash"]

        # Start on the Stash page
        self.stash_selector()

    def psychonaut_button_event(self):
        webbrowser.open_new("https://psychonautwiki.org/wiki/Main_Page")


if __name__ == "__main__":
    app = App()
    app.mainloop()
