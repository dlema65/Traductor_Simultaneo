"""
Mantener una envoltura para los servicios IBM Watson a utilizar
"""
import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1, LanguageTranslatorV3, TextToSpeechV1
import wave
from configparser import ConfigParser

"""
Las claves de acceso (apikey) y las URLs de los recursos de IBM Watson
a utilizar se configurarán en un archivo de configuración (application.ini)
"""

config = ConfigParser()
config.read('../application.ini')

# diccionario que mapea nombres de idiomas en el modelo de interpretación
# a utilizar
models = {
    "Español": "es-CO_BroadbandModel",
    "Inglés": "en-US_BroadbandModel",
    "Italiano": "it-IT_BroadbandModel",
    "Francés": "fr-FR_BroadbandModel",
    "Alemán": "de-DE_BroadbandModel",
}

# diccionario que mapea nombres de idiomas en el modelo de voz usado para su
# sintetización
voices = {
    "Español": "es-LA_SofiaV3Voice",
    'Inglés': 'en-US_EmilyV3Voice',
    'Italiano': 'it-IT_FrancescaV3Voice',
    'Francés': 'fr-FR_ReneeV3Voice',
    'Alemán': 'de-DE_BirgitV3Voice',
}


class SttWrapper:
    """
    Envoltura para la conversión de audio a texto
    """

    def __init__(self):
        """
        Instancia objeto de tipo SttWrapper
        """
        self.authenticator = IAMAuthenticator(os.environ.get('SPEECH_TO_TEXT_APIKEY',
                                                             config.get('IBM_WATSON_SERVICES', 'SPEECH_TO_TEXT_APIKEY')
                                                             ))
        self.speech_to_text = SpeechToTextV1(authenticator=self.authenticator)
        self.speech_to_text.set_service_url(os.environ.get('SPEECH_TO_TEXT_URL',
                                                           config.get('IBM_WATSON_SERVICES', 'SPEECH_TO_TEXT_URL')
                                                           ))

    def to_text(self, audio, language='Español'):
        """
        Implementación sincrónica de la conversión de audio a texto
        :param audio: audio de entrada
        :param language: idioma a ser procesado
        :return: texto convertido
        """

        # mapea el modelo a partir del idioma recibido
        model = models[language]

        # convierte de audio a texto
        response = self.speech_to_text.recognize(
            audio=audio,
            content_type='audio/l16;rate=44100;channels=1;endianness=little-endian',
            model=model,
            max_alternatives=3)

        # retorna el texto
        return response


class TtsWrapper:
    """
    Clase que envuelve el servicio de Text to Speech o lectura de texto
    """

    def __init__(self):
        authenticator = IAMAuthenticator(os.environ.get('TEXT_TO_SPEECH_APIKEY',
                                                        config.get('IBM_WATSON_SERVICES', 'TEXT_TO_SPEECH_APIKEY')))
        self.text_to_speech = TextToSpeechV1(authenticator=authenticator)
        self.text_to_speech.set_service_url(os.environ.get('TEXT_TO_SPEECH_URL',
                                                           config.get('IBM_WATSON_SERVICES', 'TEXT_TO_SPEECH_URL')))

    def tts(self, text, language='Inglés'):
        """
        Convierte de texto a voz
        :param text: texto a ser convertido
        :param language: idioma
        """
        return self.text_to_speech.synthesize(text,
                                              accept='audio/l16;rate=44100;channels=1',
                                              voice=voices[language]
                                              )


class TranslatorWrapper:
    """
    clase que envuelve el servicio de traducción
    """

    def __init__(self):
        authenticator = IAMAuthenticator(os.environ.get('LANGUAGE_TRANSLATOR_APIKEY',
                                                        config.get('IBM_WATSON_SERVICES',
                                                                   'LANGUAGE_TRANSLATOR_APIKEY')))
        self.language_translator = LanguageTranslatorV3(authenticator=authenticator,
                                                        version='2018-05-01')
        self.language_translator.set_service_url(os.environ.get('LANGUAGE_TRANSLATOR_URL',
                                                                config.get('IBM_WATSON_SERVICES',
                                                                           'LANGUAGE_TRANSLATOR_URL')))

    def translate(self, text, source_language, target_language):
        """
        Traduce el texto suministrado del idioma origen al idioma destino
        :param text: texto a ser traducido
        :param source_language: idioma origen
        :param target_language: idioma destino
        :return: traducción
        """
        # a partir del idioma, obtiene el código ISO 639-1.
        source = models[source_language][0:2]
        target = models[target_language][0:2]
        # devuelve texto traducido
        return self.language_translator.translate([text, ], source=source, target=target)


"""
El programa principal de este módulo se usa solo para ejecución de pruebas de 
funcionamiento
"""
if __name__ == '__main__':
    # abre archivo de audio
    audio_input = open('../audio_prueba_video_3.wav', 'rb')

    # instancia Speech to Text wrapper
    stt = SttWrapper()

    # convierte de audio a texto
    resultado = stt.to_text(audio_input)

    # imprime resultado
    print(resultado.result)

    a_traducir = 'Il Nome della Rosa: il libro più intelligente - ma anche il più divertente - di ' \
                 'questi ultimi anni'

    translator = TranslatorWrapper()
    print('==== original ====')
    print(a_traducir)
    print('==== Traducción al español ====')
    print(translator.translate(a_traducir, 'Italiano', 'Español'))
    print('==== Traducción al inglés ====')
    print(translator.translate(a_traducir, 'Italiano', 'Inglés'))

    output_file = wave.open("../prueba lectura video 3.wav", "wb")
    output_file.setnchannels(1)
    output_file.setframerate(44100)
    output_file.setsampwidth(2)

    tts = TtsWrapper()
    spoke_phrase = tts.tts(a_traducir, language='Italiano')

    output_file.writeframes(spoke_phrase.result.content)
    output_file.close()

