import pyaudio
import wave
import datetime
import time
import os

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 976  # 2 minutes before and 14 minutes after (16 minutes total)
OUTPUT_DIR = "recordings"

# Function to record audio
def record_audio(stream, frames):
    print("Recording audio...")
    for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

try:
    while True:
        # Get current time
        now = datetime.datetime.now()
        
        # Calculate the target time (2 minutes before the next full hour)
        target_time = now.replace(second=0, microsecond=0)
        target_time = target_time.replace(minute=58)
        
        print("Waiting until {} to start recording...".format(target_time))
        
        # Wait until target time
        while datetime.datetime.now() < target_time:
            time.sleep(1)

        # Start recording
        frames = []
        record_audio(stream, frames)

        # Generate unique file name based on timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = os.path.join(OUTPUT_DIR, f"audio_capture_{timestamp}.wav")

        # Save recorded audio to file
        wf = wave.open(file_name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("Audio saved to '{}'".format(file_name))

except KeyboardInterrupt:
    print("Recording interrupted")

finally:
    # Close stream
    stream.stop_stream()
    stream.close()
    audio.terminate()