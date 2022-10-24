import gradio as gr
from crh_transliterator.transliterator import transliterate
from crh_preprocessor.preprocessor import preprocess


def tts(text: str) -> str:
    text = transliterate(text)
    text = preprocess(text)
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
