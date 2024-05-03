import curses
from sclib import SoundcloudAPI, Track, Playlist
from pygame import mixer
import sys
from progressBar import ProgressBar

links = []

window = curses.initscr()

dims = window.getmaxyx()
window.keypad(1)
curses.start_color()
curses.use_default_colors()
curses.noecho()
curses.curs_set(False)

tracklist = []
trackIndex = 0
paused = False

for arg in sys.argv:
    links.append(str(arg))

def main():
    inputKey:str = ""
    global trackIndex

    mixer.init() # Initialzing pyamge mixer

    playTrack(tracklist[0])

    while str(inputKey) != "Q":
        windowDisplay()

        # Get input
        inputKey = window.getkey()

        # Handling input
        if inputKey == "KEY_RIGHT":
            nextTrack()
        elif inputKey == "KEY_LEFT":
            previusTrack()
        elif inputKey == " ":
            pause()
    exit()

def windowDisplay():
    # Clear window
    window.clear()
    window.box()

    # Display Stuff
    userInterface(tracklist[trackIndex])

    # Refresh After Display
    window.refresh()

def pause():
    global paused

    if(not paused):
        progressBar.pause()
        mixer.music.pause()
    else:
        progressBar.resume()
        mixer.music.unpause()
    
    paused = not paused

def playTrack(track:Track): # Donwnloading and setting up a process to play the track
    global trackIndex

    progressBar.duration = tracklist[trackIndex].duration
    progressBar.reset()

    artist:str = track.artist
    artist = artist.replace('/', '')

    title:str = track.title
    title = title.replace('/', '')

    filename = f'./{artist} - {title}.mp3'
    windowDisplay()

    progressBar.start()

    with open(filename, 'wb+') as file:
        track.write_mp3_to(file)

        mixer.music.load(filename) # Loading Music File
        mixer.music.play()


def nextTrack():
    global trackIndex

    if trackIndex < len(tracklist)-1:  # Check if there's a next track
        trackIndex += 1
        playTrack(tracklist[trackIndex])

def previusTrack():
    global trackIndex

    if trackIndex > 0:
        trackIndex -= 1
        playTrack(tracklist[trackIndex])


def displayOnCenter(message:str, offsetX=0, offsetY=0):
    window.addstr(
        int(int(dims[0])/2-1) + offsetY, 
        int(int(dims[1]/2)) - int(len(message)/2) + offsetX, 
        message
    )

def displayOnBottom(message:str, offsetX=0, offsetY=0):
    window.addstr(
        int(int(dims[0])) + offsetY, 
        int(int(dims[1]/2)) - int(len(message)/2) + offsetX, 
        message
    )

def loadPlaylist():
    api = SoundcloudAPI()

    for link in links:
        playlist = api.resolve(link)

        if type(playlist) is Playlist:
            for track in playlist.tracks:
                tracklist.append(track)
        elif type(playlist) is Track:
            tracklist.append(playlist)

def userInterface(track:Track): # Displaying the track time, artist and name
    displayOnCenter(f'• {track.artist} - {track.title} •')
    
    uiStr = "◄◄  ❚❚  ►►"
    if paused:
        uiStr = "◄◄  ▶  ►►"

    displayOnBottom(uiStr, offsetY=-3)
    

def exit():
    curses.endwin()
    sys.exit(0)

if __name__ == "__main__":
    displayOnCenter("Loading Playlist...")
    window.refresh()
    links.pop(0) # remove the first argument
    loadPlaylist()
    progressBar = ProgressBar(
        window=window,
        callback=nextTrack
    )
    try:
        main()
    finally:
        exit()