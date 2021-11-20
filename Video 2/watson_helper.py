"""
Mantener una envoltura para los servicios IBM Watson a utilizar
"""
import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1
import wave
from configparser import ConfigParser

"""
Las claves de acceso (apikey) y las URLs de los recursos de IBM Watson
a utilizar se configurarán en un archivo de configuración (application.ini)
"""

config = ConfigParser()
config.read('../application.ini')

models = {
    "Español": "es-CO_BroadbandModel",
    "Inglés": "en-US_BroadbandModel",
    "Italiano": "it-IT_BroadbandModel",
    "Francés": "fr-FR_BroadbandModel",
    "Alemán": "de-DE_BroadbandModel",
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


"""
El programa principal de este módulo se usa solo para ejecución de pruebas de 
funcionamiento
"""
if __name__ == '__main__':
    # abre archivo de audio
    audio_input = open('../audio_prueba_video_2.wav', 'rb')

    # instancia Speech to Text wrapper
    stt = SttWrapper()

    # convierte de audio a texto
    resultado = stt.to_text(audio_input)

    # imprime resultado
    print(resultado.result)
