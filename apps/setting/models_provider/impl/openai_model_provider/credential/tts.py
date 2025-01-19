# coding=utf-8
from typing import Dict

from common import forms
from common.exception.app_exception import AppApiException
from common.forms import BaseForm, TooltipLabel
from setting.models_provider.base_model_provider import BaseModelCredential, ValidCode
from django.utils.translation import gettext_lazy as _

class OpenAITTSModelGeneralParams(BaseForm):
    # alloy, echo, fable, onyx, nova, shimmer
    voice = forms.SingleSelect(
        TooltipLabel('Voice', _('Try out the different sounds (Alloy, Echo, Fable, Onyx, Nova, and Sparkle) to find one that suits your desired tone and audience. The current voiceover is optimized for English.')),
        required=True, default_value='alloy',
        text_field='value',
        value_field='value',
        option_list=[
            {'text': 'alloy', 'value': 'alloy'},
            {'text': 'echo', 'value': 'echo'},
            {'text': 'fable', 'value': 'fable'},
            {'text': 'onyx', 'value': 'onyx'},
            {'text': 'nova', 'value': 'nova'},
            {'text': 'shimmer', 'value': 'shimmer'},
        ])


class OpenAITTSModelCredential(BaseForm, BaseModelCredential):
    api_base = forms.TextInputField('API Url', required=True)
    api_key = forms.PasswordInputField('API Key', required=True)

    def is_valid(self, model_type: str, model_name, model_credential: Dict[str, object], model_params, provider,
                 raise_exception=False):
        model_type_list = provider.get_model_type_list()
        if not any(list(filter(lambda mt: mt.get('value') == model_type, model_type_list))):
            raise AppApiException(ValidCode.valid_error.value, _('{model_type} Model type is not supported').format(model_type=model_type))

        for key in ['api_base', 'api_key']:
            if key not in model_credential:
                if raise_exception:
                    raise AppApiException(ValidCode.valid_error.value, _('{key}  is required').format(key=key))
                else:
                    return False
        try:
            model = provider.get_model(model_type, model_name, model_credential, **model_params)
            model.check_auth()
        except Exception as e:
            if isinstance(e, AppApiException):
                raise e
            if raise_exception:
                raise AppApiException(ValidCode.valid_error.value, _('Verification failed, please check whether the parameters are correct: {error}').format(error=str(e)))
            else:
                return False
        return True

    def encryption_dict(self, model: Dict[str, object]):
        return {**model, 'api_key': super().encryption(model.get('api_key', ''))}

    def get_model_params_setting_form(self, model_name):
        return OpenAITTSModelGeneralParams()
