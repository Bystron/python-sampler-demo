import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import os

# Define the folder path where your audio samples are located
folder_path = input("Welcome to python-sampler! please locate your sample Folder:")

# Load the audio samples
s = 0
samples = []
for file_name in os.listdir(folder_path):
    if file_name.endswith(".wav"):
        file_path = os.path.join(folder_path, file_name)
        data, sample_rate = sf.read(file_path)
        print(file_name+" Loaded as Audio Sample!") #Needs to also tell the sample slot
        s += 1
        samples.append(data)

# Set the tempo and number of bars
tempo = input("BPM:") # beats per minute
bars = input("Number of Bars:") #Default is 8

# Calculate the duration of a single bar in seconds
bar_duration = 60.0 / tempo

# Define the sequence of sample indices, pitch shifts, and speed factors for each bar
sequence = []

i = 1
while i < bars:
   sample_index = input(i+" Sample_index(EJ. 0, 1, 2...):")
   pitch_shift = input(i+" pitch_shift(Can use Negative Numbers):")
   speed_factor= input(i+" Sample_index (Can use Decimals):")
   sequence[i] = (sample_index, pitch_shift, speed_factor) #Not working correclty
   i += 1

# Initialize the start time
start_time = time.time()

# Run the sequencer loop
while True:
    # Calculate the elapsed time in seconds
    elapsed_time = time.time() - start_time

    # Calculate the current bar index
    current_bar = int(elapsed_time / bar_duration) % bars

    # Get the current sequence entry for the current bar
    current_entry = sequence[current_bar]

    # Extract the sample index, pitch shift, and speed factor
    sample_index, pitch_shift, speed_factor = current_entry

    # Get the current audio sample
    sample = samples[sample_index]

    # Resample the audio sample based on the speed factor
    resampled_sample = np.interp(
        np.arange(0, len(sample), speed_factor),
        np.arange(0, len(sample)),
        sample
    )

    # Apply the pitch shift to the resampled sample
    pitch_shifted_sample = np.roll(resampled_sample, pitch_shift)

    # Play the audio sample
    sd.play(pitch_shifted_sample, samplerate=sample_rate, blocking=False)

    # Calculate the time to sleep until the next beat
    sleep_time = bar_duration - (elapsed_time % bar_duration)

    # Sleep until the next beat
    time.sleep(sleep_time)
