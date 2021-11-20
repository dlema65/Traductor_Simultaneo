import tkinter as tk
from tkinter import ttk, PhotoImage
from colors import *  # define colores con nombres dicientes
from recorder import Recorder
from watson_helper import SttWrapper

# para mejorar la presentación en Windows cuando se tienen monitores de
# alta resolución (4k o más)
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def listen():
    """
    Función que implementa las acciones del botón micrófono.
    """
    # verifica el estado de la grabadora
    if recorder.is_recording:  # está encendida?

        # apaga la grabación y recupera el audio
        recording = recorder.stop()

        # borra el contenido de la caja de texto escuchado
        listened_text.delete('1.0', 'end')

        # obtiene la frase en texto
        listened_phrase = stt.to_text(recording, language=origin_language.get()) \
            .result['results'][0]['alternatives'][0]['transcript']

        # escribe texto en la caja de texto escuchado
        listened_text.insert('1.0', listened_phrase)

        # restaura el color del botón de micrófono a verde
        mic_button.config(bg=SPRING_GREEN, activebackground=rgba_to_rgb(SPRING_GREEN + 'CC'))

    else:    # en caso de estar apagada

        # enciende la grabadora
        recorder.start()

        # pone botón de mic en rojo
        mic_button.config(bg=WARM_RED, activebackground=rgba_to_rgb(WARM_RED + 'CC'))


# crea ventana principal
root = tk.Tk()
root.geometry("400x600")
root.title('Traductor Turístico')
favicon = PhotoImage(file='../static/images/favicon.gif')
root.iconphoto(False, favicon)

# Crea instancias de las clases helper desarrolladas
recorder = Recorder()
stt = SttWrapper()

# arma visualización
title = ttk.Label(root, text='Traductor Turístico', padding=20)
title.config(font=('Segoe UI', 20))
title.pack()

# marco que contiene los combobox de configuración de idiomas
setup_frame = ttk.Frame(root)

# imágenes para los botones
mic_image = PhotoImage(file=r'../static/images/mic_on_icon_64px.png')
speaker_image = PhotoImage(file=r'../static/images/speaker_64px.png')

# modelos que guardan información sobre idiomas
origin_language = tk.StringVar()
target_language = tk.StringVar()

# combobox de configuración de idioma origen
tk.Label(setup_frame, text='Idioma Origen').grid(row=0, column=0)
# nótese que se agrega asociación entre el combo box y la variable que conserva el idioma origen
origin_language_combobox = ttk.Combobox(setup_frame, textvariable=origin_language)
origin_language_combobox["values"] = ("Español", "Inglés", "Italiano", "Francés", "Alemán")
origin_language_combobox["state"] = "readonly"
origin_language_combobox.current(0)
origin_language_combobox.grid(row=1, column=0, padx=5)

# combobox de configuración de idioma destino
tk.Label(setup_frame, text='Idioma Destino').grid(row=0, column=1)
final_language_combobox = ttk.Combobox(setup_frame, textvariable=target_language)
final_language_combobox["values"] = ("Español", "Inglés", "Italiano", "Francés", "Alemán")
final_language_combobox["state"] = "readonly"
final_language_combobox.current(1)
final_language_combobox.grid(row=1, column=1, padx=5)
setup_frame.pack()

# marco con controles de escucha (botón y caja de texto)
listen_frame = ttk.Frame(root)
# nótese que se agrega imagen al botón, así como definición de la función a ejecutar cuando se presiona
mic_button = tk.Button(listen_frame,
                       text='Mic',
                       image=mic_image,
                       bg=SPRING_GREEN,
                       activebackground=rgba_to_rgb(SPRING_GREEN + 'CC'),
                       command=listen
                       )
mic_button.pack(side='left', pady=5, padx=5)
ttk.Label(listen_frame, text='Lo escuchado: ', ).pack(side='top', expand=True)
listened_text = tk.Text(listen_frame, height=6, wrap='word')
listened_text.pack(side='top', expand=True, fill='both')
listen_frame.pack(pady=5, padx=5)

translation_frame = ttk.Frame(root)
read_button = tk.Button(translation_frame,
                        text='Decir',
                        image=speaker_image,
                        bg=SPRING_GREEN,
                        activebackground=rgba_to_rgb(SPRING_GREEN + 'CC'),
                        )
read_button.pack(side='right', pady=5, padx=5)
ttk.Label(translation_frame, text='Traducción: ').pack(side='top')
translated_text = tk.Text(translation_frame, height=6)
translated_text['state'] = 'disabled'
translated_text.pack(side='top')
translation_frame.pack(pady=5, padx=5)

# frame con botones de control
control_frame = ttk.Frame(root)
clear_button = ttk.Button(control_frame, text='Borrar')
clear_button.pack(side='left', padx=5)
quit_button = ttk.Button(control_frame, text='Salir', command=root.destroy)
quit_button.pack(side='right', padx=5)
control_frame.pack(pady=5, padx=5)


root.mainloop()
