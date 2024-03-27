import tkinter as tk
from tkinter import filedialog
import subprocess
import os

class AudioVideoCombinerApp:
    def __init__(self, root):
        self.root = root
        root.title("Audio Video Combiner")

        tk.Label(root, text="Select Audio Files:").pack()
        self.audio_files_listbox = tk.Listbox(root, selectmode=tk.EXTENDED, width=50, height=10)
        self.audio_files_listbox.pack()
        tk.Button(root, text="Add Audio Files", command=self.add_audio_files).pack()

        tk.Label(root, text="Select Background Image:").pack()
        self.background_image_entry = tk.Entry(root)
        self.background_image_entry.pack()
        tk.Button(root, text="Browse", command=self.browse_background_image).pack()

        tk.Label(root, text="Output Video File:").pack()
        self.output_video_entry = tk.Entry(root)
        self.output_video_entry.pack()
        tk.Button(root, text="Browse", command=self.browse_output_video).pack()

        tk.Button(root, text="Combine and Create Video", command=self.combine_audio_video).pack()

    def add_audio_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio files", "*.mp3")])
        for file in files:
            self.audio_files_listbox.insert(tk.END, file)

    def browse_background_image(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        self.background_image_entry.delete(0, tk.END)
        self.background_image_entry.insert(0, file)

    def browse_output_video(self):
        file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 file", "*.mp4")])
        self.output_video_entry.delete(0, tk.END)
        self.output_video_entry.insert(0, file)

    def combine_audio_video(self):
        audio_files = self.audio_files_listbox.get(0, tk.END)
        background_image = self.background_image_entry.get()
        output_video = self.output_video_entry.get()

        with open("filelist.txt", "w") as filelist:
            for audio_file in audio_files:
                filelist.write(f"file '{audio_file}'\n")

        subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", "filelist.txt", 
            "-c", "copy", "combined.mp3"
        ])

        subprocess.run([
            "ffmpeg", "-loop", "1", "-i", background_image, "-i", "combined.mp3",
            "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
            "-vf", "scale=1920:1080", "-pix_fmt", "yuv420p", "-shortest", output_video
        ])

        os.remove("combined.mp3")  # Clean up intermediate file
        os.remove("filelist.txt")  # Clean up file list

        tk.messagebox.showinfo("Success", "The video has been created successfully.")

root = tk.Tk()
app = AudioVideoCombinerApp(root)
root.mainloop()
