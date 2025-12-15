import pyaudio
import wave
import os
from vosk import Model, KaldiRecognizer
import json
import pyttsx3
import whisper
import threading

whisper_model = whisper.load_model("base")
def speak(text):
    def run_speech():
        engine = pyttsx3.init()
        engine.setProperty("rate", 180)   
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    
    threading.Thread(target=run_speech, daemon=True).start()
def start_listening_thread(command=None,callback=None):
    def thread_target():
        result = listen_for_selection(command)
        if callback:
            callback(result)

    threading.Thread(target=thread_target, daemon=True).start()

def listen_for_selection(command=None): 
    RATE = 16000
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    MODEL_PATH = "C:\\vosk-model-small-en-us-0.15"
    info = None
    if not os.path.exists(MODEL_PATH):
        raise Exception(f"Vosk model not found at '{MODEL_PATH}'. Download and unpack it first.")

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, RATE)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    done = False
    try:
        while not done:
            data = stream.read(CHUNK, exception_on_overflow = False)
            frames.append(data)
            
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                j = json.loads(result)
                text = j.get("text", "").lower()
                if text:
                    print("Heard:", text)
                if(command=="done"):
                    if "done" in text.split():
                        done = True
                        info = text
                        break
                if(command=="Send Email"):
                    if "send" in text.split():
                        done = True
                        info = "send email"
                        break
                    if "email" in text.split():
                        done = True
                        info = "send email"
                        break  
                if(command=="Package Type"):
                    if "amazon" in text.split():
                        done = True
                        info = "amazon"
                        break
                    elif "ups" in text.split():
                        done = True
                        info = "ups"
                        break
                    elif "fedex" in text.split():
                        done = True
                        info = "fedex"
                        break
                    elif "usps" in text.split():
                        done = True
                        info = "usps"
                        break
                else:
                    if "package" in text.split():
                        print("Detected 'package'. Stopping.")
                        done = True
                        info = "packages"
                        break
                    elif "mail" in text.split():
                        print("Detected 'mail'. Stopping.")
                        done = True
                        info= "mails"
                        break
                    elif "exit" in text.split():
                        print("Detected 'exit'. Stopping.")
                        info = "exit"
                        done = True
                        break
                
            else:
                partial = json.loads(recognizer.PartialResult()).get("partial", "")
                pass

    except KeyboardInterrupt:
        print("Interrupted by user.")

    # clean up
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return info

def listen_for_info_thread(command, callback=None):
    def thread_target():
        result = listen_for_info(command)
        if callback:
            callback(result)

    threading.Thread(target=thread_target, daemon=True).start()
def listen_for_info(command):
    RATE = 16000
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    MODEL_PATH = "C:\\vosk-model-small-en-us-0.15"
    OUTPUT_FILENAME = "audio_until_done.wav"

    if not os.path.exists(MODEL_PATH):
        raise Exception(f"Vosk model not found at '{MODEL_PATH}'. Download and unpack it first.")

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, RATE)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    print("Listening... Say 'done' to stop recording.")

    frames = []
    done = False
    try:
        while not done:
            data = stream.read(CHUNK, exception_on_overflow = False)
            frames.append(data)
            
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                j = json.loads(result)
                text = j.get("text", "").lower()
                if text:
                    print("Heard:", text)
                if command in text.split():
                    print(f"Detected '{command}'. Stopping.")
                    done = True
                    break
                if "exit" in text.split():
                    print("Detected 'exit'. Stopping.")
                    done = True
                    return "exit"
            else:
                partial = json.loads(recognizer.PartialResult()).get("partial", "")
                pass

    except KeyboardInterrupt:
        print("Interrupted by user.")

    # clean up
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf = wave.open(OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    print(f"Saved recorded audio to {OUTPUT_FILENAME}")
    result = whisper_model.transcribe(OUTPUT_FILENAME)
    return result["text"]