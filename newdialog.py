from tkinter import *


class SpecificDialog(Toplevel):
    """Class for creating additional Dialogs, that have minimal dependence on their parents."""
    def __init__(self, parent, name_info='', title='_no_title_'):
        """Default initialization, top-level settings, executing wait_window() here."""
        # Create a top_level window.
        Toplevel.__init__(self, parent)
        self.name_info = name_info

        # Some top-level settings.
        self.transient(parent)
        self.title(title)
        # Create dialog body.
        body = Frame(self)
        body.pack(padx=5, pady=5)
        # Set a default focus to the window.
        self.initial_focus = self.body(body)
        self.buttonbox()
        # Make dialog modal
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        # Make sure an explicit close is treated as cancel
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        # Set dialog position relative to the parent window.
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 150, parent.winfo_rooty() + 150))
        # Move the keyboard focus to the appropriate widget.
        self.initial_focus.focus_set()

        # Some variables
        self.parent = parent
        self.result = {}

        # Method, that enters a local event loop and doesn't return until
        # the given window is destroyed.
        self.wait_window(self)

    def buttonbox(self):
        """Function to create a frame with only button [OK]"""
        # Create a Frame and place box on it.
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        # Bind <Enter> to 'OK' and <Esc> to 'Cancel'
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def body(self, master):
        """
        Create the main dialog body.
        Return widget, that should have initial focus.
        """
        # This method should be overridden
        pass

    def ok(self, event=None):
        """Behavior, if [OK] or [RETURN] pressed"""
        valid_report = self.validate()
        if valid_report != 'OK':
            self.react_validate(valid_report)
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        """Destroy window and put focus back to the parent window."""
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        """Validate information, you've putted."""
        # override this method later.
        return 'OK'

    def react_validate(self, report):
        """Reaction, if validation was false."""
        # override this method later.
        pass

    def apply(self):
        """Save returned value in this method."""
        # override this method later.
        pass
