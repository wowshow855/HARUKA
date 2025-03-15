# HARUKA
H.A.R.U.K.A. – Helpful Assistant for Real-time, User &amp; Knowledge Assistance. HARUKA is a simple to use LLM manager based on Ollama which also supports adding personality! Simply install the program, follow the 3 step instructions, and chat away! In the future HARUKA is also planned to be able to interact with custom python scripts and have a customization 3D VRM model.
HARUKA is designed to be:

- Simple to use, modify, deploy.
- Minimal requirements
- Open Source
- Completely free!
- Multiplatform (Windows, MacOS, Linux)

HARUKA is designed to be nearly 100% in python.
# INSTALLATION

## Basic requirements:
HARUKA only requires 3 programs!

- Python 3.10.11 Recommened but other versions *may* work (https://www.python.org/downloads/release/python-31011/)
- Ollama (https://ollama.com/)
- Torch (Instructions below)

### Installing an LLM for HARUKA

HARUKA supports EVERY LLM compatible on Ollama. The default recommended model is "dolphin3". Find models on https://ollama.com/search to use other models on Hugging Face for example consult a Youtube tutorial.

To install a model:
```
ollama pull dolphin3
```

### Install libraries with pip

In your system CLI (CMD, Powershell, MacOS Terminal, Linux Command line)

Copy and paste this command to install libraries:
```
pip install sounddevice, soundfile, kokoro, numpy, dotenv, speechrecognition
```

### Install Torch:

If you have an NVIDIA GPU:

1. Install CUDA 12.6 from https://developer.nvidia.com/cuda-12-6-0-download-archive

2. Scroll down and get command from https://pytorch.org/ select your cuda version and run it

Example:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

If you do not have an NVIDIA GPU:

Scroll down and get command from https://pytorch.org/ select CPU and run it

Example:
```
pip install torch torchvision torchaudio
```

If you are on Linux and have an AMD GPU you can use ROCm:

Scroll down and get command from https://pytorch.org/ select your cuda version and run it

Example:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2.4
```


## Running the program

### Quickly set up in 3 easy steps!

1. Download the repo.
2. Run "main.py"
3. Follow instruction and enjoy!
## About .env File Modifications

In the .env file there are the following default variables:

```
llm_model='dolphin3'
context_file="context.txt"
max_context_size="10485760"
personality_file="personality.txt"
htoken_file="htoken.txt"
USE_PERSONALITY='1'
use_mic='0'
```

llm_model = You can select the LLM used for HARUKA

context_file = context file name

max_context_size = the max size context file can be

personality_file = personality file name

htoken_file = future feature (HARUKA TOKEN)

USE_PERSONALITY = 1 for yes, 0 for no

use_mic = 1 for yes, 0 for no

