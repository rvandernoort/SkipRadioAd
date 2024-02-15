import pyaudio
import wave

# Set the duration of the recording in seconds
duration = 10

# Set the output file path
output_file = "./recordings/test.wav"

# Create an instance of the PyAudio class
audio = pyaudio.PyAudio()

# Set the audio parameters
format = pyaudio.paInt16
channels = 1
sample_rate = 44100
frames_per_buffer = 1024

# Open a new stream for recording
stream = audio.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=frames_per_buffer)

# Start recording
print("Recording started...")
frames = []
for i in range(0, int(sample_rate / frames_per_buffer * duration)):
    data = stream.read(frames_per_buffer)
    frames.append(data)

# Stop recording
print("Recording stopped...")

# Close the stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio instance
audio.terminate()

# Save the recorded audio to a WAV file
with wave.open(output_file, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))

print("Recording saved to", output_file)