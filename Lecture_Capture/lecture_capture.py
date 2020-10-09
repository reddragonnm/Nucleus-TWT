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


def record():
    """Opens stream to record from system's default microphone. In its current state press q to quit recording"""
    recording = np.empty([FRAMES, 2])
    try:
        while True:
            r = sd.rec(frames=FRAMES, samplerate=FRAMES, channels=2)
            print(r.shape)
            sd.wait()
            recording = np.concatenate((recording, r))
            print(recording.shape)
            if keyboard.is_pressed('q'):
                sd.stop()
                break
    except KeyboardInterrupt:
        print('User Interrupt')
        return recording
    except Exception as e:
        print(type(e).__name__ + ' -> ' + str(e))

    return recording


def main():
    recording = record()
    save(get_path(), recording)


if __name__ == '__main__':
    main()
