from tkinter import *
import os
import tkinter.messagebox 
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
from pygame import mixer
from mutagen.mp3 import MP3
import threading
import time

root = ThemedTk(theme="radiance")
root.geometry('750x356+230+160')

statusbar = ttk.Label(root, text = "Welcome to Melody", relief = SUNKEN, anchor = W, font = ("Courier New", 15, "italic bold")) 
statusbar.pack(side = BOTTOM, fill = X)

# create the menu bar
menubar = Menu(root)
root.config(menu=menubar)


# create the submenu
subMenu = Menu(menubar, tearoff=0)

playlist = []
# playlist = contains the full path + filename
# playlistbox = contains just the filename
# Fullpath + filename is required to play the music inside play_music load function 

def browse_file():
    global filename
    filename = filedialog.askopenfilename()
    add_to_playlist(filename)

    mixer.music.queue(filename)
                                            #### here filename refers to filename path and f refers to filename
def add_to_playlist(f):
    f = os.path.basename(f)
    index = 0
    playlistbox.insert(index, f)
    playlist.insert(index, filename)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command = browse_file)
subMenu.add_command(label="Exit", command = root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a music player build using python Tkinter by Nitesh Yadav')

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command = about_us)

mixer.init() # initializing the mixer


root.title("Melody")
root.iconbitmap(r"images/Melody.ico")

leftframe = Frame(root)
leftframe.pack(side = LEFT, padx = 30, pady = 30)

playlistbox = Listbox(leftframe, width =25)
playlistbox.pack()

add_btn = ttk.Button(leftframe, text = "+ Add", command = browse_file)
add_btn.pack(side = LEFT)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

del_btn = ttk.Button(leftframe, text = "_  Del", command = del_song)
del_btn.pack(side = LEFT)

rightframe = Frame(root)
rightframe.pack(pady = 25)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text = 'Total Length: --:--')
lengthlabel.pack(pady = 8)

currenttimelabel = ttk.Label(topframe, text = 'Current Time: --:--', relief = GROOVE)
currenttimelabel.pack()

def show_details(play_song):
    file_data = os.path.splitext(play_song)


    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins,secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel["text"] = "Total Length" + " - " + timeformat

    t1 = threading.Thread(target = start_count, args = (total_length,))
    t1.start()

def start_count(t):
    global paused
    # mixer.music.get_busy() : - Returns False when we press the stop button (music stops playing)
    # continue ignores all the statements below it. We check if music is paused or not 
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel["text"] = "Current Time" + " - " + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar["text"] = "Music Resumed"
        paused = False

    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar["text"] = "Playing music" + " " +  os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file, please check again.')



def stop_music():
    mixer.music.stop()
    statusbar["text"] = "Music Stopped"

paused = False

def pause_music():
    global paused 
    paused = True
    mixer.music.pause()
    statusbar["text"] = "Music Paused"

def rewind_music():
    play_music()
    statusbar["text"] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume) 
    # set_volume of mixer only takes value from 0 to 1 i.e 0,   0.1, 0.55, 0.65, 0.99, 1


muted = False


def mute_music():
    global muted
    if muted: # Unmute the music
        mixer.music.set_volume(0.7) 
        volumeBtn.configure(image = volumePhoto)
        scale.set(70)
        muted = False
    else: # mute the music
        mixer.music.set_volume(0) 
        volumeBtn.configure(image = mutePhoto)
        scale.set(0)
        muted = True

    
middleframe = Frame(rightframe)
middleframe.pack(pady = 20, padx = 30)


playPhoto = PhotoImage(file = "images/play.png")
playBtn = ttk.Button(middleframe, image = playPhoto, command = play_music)
playBtn.grid(row = 0, column = 0, padx = 10)


stopPhoto = PhotoImage(file = "images/stop-button.png")
stopBtn = ttk.Button(middleframe, image = stopPhoto, command = stop_music)
stopBtn.grid(row = 0, column = 1, padx = 10)


pausePhoto = PhotoImage(file = "images/pause.png")
pauseBtn = ttk.Button(middleframe, image = pausePhoto, command = pause_music)
pauseBtn.grid(row = 0, column = 2, padx = 10)


# bottom frame for volume, rewind, mute etc.
bottomframe = Frame(rightframe)
bottomframe.pack(pady = 20, padx = 30)

rewindPhoto = PhotoImage(file = "images/rewind.png")
rewindBtn = ttk.Button(bottomframe, image = rewindPhoto, command = rewind_music)
rewindBtn.grid(row = 0, column = 0)


mutePhoto = PhotoImage(file = "images/mute.png")
volumePhoto = PhotoImage(file = "images/speaker.png")
volumeBtn = ttk.Button(bottomframe, image = volumePhoto, command = mute_music)
volumeBtn.grid(row = 0, column = 1)


scale = ttk.Scale(bottomframe, from_ = 0, to = 100, orient = HORIZONTAL, command = set_vol)
scale.set(70) # implement the default value of scale when the music player starts
mixer.music.set_volume(0.7) 
scale.grid(row = 0, column = 2, pady = 15, padx = 30)

def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()