import os
import csv
import datetime

import pandas as pd # type: ignore
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk # type: ignore


from unity_notifier import UnityNotifier 
from ExperimentData import ExperimentData


data_for_experiments = 'unity_data.csv'
timestamp_file_event = "experiment_log.csv"

#Class with gui
class MainGUI(ExperimentData):

    def __init__(self, root):
        '''
        Here is initialization of GUI. Define styles etc.
        '''
        self.root = root
        self.root.title("Cybersickness")
        self.root.configure(bg="black")

        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        screen_width = 1200
        screen_height = 800
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.remaining_time = 0
        self.timer_running = False
        self.notifier_unity = UnityNotifier()  
        self.timer_job = None
        self.current_experiment = None

        path_to_data_experiment = os.getcwd()

        file_path = os.path.join(path_to_data_experiment,'unity_data', data_for_experiments)
        self.experiment_data = ExperimentData(file_path)

        image_path = os.path.join(path_to_data_experiment, 'Cube_vis.png')
        if os.path.exists(image_path):
            original_image = Image.open(image_path)
            resized_image = original_image.resize((120, 120), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(resized_image)
        else:
            self.image = None

        self.styles = {
            "h1": {"bg": "black", "fg": "white", "font": ("Roboto", 24)},
            "h2": {"bg": "black", "fg": "white", "font": ("Roboto", 20)},
            "vb": {"bg": "black", "fg": "white", "font": ("Roboto", 18), "justify": "left"},
            "entry": {"font": ("Roboto", 14), "foreground": "black", "width": 8},
            "api": {"font": ("Roboto", 14), "foreground": "black", "width": 8}
        }

        self.left_padx_h1_h2 = 60
        self.left_padx_vb = 80
        self.left_padx_entry = 160

        self.MainGUIapp()
        experiment = self.experiment_data.data.iloc[self.experiment_data.current_index]
        self.current_experiment = experiment
        self.fill_gui_fields(experiment)
        self.start_button.config(state="normal", text="Start Experiment", bg="green", command=self.update_simulation)

    def MainGUIapp(self):
        '''
        The method defines the apperance of the GUI
        '''
        container = self.root

        self.scenario_text = tk.Label(container, text='Scenario number', padx=self.left_padx_h1_h2, pady=20, **self.styles["h1"])
        self.scenario_text.grid(row=0, sticky=tk.W)

        self.grid_set_text = tk.Label(container, text='Grid settings', padx=self.left_padx_h1_h2, pady=10, **self.styles["h1"])
        self.grid_set_text.grid(row=1, column=0, sticky=tk.W)

        self.grid_size_text = tk.Label(container, text='Grid size', padx=self.left_padx_h1_h2, pady=5, **self.styles["h2"])
        self.grid_size_text.grid(row=2, column=0, sticky=tk.W)

        self.x_label = tk.Label(container, text="X", **self.styles["vb"])
        self.x_label.grid(row=3, column=0, padx=self.left_padx_vb, sticky=tk.W)
        self.x_size_combo = tk.Entry(container, **self.styles["entry"])
        self.x_size_combo.grid(row=3, column=0, padx=self.left_padx_entry, sticky=tk.W)

        self.y_label = tk.Label(container, text="Y", **self.styles["vb"])
        self.y_label.grid(row=4, column=0, padx=self.left_padx_vb, sticky=tk.W)
        self.y_size_combo = tk.Entry(container, **self.styles["entry"])
        self.y_size_combo.grid(row=4, column=0, padx=self.left_padx_entry, sticky=tk.W)

        self.z_label = tk.Label(container, text="Z", **self.styles["vb"])
        self.z_label.grid(row=5, column=0, padx=self.left_padx_vb, sticky=tk.W)
        self.z_size_combo = tk.Entry(container, **self.styles["entry"])
        self.z_size_combo.grid(row=5, column=0, padx=self.left_padx_entry, sticky=tk.W)

        self.items_size_text = tk.Label(container, text='Items appearance', padx=self.left_padx_h1_h2, pady=15, **self.styles["h2"])
        self.items_size_text.grid(row=6, column=0, sticky=tk.W)

        self.kind_label = tk.Label(container, text="Kind", **self.styles["vb"])
        self.kind_label.grid(row=7, column=0, padx=self.left_padx_vb, sticky=tk.W)
        self.kind_label_combo = ttk.Combobox(container, values=['Cube', 'Sphere'], **self.styles["api"])
        self.kind_label_combo.grid(row=7, column=0, padx=self.left_padx_entry, sticky=tk.W)

        self.color_label = tk.Label(container, text="Color", **self.styles["vb"])
        self.color_label.grid(row=8, column=0, padx=self.left_padx_vb, sticky=tk.W)
        self.color_label_combo = ttk.Combobox(container, values=['Blue', 'Red', 'Green'], **self.styles["api"])
        self.color_label_combo.grid(row=8, column=0, padx=self.left_padx_entry, sticky=tk.W)

        if self.image:
            self.img_label = tk.Label(container, image=self.image, bg='black')
            self.img_label.grid(row=1, column=1, rowspan=6, padx=10, pady=10)

        self.dir_label = tk.Label(container, text="Direction", **self.styles["vb"])
        self.dir_label.grid(row=3, column=3, padx=self.left_padx_vb-20, sticky=tk.W)
        self.dir_label_combo = ttk.Combobox(container, values=['Up', 'Forward', 'Left', 'None'], **self.styles["api"])
        self.dir_label_combo.grid(row=3, column=3, padx=self.left_padx_entry+30, sticky=tk.W)

        self.speed_dir_label = tk.Label(container, text="Speed", **self.styles["vb"])
        self.speed_dir_label.grid(row=4, column=3, padx=self.left_padx_vb-20, sticky=tk.W)
        self.speed_dir_label_combo = tk.Entry(container, **self.styles["entry"])
        self.speed_dir_label_combo.grid(row=4, column=3, padx=self.left_padx_entry+30, sticky=tk.W)

        self.rot_label = tk.Label(container, text="Rotation", padx=self.left_padx_h1_h2, pady=15, **self.styles["h2"])
        self.rot_label.grid(row=6, column=3, sticky=tk.W)

        self.rot_kind_label = tk.Label(container, text="Kind", **self.styles["vb"])
        self.rot_kind_label.grid(row=7, column=3, padx=self.left_padx_vb-20, sticky=tk.W)
        self.rot_label_combo = ttk.Combobox(container, values=['Roll', 'Yaw', 'Pitch', 'None'], **self.styles["api"])
        self.rot_label_combo.grid(row=7, column=3, padx=self.left_padx_entry+30, sticky=tk.W)

        self.rot_speed_label = tk.Label(container, text="Speed", **self.styles["vb"])
        self.rot_speed_label.grid(row=8, column=3, padx=self.left_padx_vb-20, sticky=tk.W)
        self.rot_speed_label_combo = tk.Entry(container, **self.styles["entry"])
        self.rot_speed_label_combo.grid(row=8, column=3, padx=self.left_padx_entry+30, sticky=tk.W)

        self.button_frame = tk.Frame(container, bg="black")
        self.button_frame.grid(row=9, column=0, columnspan=5, pady=30)

        
        self.start_button = tk.Button(self.button_frame, text="Start Experiment", command=self.start_program, font=("Roboto", 14), bg="blue", fg="white", height=2, width=18)
        self.start_button.pack(side="left", padx=20)

        self.counter_label = tk.Label(self.button_frame, text=str(self.experiment_data.current_index), font=("Roboto", 16), bg="black", fg="white", width=4)
        self.counter_label.pack(side="left", padx=10)

        self.minus_button = tk.Button(self.button_frame, text="-", command=self.decrement_index, font=("Roboto", 14), bg="gray", fg="white", width=4)
        self.minus_button.pack(side="left")

        self.plus_button = tk.Button(self.button_frame, text="+", command=self.increment_index, font=("Roboto", 14), bg="gray", fg="white", width=4)
        self.plus_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop Experiment", command=self.reset_experiment, font=("Roboto", 14), bg="red", fg="white", height=2, width=18)
        self.stop_button.pack(side="left", padx=20)

        self.timer_label = tk.Label(container, text="Time left: 0s", font=("Roboto", 16), bg="black", fg="white")
        self.timer_label.grid(row=10, column=1, pady=20)

        self.hard_stop_button = tk.Button(container, text="Hard Stop", command=self.hard_stop_experiment, font=("Roboto", 14), bg="darkred", fg="white", height=2, width=18)
        self.hard_stop_button.grid(row=10, column=2, pady=20)
        self.timer_label.grid(row=10, column=1, pady=20)

    def start_program(self):
        self.start_button.config(state="normal", text="Start Experiment", bg="green", command=self.update_simulation)
        self.stop_button.config(state="normal")

    def log_event(self, event_type):
        log_path = os.path.join(os.getcwd(), timestamp_file_event)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        scenario = self.current_experiment['Scenario'] if self.current_experiment is not None else "Unknown"
        with open(log_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([event_type, scenario, timestamp])

    def update_simulation(self):
        experiment = self.experiment_data.data.iloc[self.experiment_data.current_index]
        self.current_experiment = experiment
        self.fill_gui_fields(experiment)
        self.remaining_time = int(experiment["Duration_in_sec"])
        self.counter_label.config(text=str(self.experiment_data.current_index))
        self.start_button.config(state="disabled")
        self.log_event("START")
        print("Sending scenario:", experiment["Scenario"])

        #wysylanie scenariusza na konkretny port w Unity
        self.notifier_unity.start_scenario(experiment["Scenario"]) 
        self.update_timer()

    def increment_index(self):
        if self.experiment_data.current_index < len(self.experiment_data.data) - 1:
            self.experiment_data.current_index += 1
        self.counter_label.config(text=str(self.experiment_data.current_index))
        experiment = self.experiment_data.data.iloc[self.experiment_data.current_index]
        self.current_experiment = experiment
        self.fill_gui_fields(experiment)
        self.remaining_time = int(experiment["Duration_in_sec"])
        self.timer_label.config(text="Time left: 0s")
        self.start_button.config(state="normal", text="Start Experiment", bg="green", command=self.update_simulation)

    def decrement_index(self):
        if self.experiment_data.current_index > 0:
            self.experiment_data.current_index -= 1
        self.counter_label.config(text=str(self.experiment_data.current_index))
        experiment = self.experiment_data.data.iloc[self.experiment_data.current_index]
        self.current_experiment = experiment
        self.fill_gui_fields(experiment)
        self.remaining_time = int(experiment["Duration_in_sec"])
        self.timer_label.config(text="Time left: 0s")
        self.start_button.config(state="normal", text="Start Experiment", bg="green", command=self.update_simulation)

        
    def hard_stop_experiment(self):
        self.log_event("HARD STOP")

        #wysylanie hardstop do unity
        self.notifier_unity.hard_stop() 
        if self.flask_process:
            self.flask_process.terminate()
            print("[GUI] Flask server terminated.")

        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.remaining_time = 0

        if tk.messagebox.askyesno("Exit", "Are you sure you want to exit the program?"):
            self.root.destroy()

    def reset_experiment(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.log_event("STOP")  
        self.notifier_unity.stop_scenario(self.current_experiment["Scenario"]) 


        self.timer_running = False
        self.remaining_time = 0

        if self.current_experiment is not None:
            self.fill_gui_fields(self.current_experiment)

        self.timer_label.config(text="Time left: 0s")
        self.start_button.config(state="normal", text="Start Experiment", bg="green", command=self.update_simulation)
        self.stop_button.config(state="normal")


    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.config(text=f"Time left: {self.remaining_time}s")
            self.remaining_time -= 1
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Scenario finished.")
            self.log_event("END")
            # self.notifier_unity.stop_scenario(self.current_experiment["Scenario"]) 
            self.start_button.config(state="normal")
            self.stop_button.config(state="normal")
            self.timer_job = None
            self.timer_running = False


    def previous_experiment(self):
        experiment = self.experiment_data.get_previous_experiment()
        self.current_experiment = experiment
        self.fill_gui_fields(experiment)
        self.remaining_time = int(experiment["Duration_in_sec"])
        self.timer_label.config(text="Time left: 0s")
        self.start_button.config(state="normal", text="Start Experiment", bg="green", command=self.update_simulation)

    def fill_gui_fields(self, experiment):
        self.scenario_text.config(text=f"Scenario number: {experiment['Scenario']}")
        self.x_size_combo.delete(0, tk.END)
        self.x_size_combo.insert(0, f"{experiment['X']}")
        self.y_size_combo.delete(0, tk.END)
        self.y_size_combo.insert(0, f"{experiment['Y']}")
        self.z_size_combo.delete(0, tk.END)
        self.z_size_combo.insert(0, f"{experiment['Z']}")
        self.kind_label_combo.set(experiment['Cube'])
        self.color_label_combo.set(experiment['Color'])
        self.dir_label_combo.set(experiment['Kind_of_move'])
        self.speed_dir_label_combo.delete(0, tk.END)
        self.speed_dir_label_combo.insert(0, experiment['Velocity_move'])
        self.rot_label_combo.set(experiment['Kind_of_roll'])
        self.rot_speed_label_combo.delete(0, tk.END)
        self.rot_speed_label_combo.insert(0, experiment['Velocity_roll'])


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()
