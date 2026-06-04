from core.providers.llm.base import LLMProviderBase
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


class TelemetryLLMProvider(LLMProviderBase):
    def __init__(self, provider):
        self._provider = provider

    def response(self, session_id, dialogue, **kwargs):
        logger.bind(tag=TAG).debug(f"LLM request session_id={session_id}, dialogue={dialogue}")
        return self._provider.response(session_id, dialogue, **kwargs)

    def response_no_stream(self, system_prompt, user_prompt, **kwargs):
        return self._provider.response_no_stream(system_prompt, user_prompt, **kwargs)

    def response_with_functions(self, session_id, dialogue, functions=None):
        logger.bind(tag=TAG).debug(f"LLM function call request session_id={session_id}, dialogue={dialogue}, functions={functions}")
        return self._provider.response_with_functions(session_id, dialogue, functions)
