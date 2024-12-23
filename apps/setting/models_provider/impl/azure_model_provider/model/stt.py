import asyncio
import io
from typing import Dict

from openai import OpenAI, AzureOpenAI

from common.config.tokenizer_manage_config import TokenizerManage
from setting.models_provider.base_model_provider import MaxKBBaseModel
from setting.models_provider.impl.base_stt import BaseSpeechToText


def custom_get_token_ids(text: str):
    tokenizer = TokenizerManage.get_tokenizer()
    return tokenizer.encode(text)


class AzureOpenAISpeechToText(MaxKBBaseModel, BaseSpeechToText):
    api_base: str
    api_key: str
    api_version: str
    model: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs.get('api_key')
        self.api_base = kwargs.get('api_base')
        self.api_version = kwargs.get('api_version')

    @staticmethod
    def new_instance(model_type, model_name, model_credential: Dict[str, object], **model_kwargs):
        optional_params = {}
        if 'max_tokens' in model_kwargs and model_kwargs['max_tokens'] is not None:
            optional_params['max_tokens'] = model_kwargs['max_tokens']
        if 'temperature' in model_kwargs and model_kwargs['temperature'] is not None:
            optional_params['temperature'] = model_kwargs['temperature']
        return AzureOpenAISpeechToText(
            model=model_name,
            api_base=model_credential.get('api_base'),
            api_key=model_credential.get('api_key'),
            api_version=model_credential.get('api_version'),
            **optional_params,
        )

    def check_auth(self):
        client = AzureOpenAI(
            azure_endpoint=self.api_base,
            api_key=self.api_key,
            api_version=self.api_version
        )
        response_list = client.models.with_raw_response.list()
        # print(response_list)

    def speech_to_text(self, audio_file):
        client = AzureOpenAI(
            azure_endpoint=self.api_base,
            api_key=self.api_key,
            api_version=self.api_version
        )
        audio_data = audio_file.read()
        buffer = io.BytesIO(audio_data)
        buffer.name = "file.mp3"  # this is the important line
        res = client.audio.transcriptions.create(model=self.model, language="zh", file=buffer)
        return res.text
