import boto3
from .aws_config import AWS_REGION


class TranslationService:
    def __init__(self):
        self.client = boto3.client('translate', region_name=AWS_REGION)

    def translate_text(self, text, source_language = 'auto', target_language = 'en'):
        response = self.client.translate_text(
            Text = text,
            SourceLanguageCode = source_language,
            TargetLanguageCode = target_language
        )

        translation = {
            'translatedText': response['TranslatedText'],
            'sourceLanguage': response['SourceLanguageCode'],
            'targetLanguage': response['TargetLanguageCode']
        }

        return translation
