import sounddevice as sd
import soundfile as sf
import numpy as np
import keyboard
from tkinter import filedialog, Tk

FRAMES = 44100


# Ideally we would want to use pygame to open a file browser, but this is an implementation in TK (which is included
# in the python). Though this should be sufficient because it just opens the system's default file browser
def get_path():
    """Creates dialog to save file"""
    root = Tk()
    root.withdraw()
    path = filedialog.asksaveasfilename(filetypes=(("WAV", "*.wav"), ("all files", "*.*")), defaultextension='.wav')

    return path


def save(filename, file):
    """Persists recording in WAV format"""
    sf.write(filename, file, FRAMES)

# Function is now set up to return one second chunks to add to np array. The idea is that in the gui it will be controlled by a button that toggles a boolean to determine if it will break out of the recording loop
def record():
    """Opens stream to record from system's default microphone. Records 1 second at a time"""
    try:
        r = sd.rec(frames=FRAMES, samplerate=FRAMES, channels=2)
        sd.wait()
    except KeyboardInterrupt:
        print('User Interrupt')
        return r
    except Exception as e:
        print(type(e).__name__ + ' -> ' + str(e))

    return r


def main():
    recording = np.empty([FRAMES, 2])
    while True:
        recording= np.concatenate((recording, record()))
        # Press q to stop the recording
        if keyboard.is_pressed('q'):
            sd.stop()
            break

    save(get_path(), recording)


if __name__ == '__main__':
    main()
