"""
polly_service.py  (NEW – Exercise #3)
Text-to-Speech service wrapper around Amazon Polly.

Design decision:
    We chose the STANDARD engine with the Joanna (en-US) voice because it is
    available in every AWS region that also supports Translate and Rekognition,
    keeping the deployment footprint simple.  Neural voices sound more natural
    but are region-limited and cost ~4× more per character.

    Audio is returned as raw bytes (MP3) so that the Chalice endpoint can
    base64-encode and embed it directly in the JSON response.  This avoids
    writing a temporary file to disk and keeps the service stateless.
"""

import boto3
import aws_config


class PollyService:
    # Sensible defaults – easily overridden by the caller
    DEFAULT_VOICE  = "Joanna"   # English (US) – female
    DEFAULT_ENGINE = "standard" # 'standard' | 'neural'
    DEFAULT_FORMAT = "mp3"

    def __init__(self):
        self.client = boto3.client("polly", region_name=aws_config.AWS_REGION)

    def synthesize(
        self,
        text: str,
        voice_id: str  = DEFAULT_VOICE,
        engine: str    = DEFAULT_ENGINE,
        output_format: str = DEFAULT_FORMAT
    ) -> bytes:
        """
        Convert *text* to speech and return raw audio bytes.

        Parameters
        ----------
        text          : str  – plain text to synthesise (max 3 000 chars for
                                standard; use start_speech_synthesis_task for
                                longer documents)
        voice_id      : str  – Polly VoiceId (default: Joanna)
        engine        : str  – 'standard' or 'neural'
        output_format : str  – 'mp3', 'ogg_vorbis', or 'pcm'

        Returns
        -------
        bytes – raw audio stream content
        """
        response = self.client.synthesize_speech(
            Text=text,
            VoiceId=voice_id,
            Engine=engine,
            OutputFormat=output_format
        )

        
        audio_bytes = response["AudioStream"].read()
        return audio_bytes
