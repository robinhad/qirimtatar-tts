import gradio as gr
from crh_transliterator.transliterator import transliterate
from crh_preprocessor.preprocessor import preprocess


def tts(text: str) -> str:
    text = transliterate(text)
    text = preprocess(text)
    return text


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
)
iface.launch()
