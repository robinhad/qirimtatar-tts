from io import BytesIO
import requests
from os.path import exists, join
from TTS.utils.synthesizer import Synthesizer
from enum import Enum
from crh_preprocessor.preprocessor import preprocess
from torch import no_grad


class Voices(Enum):
    """List of available voices for the model."""

    Arslan = "arslan"
    Nuri = "nuri"
    Kemal = "kemal"
    Abibulla = "abibulla"


class TTS:
    """ """

    def __init__(self, use_cuda=False) -> None:
        """
        Class to setup a text-to-speech engine, from download to model creation.  \n
        Downloads or uses files from `cache_folder` directory.  \n
        By default stores in current directory."""
        self.__setup_cache(use_cuda=use_cuda)

    def tts(self, text: str, voice: str, output_fp=BytesIO()):
        """
        Run a Text-to-Speech engine and output to `output_fp` BytesIO-like object.
        - `text` - your model input text.
        - `voice` - one of predefined voices from `Voices` enum.
        - `output_fp` - file-like object output. Stores in RAM by default.
        """

        if voice not in [option.value for option in Voices]:
            raise ValueError(
                f"Invalid value for voice selected! Please use one of the following values: {', '.join([option.value for option in Voices])}."
            )

        text = preprocess(text)

        with no_grad():
            wavs = self.synthesizer.tts(text, speaker_name=voice)
            self.synthesizer.save_wav(wavs, output_fp)

        output_fp.seek(0)

        return output_fp, text

    def __setup_cache(self, use_cuda=False):
        """Downloads models and stores them into `cache_folder`. By default stores in current directory."""
        print("downloading uk/crh/vits-tts")
        release_number = "v1.0.0"
        model_link = f"https://github.com/robinhad/qirimtatar-tts/releases/download/{release_number}/model.pth"
        config_link = f"https://github.com/robinhad/qirimtatar-tts/releases/download/{release_number}/config.json"
        speakers_link = f"https://github.com/robinhad/qirimtatar-tts/releases/download/{release_number}/speakers.pth"

        cache_folder = "."

        model_path = join(cache_folder, "model.pth")
        config_path = join(cache_folder, "config.json")
        speakers_path = join(cache_folder, "speakers.pth")

        self.__download(model_link, model_path)
        self.__download(config_link, config_path)
        self.__download(speakers_link, speakers_path)

        self.synthesizer = Synthesizer(
            model_path, config_path, speakers_path, None, None, use_cuda=use_cuda
        )

        if self.synthesizer is None:
            raise NameError("Model not found")

    def __download(self, url, file_name):
        """Downloads file from `url` into local `file_name` file."""
        if not exists(file_name):
            print(f"Downloading {file_name}")
            r = requests.get(url, allow_redirects=True)
            with open(file_name, "wb") as file:
                file.write(r.content)
        else:
            print(f"Found {file_name}. Skipping download...")
