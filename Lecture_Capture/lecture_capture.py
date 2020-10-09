import sounddevice as sd
import soundfile as sf
import numpy as np

FRAMES = 44100

def save(filename, file):
    sf.write(filename, file, FRAMES)


def record():
    recording = np.empty([FRAMES,2])
    try:
        while True:
            r = sd.rec(frames=FRAMES, samplerate=FRAMES, channels=2)
            print(r.shape)
            sd.wait()
            recording = np.concatenate((recording, r))
            print(recording.shape)
    except KeyboardInterrupt:
        print('User Interrupt')
        return recording
    except Exception as e:
        print(type(e).__name__ + ' -> ' + str(e))

    return recording


def main():
    recording = record()

    save("recording.wav", recording)


if __name__ == '__main__':
    main()
