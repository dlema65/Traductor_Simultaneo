import tkinter as tk
from tkinter import ttk, PhotoImage
from colors import *  # define colores con nombres dicientes

# para mejorar la presentación en Windows cuando se tienen monitores de
# alta resolución (4k o más)
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# crea ventana principal
root = tk.Tk()
root.geometry("400x600")
root.title('Traductor Turístico')
favicon = PhotoImage(file='../static/images/favicon.gif')
root.iconphoto(False, favicon)

# arma visualización
title = ttk.Label(root, text='Traductor Turístico', padding=20)
title.config(font=('Segoe UI', 20))
title.pack()

# marco que contiene los combobox de configuración de idiomas
setup_frame = ttk.Frame(root)

# combobox de configuración de idioma origen
tk.Label(setup_frame, text='Idioma Origen').grid(row=0, column=0)
origin_language_combobox = ttk.Combobox(setup_frame)
origin_language_combobox["values"] = ("Español", "Inglés", "Italiano", "Francés", "Alemán")
origin_language_combobox["state"] = "readonly"
origin_language_combobox.current(0)
origin_language_combobox.grid(row=1, column=0, padx=5)

# combobox de configuración de idioma destino
tk.Label(setup_frame, text='Idioma Destino').grid(row=0, column=1)
final_language_combobox = ttk.Combobox(setup_frame)
final_language_combobox["values"] = ("Español", "Inglés", "Italiano", "Francés", "Alemán")
final_language_combobox["state"] = "readonly"
final_language_combobox.current(1)
final_language_combobox.grid(row=1, column=1, padx=5)
setup_frame.pack()

# marco con controles de escucha (botón y caja de texto)
listen_frame = ttk.Frame(root)
mic_button = tk.Button(listen_frame,
                       text='Mic',
                       bg=SPRING_GREEN,
                       activebackground=rgba_to_rgb(SPRING_GREEN + 'CC'),
                       )
mic_button.pack(side='left', pady=5, padx=5)
ttk.Label(listen_frame, text='Lo escuchado: ', ).pack(side='top', expand=True)
listened_text = tk.Text(listen_frame, height=6, wrap='word')
listened_text.pack(side='top', expand=True, fill='both')
listen_frame.pack(pady=5, padx=5)

translation_frame = ttk.Frame(root)
read_button = tk.Button(translation_frame,
                        text='Decir',
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