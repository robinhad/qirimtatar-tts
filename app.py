from os import getenv
from queue import Queue
from threading import Thread
from time import sleep
from data_logger import log_data
import gradio as gr
from crh_transliterator.transliterator import transliterate
from crh_preprocessor.preprocessor import preprocess
from datetime import datetime

import tempfile
import gradio as gr
from datetime import datetime
from enum import Enum
from crh_tts.tts import TTS, Voices
from torch.cuda import is_available


class VoiceOption(Enum):
    Sevil = "Севіль (жіночий) 👩"
    #Arslan = "Арслан (чоловічий) 👨"
    Eskander = "Ескандер (чоловічий) 👨"
    # Abibulla = "Абібулла (чоловічий) 👨"


def check_thread(logging_queue: Queue):
    logging_callback = log_data(hf_token=getenv("HF_API_TOKEN"), dataset_name="crh-tts-output", private=False)
    while True:
        sleep(60)
        batch = []
        while not logging_queue.empty():
            batch.append(logging_queue.get())

        if len(batch) > 0:
            try:
                logging_callback(batch)
            except:
                print("Error happened while pushing data to HF. Puttting items back in queue...")
                for item in batch:
                    logging_queue.put(item)

if getenv("HF_API_TOKEN") is not None:
    log_queue = Queue()
    t = Thread(target=check_thread, args=(log_queue,))
    t.start()

print(f"CUDA available? {is_available()}")


badge = (
    "https://visitor-badge-reloaded.herokuapp.com/badge?page_id=robinhad.qirimtatar-tts"
)

crh_tts = TTS(use_cuda=is_available())


def tts(text: str, voice: str):
    print("============================")
    print("Original text:", text)
    print("Voice", voice)
    print("Time:", datetime.utcnow())

    voice_mapping = {
        VoiceOption.Sevil.value: Voices.Sevil.value,
        #VoiceOption.Arslan.value: Voices.Arslan.value,
        VoiceOption.Eskander.value: Voices.Eskander.value,
        #VoiceOption.Abibulla.value: Voices.Abibulla.value,
    }

    speaker_name = voice_mapping[voice]
    if getenv("HF_API_TOKEN") is not None:
        log_queue.put([text, speaker_name, str(datetime.utcnow())])
    text_limit = 7200
    text = (
        text if len(text) < text_limit else text[0:text_limit]
    )  # mitigate crashes on hf space
    result = transliterate(text)
    text = preprocess(result)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
        _, text = crh_tts.tts(text, speaker_name, fp)
        return fp.name, text


with open("README.md") as file:
    article = file.read()
    article = article[article.find("---\n", 4) + 5 : :]


iface = gr.Interface(
    fn=tts,
    inputs=[
        gr.components.Textbox(
            label="Input",
            value="Qırımtatarlar! Селям! Ишлер насыл?",
        ),
        gr.components.Radio(
            label="Голос",
            choices=[option.value for option in VoiceOption],
            value=VoiceOption.Sevil.value,
        ),
    ],
    outputs=[
        gr.components.Audio(label="Output"),
        gr.components.Textbox(label="Оброблений текст"),
    ],
    title="Кримськотатарський синтез мовлення",
    description="Кримськотатарський Text-to-Speech за допомогою Coqui TTS",
    article=article + f'\n  <center><img src="{badge}" alt="visitors badge"/></center>',
    examples=[
        ["Selâm! İşler nasıl?", VoiceOption.Eskander.value],
        [
            "Qırımtatarlar üç subetnik gruppasından er birisiniñ (tatlar, noğaylar ve yalıboylular) öz şivesi bar.",
            VoiceOption.Sevil.value,
        ],
        ["Селям! Ишлер насыл?", VoiceOption.Sevil.value],
        ["Selâm! 123456789", VoiceOption.Eskander.value],
    ],
)
iface.launch()
