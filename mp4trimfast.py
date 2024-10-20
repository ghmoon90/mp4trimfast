import tkinter as tk
from tkinter import filedialog, messagebox
import moviepy.editor as mp
import json
import os

# Function to select mp4 file using tkinter
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    return file_path

# Function to load settings from JSON file
def load_settings(json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            settings = json.load(f)
    else:
        # Default settings if the file doesn't exist
        settings = {"start_time": 0, "end_time": 10, "speed": 1.0}
    return settings

# Function to save updated settings to JSON
def save_settings(json_file, settings):
    with open(json_file, 'w') as f:
        json.dump(settings, f, indent=4)

# Function to process the video with trimming and speed
def process_video(file_path, start_time, end_time, speed):
    # Load the video
    video = mp.VideoFileClip(file_path)
    
    # Trim the video
    trimmed_video = video.subclip(start_time, end_time)
    
    # Accelerate the video speed
    accelerated_video = trimmed_video.fx(mp.vfx.speedx, speed)
    
    # Save the processed video
    output_path = file_path.replace(".mp4", "_processed.mp4")
    accelerated_video.write_videofile(output_path)
    print(f"Processed video saved as: {output_path}")
    messagebox.showinfo("Success", f"Processed video saved as: {output_path}")

# Function to open the settings editor GUI
def edit_settings_gui(settings_file):
    # Load current settings
    settings = load_settings(settings_file)

    def save_and_close():
        try:
            # Get the values from the input fields and save them to the settings JSON
            settings["start_time"] = float(start_time_var.get())
            settings["end_time"] = float(end_time_var.get())
            settings["speed"] = float(speed_var.get())
            save_settings(settings_file, settings)
            messagebox.showinfo("Settings", "Settings saved successfully!")
            settings_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for the settings.")

    # Create the settings window
    settings_window = tk.Tk()
    settings_window.title("Edit Settings")

    # Input fields for start_time, end_time, and speed
    tk.Label(settings_window, text="Start Time (seconds)").grid(row=0, column=0)
    start_time_var = tk.StringVar(value=str(settings["start_time"]))
    tk.Entry(settings_window, textvariable=start_time_var).grid(row=0, column=1)

    tk.Label(settings_window, text="End Time (seconds)").grid(row=1, column=0)
    end_time_var = tk.StringVar(value=str(settings["end_time"]))
    tk.Entry(settings_window, textvariable=end_time_var).grid(row=1, column=1)

    tk.Label(settings_window, text="Speed (e.g., 1.0 for normal, 2.0 for double speed)").grid(row=2, column=0)
    speed_var = tk.StringVar(value=str(settings["speed"]))
    tk.Entry(settings_window, textvariable=speed_var).grid(row=2, column=1)

    # Save button
    tk.Button(settings_window, text="Save", command=save_and_close).grid(row=3, column=0, columnspan=2)

    # Start the GUI event loop
    settings_window.mainloop()

# Main function
def main():
    # File to store the settings
    settings_file = 'settings.json'  # Update this path as needed

    # Launch the settings editor GUI
    edit_settings_gui(settings_file)

    # Load updated settings after the user edits them
    settings = load_settings(settings_file)
    
    # Get the settings values
    start_time = settings.get("start_time", 0)
    end_time = settings.get("end_time", 10)
    speed = settings.get("speed", 1.0)

    # Select mp4 file
    file_path = select_file()
    
    if file_path:
        # Process the video
        process_video(file_path, start_time, end_time, speed)
    else:
        print("No file selected!")

if __name__ == "__main__":
    main()
