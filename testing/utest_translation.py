"""
utest_translation.py  – updated for Exercise #3
Added: PollyServiceTest to verify that synthesize() returns non-empty MP3 bytes.
"""

import os
import sys
import unittest

import translation_service
import polly_service  # NEW


class TranslationServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = translation_service.TranslationService()

    def test_translate_text(self):
        translation = self.service.translate_text('Einbahnstrabe')
        self.assertTrue(translation)
        self.assertEqual('de', translation['sourceLanguage'])
        self.assertEqual('One way street', translation['translatedText'])
        print('OK test for translation')


# NEW ── Unit test for the Polly (text-to-speech) service
class PollyServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = polly_service.PollyService()

    def test_synthesize_returns_bytes(self):
        """synthesize() must return a non-empty bytes object."""
        audio = self.service.synthesize("Hello, this is a test.")
        self.assertIsInstance(audio, bytes)
        self.assertGreater(len(audio), 0)
        print('OK test for Polly synthesis – received', len(audio), 'bytes')

    def test_synthesize_french_text(self):
        """Polly should handle non-English input text (French example)."""
        audio = self.service.synthesize("Bonjour le monde")
        self.assertIsInstance(audio, bytes)
        self.assertGreater(len(audio), 0)
        print('OK test for Polly synthesis with French text')


if __name__ == "__main__":
    unittest.main()
