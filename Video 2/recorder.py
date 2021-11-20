import pyaudio
import threading
import time
import wave

# define constantes para...
CHUNK = 1024   # tamaño de los fragmentos de grabación
FORMAT = pyaudio.paInt16   # formato del audio
CHANNELS = 1   # número de canales (monofónico en este ejercicio)
RATE = 44100   # número de muestras por segundo


class Recorder:
    """
    Clase que implementa la funcionalidad de una grabadora
    """

    def __init__(self):
        """
        Instancia un objeto de tipo recorder
        """
        self._p = pyaudio.PyAudio()
        self.is_recording = False   # estado
        self._t = None             # hilo que se usa para grabar

    def __record(self):
        """
        Operación que controla la grabación
        Planeada para correr en un hilo independiente
        """
        # abre un entrada stream de audio
        self._stream = self._p.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    frames_per_buffer=CHUNK)

        # define variable para almacenar los fragmentos de la grabación
        self._frames = []

        # ciclo que acumula los fragmentos de grabación
        while self.is_recording:
            data = self._stream.read(CHUNK)
            self._frames.append(data)

    def start(self):
        """
        Arranca la grabacion
        """
        # verificar que no esté arrancada
        if self.is_recording:
            print("la grabadora ya está encendida")
            return

        # marca el inicio de la grabación
        self.is_recording = True

        # define hilo y asigna la operación de grabar a dicho hilo
        self._t = threading.Thread(target=self.__record)

        # arranca hilo
        self._t.start()

    def stop(self):
        """
        Detiene la grabación
        :return: secuencia de bytes con el audio de la grabación
        """
        # verificar que esté encendida
        if self.is_recording:

            # indica que se apague la grabación
            self.is_recording = False

            # espera la terminación del hilo de la grabación
            self._t.join()

            # pone None a la variable que tiene el hilo para que el garbage collector se pueda
            # deshacer de él
            self._t = None

            # detiene y cierra el stream de entrada de audio
            self._stream.stop_stream()
            self._stream.close()

            # devuelve stream de bytes con el audio
            return b''.join(self._frames)

    def save(self, filename):
        """
        Guarda en un archivo la última grabación efectuada
        :param filename: nombre del archivo de salida
        """
        # abre archivo de salida de tipo wave (onda). Nótese que es de escritura de bytes
        output_file = wave.open(filename, 'wb')
        output_file.setnchannels(CHANNELS)
        output_file.setframerate(RATE)
        output_file.setsampwidth(self._p.get_sample_size(FORMAT))
        output_file.writeframes(b''.join(self._frames))
        output_file.close()


# El programa principal se usa solo para prob ar el funcionamiento de la grabadora
if __name__ == '__main__':
    recorder = Recorder()
    recorder.start()
    time.sleep(5)
    phrase = recorder.stop()
    recorder.save("../audio_prueba_video_2.wav")

