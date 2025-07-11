import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["USE_CUDA"] = "0"
os.environ["TORCH_CUDA_VERSION"] = "0"
try:
    import torch
    torch.cuda.is_available = lambda : False
    torch.cuda.device_count = lambda : 0
    torch.cuda.current_device = lambda : 0
    torch.cuda._initialized = True
except Exception:
    pass

import orpheus_tts

def speak(text):
    try:
        orpheus_tts.speak(text)
    except Exception as e:
        print(f"[Orpheus TTS] Error: {e}")
