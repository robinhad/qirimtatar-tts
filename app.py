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
    Nuri = "Севіль (жіночий) 👩"
    Arslan = "Арслан (чоловічий) 👨"
    Kemal = "Ескандер (чоловічий) 👨"
    Abibulla = "Абібулла (чоловічий) 👨"


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
        VoiceOption.Nuri.value: Voices.Nuri.value,
        VoiceOption.Arslan.value: Voices.Arslan.value,
        VoiceOption.Kemal.value: Voices.Kemal.value,
        VoiceOption.Abibulla.value: Voices.Abibulla.value,
    }

    speaker_name = voice_mapping[voice]
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
            value=VoiceOption.Nuri.value,
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
        ["Selâm! İşler nasıl?", VoiceOption.Kemal.value],
        [
            "Qırımtatarlar üç subetnik gruppasından er birisiniñ (tatlar, noğaylar ve yalıboylular) öz şivesi bar.",
            VoiceOption.Arslan.value,
        ],
        ["Селям! Ишлер насыл?", VoiceOption.Nuri.value],
        ["Selâm! 123456789", VoiceOption.Abibulla.value],
    ],
)
iface.launch()
