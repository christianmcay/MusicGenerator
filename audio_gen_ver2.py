import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

class AudioProcessing:
    def __init__(self, sample_rate, frequency, duration, amplitude):
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.duration = duration
        self.amplitude = amplitude

    def generate_sine_wave(self):
        num_samples = int(self.sample_rate * self.duration)
        samples = np.arange(num_samples)
        waveform = self.amplitude * np.sin(2 * np.pi * self.frequency * samples / self.sample_rate)
        return waveform.astype(np.int16)
    
    def generate_square_wave(self):
        num_samples = int(self.sample_rate * self.duration)
        samples = np.arange(num_samples)
        w = 2 * np.pi * self.frequency
        square_wave = 0
        for index in range(1, 300, 2):  
            square_wave += (1/index) * np.sin(index * w * (samples / self.sample_rate))
        square_wave = self.amplitude * (4/np.pi) * square_wave
        return square_wave.astype(np.int16)

    def generate_triangle_wave(self):
        num_samples = int(self.sample_rate * self.duration)
        samples = np.arange(num_samples)
        w = 2 * np.pi * self.frequency
        triangle_wave = 0
        for index in range(1, 300, 1):  
            triangle_wave += (((-1)**index)/((2*index-1)**2)) * np.sin((2* index - 1) * w * (samples / self.sample_rate))
        triangle_wave = self.amplitude * (-1) * (8/(np.pi**2)) * triangle_wave
        return triangle_wave.astype(np.int16)

    def generate_sawtooth_wave(self):
        num_samples = int(self.sample_rate * self.duration)
        samples = np.arange(num_samples)
        w = 2 * np.pi * self.frequency
        sawtooth_wave = 0
        for index in range(1, 300, 1):
            sawtooth_wave += ((-1)**index / index) * np.sin(w * index * (samples / self.sample_rate))
        sawtooth_wave = self.amplitude *(-2/np.pi) * sawtooth_wave
        return sawtooth_wave.astype(np.int16)

    def plot_waveform(self, waveform):
        time = np.linspace(0, self.duration, len(waveform))
        plt.figure()
        plt.plot(time, waveform)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Waveform')
        plt.show()

NOTE_FREQUENCIES = np.array([27.50, 29.14, 30.87,
                            32.70, 34.65, 36.71, 
                            38.89, 41.20, 43.65, 
                            46.25, 49.00, 51.91,
                            55.00, 58.27, 61.74,
                            65.41, 69.30, 73.42, 
                            77.78, 82.41, 87.31, 
                            92.50, 98.00, 103.83,
                            110.00, 116.54, 123.47,
                            130.81, 138.59, 146.83, 
                            155.56, 164.81, 174.61, 
                            185.00, 196.00, 207.65,
                            220.00, 233.08, 246.94,
                            261.63, 277.18, 293.66, 
                            311.13, 329.63, 349.23, 
                            369.99, 392.00, 415.30,
                            440.00, 466.16, 493.88,
                            523.25, 554.37, 587.33, 
                            622.25, 659.25, 698.46, 
                            739.99, 783.99, 830.61,
                            880.00, 932.33, 987.77,
                            1046.50, 1108.73, 1174.66, 
                            1244.51, 1318.51, 1396.91, 
                            1479.98, 1567.98, 1661.22,
                            1760.00, 1864.66, 1975.53,
                            2093.00, 2217.46, 2349.32, 
                            2489.02, 2637.02, 2793.83, 
                            2959.96, 3135.96, 3322.44,
                            3520.00, 3729.31, 3951.07,
                            4186.01])

SCALES = {"major": [2, 2, 1, 2, 2, 2, 1, 0], "minor": [2, 1, 2, 2, 1, 2, 2, 0]}

def generate_scale_waveform(start_freq, scale_type, sample_rate=44100, duration=1, amplitude=25000):
    start_freq_index = np.where(NOTE_FREQUENCIES == start_freq)[0][0]
    waveform = np.array([], dtype=np.int16)
    for scale_jump in SCALES[scale_type]:
        if start_freq_index >= len(NOTE_FREQUENCIES):
            break
        freq = NOTE_FREQUENCIES[start_freq_index]
        audio = AudioProcessing(sample_rate, freq, duration, amplitude)
        sq_wave = audio.generate_sine_wave()
        waveform = np.append(waveform, sq_wave)
        start_freq_index += scale_jump
    return waveform

start_freq = np.random.choice(NOTE_FREQUENCIES)
print(f"Start freq: {start_freq}")

major_waveform = generate_scale_waveform(start_freq, "major")
minor_waveform = generate_scale_waveform(start_freq, "minor")

write(f'{start_freq}_major_scale.wav', 44100, major_waveform)
write(f'{start_freq}_minor_scale.wav', 44100, minor_waveform)
