logo = (r"""
      _    _          _____  _    _ _  __          
     | |  | |   /\   |  __ \| |  | | |/ /    /\    
     | |__| |  /  \  | |__) | |  | | ' /    /  \   
     |  __  | / /\ \ |  _  /| |  | |  <    / /\ \  
     | |  | |/ ____ \| | \ \| |__| | . \  / ____ \ 
     |_|  |_/_/    \_\_|  \_\\____/|_|\_\/_/    \_\
    """)

import asyncio
import subprocess
import re
import sys
import sounddevice as sd
import soundfile as sf
import time
from kokoro import KPipeline
import os
import numpy as np
from dotenv import load_dotenv, set_key
import speech_recognition as sr

load_dotenv()

clear = lambda: os.system('cls')
            
#env file setup
llm_model = os.getenv('llm_model')
context_file = os.getenv('context_file')
max_context_size = int(os.getenv('max_context_size', 10485760))
personality_file = os.getenv('personality_file')
htoken_file = os.getenv('htoken_file')
use_personality = os.getenv('use_personality')
use_mic = os.getenv('use_mic')

#load personality
personality = ""
if os.path.exists(personality_file):
    with open(personality_file, 'r', encoding='utf-8') as f:
        personality = f.read()

#load htoken
htoken = ""
if os.path.exists(htoken_file):
    with open(htoken_file, 'r', encoding='utf-8') as f:
        htoken = f.read()

# first time set up
def firsttime():
    if not os.path.exists(context_file):
        print('No context file found. Entering setup...')
        with open(context_file, "w", encoding='utf-8') as f:
            f.write("")
        
        while True:
            print("\nWELCOME TO HARUKA SETUP! Would you like to (can be edited later in .env):")
            print("1. Use personality file (default)")
            print("2. Do not use the personality file")
            choice = input("Enter 1 or 2: ").strip()

            if choice == "1":
                set_key('.env', 'USE_PERSONALITY', '1')
                print("Personality file will be injected into the prompt.")
            elif choice == "2":
                set_key('.env', 'USE_PERSONALITY', '0')
                print("Personality file will not be used.")
            else:
                print("Invalid input, try again.")

            print("\Would you like to (can be edited later in .env):")
            print("1. Use mic (default)")
            print("2. Disable mic")
            choice = input("Enter 1 or 2: ").strip()
            
            if choice == "1":
                set_key('.env', 'use_mic', '1')
                print("Microphone will be used.")
                return True
            elif choice == "2":
                set_key('.env', 'use_mic', '0')
                print("Text input will be used instead.")
                return False
            else:
                print("Invalid input, try again.")


def load_context():
    if os.path.exists(context_file):
        with open(context_file, "r", encoding='utf-8') as f:
            return f.read()
    return ""

def save_context(context):
    if len(context.encode('utf-8')) > max_context_size:
        context = context[-max_context_size:]  # file limit
    
    with open(context_file, "w", encoding='utf-8') as f:
        f.write(context)

# kokoro setup
pipeline = KPipeline(lang_code='a')

async def generate_text_with_ollama(prompt: str) -> str:
    process = await asyncio.create_subprocess_exec(
        'ollama', 'run', llm_model, prompt,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        response = stdout.decode('utf-8').strip()

        # shit to make it compatible with llm w/ reasoning models
        # Extract think
        think_match = re.search(r'<think>(.*?)</think>', response, re.DOTALL)
        think_part = think_match.group(1).strip() if think_match else ""

        # The answer part
        answer_part = response.split('</think>', 1)[-1].strip()

        return think_part, answer_part

    return "", ""

def listen_for_wake_word(spoken_text):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for 'Hey Haruka!'...")
        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio).lower()
                print("Heard:", text)
                
                if "hey haruka" in text:
                    print("Wake word detected! Start speaking...")
                    return listen_for_speech(spoken_text)
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("Speech Recognition service unavailable")
                return None

def listen_for_speech(spoken_text):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Recording...")
        audio = recognizer.listen(source)
        print("Processing...")
    
    try:
        spoken_text = recognizer.recognize_google(audio)
        print("You said:", spoken_text)
        return spoken_text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Speech Recognition service unavailable.")
        return ""

async def kokoro_generate_speech(text: str, output_file: str):
    try:
        # Initialize a list to store all audio data
        full_audio = []
        
        # Generate the speech with Kokoro
        generator = pipeline(
            text, voice='af_heart',  # Change voice here
            speed=1
        )
        
        for i, (gs, ps, audio) in enumerate(generator):
            # Append the generated audio to the full_audio list
            full_audio.append(audio)
        concatenated_audio = np.concatenate(full_audio, axis=0)
        # write audio
        sf.write(output_file, concatenated_audio, 24000)
    except Exception as e:
        print(f"Error generating speech: {e}")

def typingPrint(text: str, delay: float):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(delay)

async def main():

    clear()
    print(logo)
    typingPrint("Inspried by MITUSHA, V0.1.0\n", 0.05)
    typingPrint("Built for Speed, Ease, and Dweebs.\n", 0.05)
    firsttime()
    time.sleep(1)

    while(True):
        # Load the conversation context from the file
        context = load_context()
        
        prompt = ""
        if use_mic:
            listen_for_wake_word(prompt)
        else:
            prompt = input("Please input prompt: \n")
        if prompt == "quit":
            sys.exit(0)
    
        full_prompt = htoken + context + "\nUser: " + prompt + "\nAI:"

        if personality:
            full_prompt = personality + "\n" + full_prompt

        think_part, answer_part = await generate_text_with_ollama(full_prompt)
    
        if answer_part:
            if think_part != "":
                print("Think Part:", think_part)
            print("Answer Part:", answer_part)

            context += f"\nUser: {prompt}\nAI: {answer_part}"
            save_context(context)

            #delete ts tokens
            answer_part_audio = re.sub(r'\{.*?\}', '', answer_part)

            await kokoro_generate_speech(answer_part_audio, "output.wav")
            data, fs = sf.read("output.wav", dtype='float32')
            sd.play(data, fs)

if __name__ == "__main__":
    asyncio.run(main())