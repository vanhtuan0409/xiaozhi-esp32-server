import io

from config.logger import setup_logging
from core.providers.tts.base import TTSProviderBase

TAG = __name__
logger = setup_logging()


class TTSProvider(TTSProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)

        self.voice_name = config.get("voice")
        self.audio_file_type = "wav"

        self._tts = None
        self._voice = None
        self._init_vieneu()

    def _init_vieneu(self):
        from vieneu import Vieneu

        self._tts = Vieneu(mode="turbo")
        self.sample_rate = self._tts.sample_rate

        if self.voice_name:
            try:
                self._voice = self._tts.get_preset_voice(self.voice_name)
            except Exception:
                logger.bind(tag=TAG).warning(
                    f"Voice '{self.voice_name}' not found, using default"
                )

        logger.bind(tag=TAG).info(
            f"VieNeu TTS initialized: mode=turbo, sample_rate={self.sample_rate}"
        )

    async def text_to_speak(self, text, output_file):
        try:
            import soundfile as sf

            audio = (
                self._tts.infer(text, voice=self._voice)
                if self._voice
                else self._tts.infer(text)
            )

            if audio is None or len(audio) == 0:
                raise Exception(f"VieNeu returned empty audio for text='{text}'")

            if output_file:
                self._tts.save(audio, output_file)
            else:
                buf = io.BytesIO()
                sf.write(buf, audio, self.sample_rate, format="WAV")
                return buf.getvalue()

        except Exception as e:
            error_msg = f"VieNeu TTS failed: {e}"
            logger.bind(tag=TAG).error(error_msg)
            raise Exception(error_msg)

    async def close(self):
        await super().close()
        if self._tts:
            self._tts.close()
            self._tts = None
