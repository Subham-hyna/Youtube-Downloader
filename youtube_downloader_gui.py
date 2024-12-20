import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
from pytubefix import YouTube
from pytubefix.cli import on_progress
import time

## Functions
def choose_output():
    save_dir_button["state"] = 'normal'

def choose_folder():
    folder = filedialog.askdirectory(initialdir="/")

    if folder:
        dir_string.set(value = folder)
        download_button["state"] = 'normal'

def reset():
    url_string.set(value="")
    successful_download.pack_forget()

def successful():
    download_button["state"] = "normal"
    url_reset_button["state"] = "enable"
    url_string.set(value="")
    time.sleep(5)
    successful_download.pack_forget()

def Download():
    download_button["state"] = "disable"
    url_reset_button["state"] = "disable"
    link = url_string.get()
    save_path = dir_string.get()
    output = ch_string.get()

    while True:
        if link.strip() == "":
            continue
        else:
            break 

    youtubeObject = YouTube(link, on_progress_callback=on_progress)
    if output == "audio":
        stream = youtubeObject.streams.filter(only_audio=True)[1]
        try:
            print("Download Started")
            stream.download(filename=f"{youtubeObject.title}.mp3", output_path=save_path) 
            print(f"{output} Dowloaded Successfully") 
            successful_download.pack()
        except Exception as e:
            print("An error has occurred ", e)
    elif output == "video":
        stream = youtubeObject.streams.filter(progressive=True,file_extension='mp4')
        highest_res_stream = stream.get_highest_resolution()
        try:
            print("Dowload Started")
            highest_res_stream.download(output_path=save_path) 
            print(f"{output} Dowloaded Successfully") 
            successful_download.pack()
        except Exception as e:
            print("An error has occurred ", e)
    
    download_button["state"] = "normal"
    url_reset_button["state"] = "enable"
    url_string.set(value="")
    time.sleep(5)
    successful_download.pack_forget()
    
        

## Window
window = ttk.Window(themename="lumen")
window.title("Youtube Video Downloader")
window.minsize(550,400)

## Variable
ch_string = tk.StringVar()
url_string = tk.StringVar()
dir_string = tk.StringVar()

## Widgets
header_label = ttk.Label(master=window, font=('verdana' , 30, 'bold'), text="Youtube Video Downloader",bootstyle= 'danger')

frame1 = ttk.Frame(master=window)
ch_audio = ttk.Radiobutton(master=frame1, text='Audio Output', bootstyle='success', value='audio', variable=ch_string, command=choose_output)
ch_video = ttk.Radiobutton(master=frame1, text='Video Output', bootstyle='success', value='video', variable=ch_string, command=choose_output)

url_entry_label = ttk.Label(master=window, text="Enter Video Url")
frame3 = ttk.Frame(master=window)
url_entry = ttk.Entry(master=frame3, bootstyle="success", textvariable=url_string, width=40)
url_reset_button = ttk.Button(master=frame3,text="Reset", bootstyle="info-outline", command=reset)

save_dir_label = ttk.Label(master=window, text="Please select a folder to download", bootstyle="warning")
frame2 = ttk.Frame(master=window)
save_dir_entry = ttk.Entry(master=frame2, textvariable=dir_string, state='disable')
save_dir_button = ttk.Button(master=frame2, text="Select Folder", bootstyle="success-outline", command=choose_folder, state='disable')

download_button = ttk.Button(master=window, text="Download", bootstyle="success", command=Download, state='disable')
successful_download = ttk.Label(master=window, text="Downloaded Successfully")

## Layout
header_label.pack(padx=(20,20), pady=(40,20))
url_entry_label.pack()
frame3.pack(pady=(0,20))
url_entry.pack(pady=(0,20))
url_reset_button.pack(side="right")
frame1.pack(pady=(0,20))
ch_audio.pack(side="left", padx=(0, 20))
ch_video.pack()
save_dir_label.pack()
frame2.pack(pady=(5,20))
save_dir_entry.pack(side="left", padx=(0, 20))
save_dir_button.pack()
download_button.pack(pady=(0,20))


## Run
window.mainloop()