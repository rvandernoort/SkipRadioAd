import pyaudio
import numpy as np
from scipy import signal

# Function to compare audio streams
def detect_sound(stream_data, sound_data):
    # Perform cross-correlation
    max_correlation = -np.inf
    best_lag = 0
        
    # Iterate over different lag values using sliding windows
    for lag in range(len(stream_data) - len(sound_data) + 1):
        # Extract a window of data from the audio stream
        window_data = stream_data[lag:lag+len(sound_data)]
        
        # Perform cross-correlation between the window and the target sound
        correlation = np.correlate(window_data, sound_data)
        
        # Update maximum correlation and corresponding lag if necessary
        if correlation > max_correlation:
            max_correlation = correlation
            best_lag = lag
    
    print("Max correlation:", max_correlation)
    
    # Adjust threshold as needed
    threshold = 1000000
    
    # If maximum correlation exceeds threshold, ding is detected
    if max_correlation > threshold:
        return True
    else:
        return False

def listen_for_sound(callback, target_sound, threshold=1000, duration=5, sample_rate=44100):
    chunk_size = int(sample_rate * duration)
    p = pyaudio.PyAudio()
    sound_data = np.fromfile(target_sound, dtype=np.int16)

    def callback_wrapper(in_data, frame_count, time_info, status):
        # Read audio data from stream
        stream_data = np.frombuffer(in_data, dtype=np.int16)
        
        # Check if ding sound is detected
        if detect_sound(stream_data, sound_data):
            callback()
        return (in_data, pyaudio.paContinue)

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size,
                    stream_callback=callback_wrapper)

    print("Listening for sound...")

    try:
        stream.start_stream()
        while stream.is_active():
            pass
    except KeyboardInterrupt:
        print("Stopping listening...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# Example callback function
def my_callback():
    print("Target sound detected!")

# Example usage
if __name__ == "__main__":
    target_sound = "./indicators/nporadio2_ster.wav"  # Replace this with your specific sound
    listen_for_sound(my_callback, target_sound)