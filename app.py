from unittest import result
import gradio as gr
from crh_transliterator.transliterator import transliterate
from crh_preprocessor.preprocessor import preprocess
from datetime import datetime


def tts(text: str) -> str:
    result = transliterate(text)
    text = preprocess(result)
    print("============================")
    print("Original text:", text)
    print("Time:", datetime.utcnow())
    return text


badge = (
    "https://visitor-badge-reloaded.herokuapp.com/badge?page_id=robinhad.qirimli-tts"
)

with open("README.md") as file:
    article = file.read()
    article = article[article.find("---\n", 4) + 5 : :]

iface = gr.Interface(
    fn=tts,
    inputs=[
        gr.components.Textbox(
            label="Input",
            value="Please input your sentence.",
        ),
    ],
    outputs="text",
    examples=[
        ["Selâm! İşler nasıl?"],
        ["Sağlıqnen qalıñız! Sağlıqnen barıñız! "],
        ["Селям! Ишлер насыл?"],
    ],
    article=article + f'\n  <center><img src="{badge}" alt="visitors badge"/></center>',
)
iface.launch()
