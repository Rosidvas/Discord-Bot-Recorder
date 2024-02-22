
import pyaudio

async def recordVoiceChat(voice_client, output_file, duration=60):
    
    if voice_client:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)

        frames = []
        for _ in range(int(44100 / 1024 * duration)):
            frames.append(stream.read(1024))
    
        stream.stop_stream()
        stream.close()
        p.terminate()

        with open(output_file, 'wb') as f:
            for frame in frames:
                f.write(frame)
    

    
    
    
