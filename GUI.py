import time
import tkinter as tk
from tkinter import Button, Label, Entry, StringVar, Checkbutton, BooleanVar
from tkinter.ttk import Combobox
from Mechanics import ChromeDriver
import threading
import pickle
from tkinter import filedialog
from PIL import Image, ImageTk

class Gui:
    """generates GUI from tkinter and populates and imports all needed modules"""
    def __init__(self):
        FONT = "Helvetica"

        self.automation_thread = None  # Initialize the thread object to None

        self.root = tk.Tk()
        self.title = self.root.title("Neopets Name Availability Checker")
        self.geometry = self.root.geometry("500x800+550+1")
        self.resizable = self.root.resizable(False, False)
        self.bg_color = self.root.config(background="white")

        # Set the window icon
        # icon_path = "green_dragon.png"
        # self.root.iconphoto(True, tk.PhotoImage(file=icon_path))

        # Load the image
        # image_path = "Neopets-logo.jpg"  # Replace with your image file path
        # image = Image.open(image_path)
        # image = image.resize((150, 150))  # Adjust the image size as needed

        # Create an ImageTk object
        # image_tk = ImageTk.PhotoImage(image)

        # Create an image widget
        # image_label = tk.Label(self.root, image=image_tk)
        # image_label.image = image_tk  # Store a reference to avoid garbage collection
        # image_label.place(x=15, y=75)

        # main label for top
        self.main_Label = Label(self.root, text="Neopets Name Availability Checker", font=(FONT, 22), background='white')
        self.main_Label.pack(ipady=5)

        # Neopets Login Username
        self.username_Label = Label(self.root, text="Neopets Username", font=(FONT, 12), background='white')
        self.username_Label.pack(ipady=5)

        # Neopets username login entry widget
        self.username_entry = Entry(self.root, width=20, font=('Helvetica', 10), background="white")
        self.username_entry.pack(ipady=5)

        # Add a Checkbutton for saving the username
        self.save_username = BooleanVar()
        self.save_username_checkbutton = Checkbutton(self.root, text="Save username", variable=self.save_username, background='white')
        self.save_username_checkbutton.pack(ipady=5)

        # Neopets Login Password
        self.password_Label = Label(self.root, text="Neopets Password", font=(FONT, 12), background='white')
        self.password_Label.pack(ipady=5)

        # Neopets Password login entry widget
        self.password_entry = Entry(self.root, width=20, font=('Helvetica', 10),background='white')
        self.password_entry.pack(ipady=5)

        # Add a Checkbutton for saving the password
        self.save_password = BooleanVar()
        self.save_password_checkbutton = Checkbutton(self.root, text="Save password", variable=self.save_password, background='white')
        self.save_password_checkbutton.pack(ipady=5)

        # Create a new Frame 2
        self.spin_frame_2 = tk.Frame(self.root, background='white')
        self.spin_frame_2.pack(anchor="w", padx=30, pady=5)

        # Neopets name count label
        self.how_many_names_label = tk.Label(self.spin_frame_2,
                                             text="Name Count:",
                                             font=(FONT, 14), wraplength=400, background='white')
        self.how_many_names_label.pack(side="left", ipady=5)

        self.spinbox_var_2 = tk.StringVar()

        # Number wheel for name count
        self.number_wheel_2 = tk.Spinbox(self.spin_frame_2, from_=1, to=100, validate="focusout",
                                         textvariable=self.spinbox_var_2, font=(FONT, 14), width=3, background='white')
        self.number_wheel_2.pack(side="left", padx=70, pady=15)

        # Create a new Frame
        self.spin_frame = tk.Frame(self.root, background='white')
        self.spin_frame.pack(anchor="w", padx=30, pady=5)

        # Label for word length
        self.word_length_label = tk.Label(self.spin_frame, text="Word Length:", font=(FONT, 14), background='white')
        self.word_length_label.pack(side="left")

        self.spinbox_var = tk.StringVar()

        # Number wheel for word length
        self.number_wheel = tk.Spinbox(self.spin_frame, from_=4, to=12, validate="focusout",
                                       textvariable=self.spinbox_var, font=(FONT, 14), width=3, background='white')
        self.number_wheel.pack(side="left", padx=63, pady=15)

        # Create a new Frame
        self.spin_frame_3 = tk.Frame(self.root,background='white')
        self.spin_frame_3.pack(anchor="w", padx=30, pady=5)

        # Label for word length
        self.time_between_names = tk.Label(self.spin_frame_3, text="Time Interval:", font=(FONT, 14),background='white')
        self.time_between_names.pack(side="left")

        self.spinbox_var_3 = tk.StringVar()

        self.float_values = ['0.25', '0.35', '0.45', '0.55', '0.65', '0.75', '0.85', '0.95', '1.00', '1.25']

        # Number wheel for word length
        self.number_wheel_3 = Combobox(self.spin_frame_3, validate="focusout", values=self.float_values,
                                       textvariable=self.spinbox_var_3, font=(FONT, 14), width=4)
        self.number_wheel_3.pack(side="left", padx=63, pady=15)


        # label for word length
        self.word_letters_label = Label(self.root, text="Desired Characters Positions", font=(FONT, 15), background='white')
        self.word_letters_label.pack(ipadx=70, pady=15)

        self.entries_frame = tk.Frame(self.root)  # Frame to hold the Entry widgets
        self.entries_frame.pack(pady=10)

        self.entries = []  # moved up
        self.entry_values = []

        # Add check button for "Capitalize First Letter"
        self.capitalize_var = tk.BooleanVar()
        self.capitalize_check = Checkbutton(self.root, text="Capitalize First Letter", font=(FONT, 12),
                                            variable=self.capitalize_var, background='white')
        self.capitalize_check.pack(pady=5)

        # Add check button for "Double Letter Requirement"
        self.double_letter_var = tk.BooleanVar()
        self.double_letter_check = Checkbutton(self.root, text="Double Letter Requirement", font=(FONT, 12),
                                               variable=self.double_letter_var, background='white')
        self.double_letter_check.pack(pady=5)

        # Inside the __init__ method
        self.file_path_button = Button(self.root, text="Choose File Path", font=(FONT, 10), command=self.browse_file_path, background='light green')
        self.file_path_button.pack(pady=5)

        self.file_path_label = tk.Label(self.root, text="No file selected", background='white')
        self.file_path_label.pack(ipady=5)

        # Button to submit the entries
        self.submit_button = Button(self.root, text="Enter", font=(FONT, 15), command=self.submit, background='light green')
        self.submit_button.pack(pady=5)

        # Button to stop the automation NOT WORKING
        # self.stop_button = Button(self.root, text="Stop", font=(FONT, 15), background="red", foreground="black")
        # self.stop_button.pack(pady=2)

        self.spinbox_var.trace('w', self.update_fields)  # Moved the trace after the initialization of self.entries_frame
        self.spinbox_var.set(4)  # Setting initial value for Spinbox
        self.update_fields()  # Display initial set of Entry fields

        # Load the entries if the corresponding files exist
        try:
            with open('username.pkl', 'rb') as f:
                self.username_entry.insert(0, pickle.load(f))
                self.save_username.set(True)
        except FileNotFoundError:
            pass
        try:
            with open('password.pkl', 'rb') as f:
                self.password_entry.insert(0, pickle.load(f))
                self.save_password.set(True)
        except FileNotFoundError:
            pass

        # Bind the function to the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def validate_length(self, new_text):
        return len(new_text) <= 1  # If length is less than or equal to 1, return True (validation success)


    def update_fields(self, *args):
        for entry in self.entries:
            entry.grid_forget()
        self.entries.clear()
        self.entry_values.clear()
        length = int(self.spinbox_var.get())
        vcmd = (self.root.register(self.validate_length), '%P')  # Registering a validation command
        for i in range(length):
            var = tk.StringVar()
            entry = Entry(self.entries_frame, textvariable=var, width=2, validate="key", validatecommand=vcmd,
                          font=('Helvetica', 20))
            entry.insert(0, "-")  # Insert placeholder in the entry field
            entry.grid(row=0, column=i)
            self.entries_frame.grid_columnconfigure(i, weight=1)  # Setting weight for column
            self.entries.append(entry)
            self.entry_values.append(var)

    def run_automation(self):
        USERNAME = self.username_entry.get()
        PASSWORD = self.password_entry.get()
        template = " ".join(var.get() for var in self.entry_values)
        is_capitalize = self.capitalize_var.get()
        is_double_letter = self.double_letter_var.get()

        URL = "https://www.neopets.com/login/"

        neopets_driver = ChromeDriver(url=URL, username=USERNAME, password=PASSWORD)
        #neopets_driver.login()
        neopets_driver.fill_fields()

        number_of_names = int(self.spinbox_var_2.get())
        time_interval = float(self.spinbox_var_3.get())

        file_path = self.file_path_label.cget('text')  # Get the selected file path
        time.sleep(5)
        neopets_driver.search_names(template, len(template), is_capitalize, is_double_letter, file_path, number_of_names, time_interval)


        # Clean up after stopping
        neopets_driver.browser_close()
        self.automation_thread = None

    def submit(self):
        result = "".join(var.get() for var in self.entry_values)
        result = result.replace("-", " ")  # replace placeholders with spaces
        print(f"Raw result: {result!r}")

        print(result)

        # Fetch the states of checkboxes
        is_capitalize = self.capitalize_var.get()
        is_double_letter = self.double_letter_var.get()

        print("Capitalize First Letter:", is_capitalize)
        print("Double Letter Requirement:", is_double_letter)

        # Start the automation in a new thread
        self.automation_thread = threading.Thread(target=self.run_automation)
        self.automation_thread.start()

    # Function to be called when the window is closed
    def on_close(self):
        # Save the entries if the corresponding Checkbuttons are checked
        if self.save_username.get():
            with open('username.pkl', 'wb') as f:
                pickle.dump(self.username_entry.get(), f)
        if self.save_password.get():
            with open('password.pkl', 'wb') as f:
                pickle.dump(self.password_entry.get(), f)
        self.root.destroy()

    def get_file_path(self):
        # User selects a file path
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialdir="/",
                                                 title="Choose location",
                                                 filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))

        # bring focus back to the main application
        self.root.focus_force()

        return file_path

    def browse_file_path(self):
        file_path = self.get_file_path()
        print("Selected file path:", file_path)
        # Do something with the file path, such as passing it to the search_names method
        self.file_path_label.config(text=file_path)

    def mainloop(self):
        self.root.mainloop()


