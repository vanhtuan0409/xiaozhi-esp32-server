import io
import wave

from config.logger import setup_logging
from core.providers.tts.base import TTSProviderBase

TAG = __name__
logger = setup_logging()


class TTSProvider(TTSProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)

        self.model_path = config.get("model_path")
        self.config_path = config.get("config_path")
        self.audio_file_type = "wav"

        self._voice = None
        self._normalizer = None
        self._init_piper()
        self._init_normalizer(config)

    def _init_piper(self):
        from piper import PiperVoice

        self._voice = PiperVoice.load(
            self.model_path,
            config_path=self.config_path,
        )

        logger.bind(tag=TAG).info(
            f"Piper TTS initialized: model={self.model_path}, "
            f"sample_rate={self._voice.config.sample_rate}"
        )

    def _init_normalizer(self, config):
        if not config.get("use_normalizer", False):
            return
        try:
            from vietnormalizer import VietnameseNormalizer

            self._normalizer = VietnameseNormalizer()
            logger.bind(tag=TAG).info("Vietnamese text normalizer enabled")
        except ImportError:
            logger.bind(tag=TAG).warning(
                "vietnormalizer package not installed, normalizer disabled"
            )

    def _normalize_text(self, text):
        if self._normalizer is None:
            return text
        return self._normalizer.normalize(text)

    def _synthesize_to_wav(self, text, target):
        with wave.open(target, "wb") as wav_file:
            self._voice.synthesize_wav(text, wav_file)

    async def text_to_speak(self, text, output_file):
        try:
            text = self._normalize_text(text)
            if output_file:
                self._synthesize_to_wav(text, output_file)
            else:
                buf = io.BytesIO()
                self._synthesize_to_wav(text, buf)
                return buf.getvalue()

        except Exception as e:
            error_msg = f"Piper TTS failed: {e}"
            logger.bind(tag=TAG).error(error_msg)
            raise Exception(error_msg)

    async def close(self):
        await super().close()
        self._voice = None
