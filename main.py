import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import pygame

nazwa_pliku = ''
numer = None
music_play = True
count = 0
pygame.mixer.init()


def powrot():
    global music_play
    aktualny = int(listbox.curselection()[0])
    listbox.selection_clear(0, END)  # Wyczyść zaznaczenie wszystkich linii
    if listbox.size() > aktualny - 1 >= 0:
        listbox.selection_set(aktualny - 1)  # Zaznacz następną linię
    else:
        listbox.selection_set(0)  # Jeśli przekroczyliśmy koniec listy, zaznacz pierwszą linijkę

    music_play = True
    play()


def nastepna():
    global music_play
    if listbox.curselection():
        aktualny = int(listbox.curselection()[0])
        listbox.selection_clear(0, END)
        if aktualny + 1 < listbox.size():
            listbox.selection_set(aktualny + 1)
        else:
            listbox.selection_set(0)

        music_play = True
        play()


def openfolder():
    global folder
    folder = filedialog.askdirectory()
    if folder:
        listbox.delete(0, END)
        list_files = os.listdir(folder)
        for file in list_files:
            if file[-3:] == 'mp3':
                listbox.insert(END, file)
            else:
                pass


def play():
    global music_play
    global nazwa_pliku
    global numer
    if not music_play:
        music_play = True
        play_button.config(image=start)
        mixer.music.pause()
    elif music_play:
        try:
            music_play = False
            play_button.config(image=stop)

            if listbox.curselection()[0] == numer:
                mixer.music.unpause()
                update_progress()
            else:
                numer = listbox.curselection()[0]
                nazwa_pliku = listbox.get(listbox.curselection()[0])
                piosenka = pygame.mixer.Sound(f'{folder}/{nazwa_pliku}')
                mixer.music.load(f'{folder}/{nazwa_pliku}')
                mixer.music.play()
                sound_get_ms = piosenka.get_length()
                current_time_min = round(sound_get_ms) // 60  # Oblicz minutę
                current_time_sec = (round(sound_get_ms) % 60)  # Oblicz sekundy

                # Sformatuj czas
                formatted_time = '{:02d}:{:02d}'.format(current_time_min, current_time_sec)
                dlugosc = round(sound_get_ms, 1)
                dlugosc1.set(str(dlugosc))
                dlugosc2.set(formatted_time)
                czas_muzyki.config(to=dlugosc)
                nazwa_utworu.set(f'Utwór: {nazwa_pliku}')
                update_progress()
        except:
            play_button.config(image=start)
            pass


def play_1():
    global music_play, count
    if music_play:
        music_play = False
    elif not music_play:
        music_play = True
    play()


def update_progress():
    global music_play
    volume = glosnosc.get() / 10
    mixer.music.set_volume(volume)
    if not music_play:
        current_time = pygame.mixer.music.get_pos()
        if current_time >= 0:
            current_time_min = current_time // 60000  # Oblicz minutę
            current_time_sec = (current_time % 60000) // 1000  # Oblicz sekundy

            # Utwórz ładnie sformatowany czas
            formatted_time = '{:02d}:{:02d}'.format(current_time_min, current_time_sec)
            czas_now.set(formatted_time)
            czas.set(round(current_time / 1000, 1))
            if str(round(current_time / 1000, 1) + 0.1) == dlugosc1.get():
                nastepna()
        else:
            nastepna()

        window.after(100, update_progress)


window = Tk()
window.geometry("600x500")
window.config(bg='black')
frame = Frame(window)
frame.config(bg='#2a2a2a')
frame.pack()

Label(frame, text='Pytify', font=('Arial', 20), fg='white', bg='#2a2a2a').pack()
listbox = Listbox(frame, width=100, height=15, bg='#434143', fg='white', highlightbackground="black", bd=0)
listbox.pack()
open_button = Button(frame, text='Open', bg='#1fdf64', width=5, height=1, font=('Arial', 12, 'bold'),
                     command=openfolder)
open_button.place(x=525, y=3)
nazwa_utworu = StringVar()
Label(window, textvariable=nazwa_utworu, fg='white', bg='Black').pack()
poprzedni = PhotoImage(file='next.png')
nastepny = PhotoImage(file='previous.png')
start = PhotoImage(file='play.png')
stop = PhotoImage(file='pause.png')
button_frame = Frame(window)
button_frame.pack()

Button(button_frame, command=powrot, image=poprzedni, bg='black', bd=0, highlightbackground="black",
       activebackground="#1d1d1d").grid(
    row=0, column=0)
play_button = Button(button_frame, image=start, bg='black', bd=0, highlightbackground="black",
                     activebackground="#1d1d1d", command=play)
play_button.grid(row=0, column=1)
Button(button_frame, command=nastepna, image=nastepny, bg='black', bd=0, highlightbackground="black",
       activebackground="#1d1d1d").grid(
    row=0, column=2)

czas_now = StringVar(window)
Label(window, textvariable=czas_now, bg='black', fg='white', font=('arial', 12)).place(x=5, y=375)

czas = DoubleVar(window, value=0)
czas_muzyki = Scale(window, from_=0.0, to=0.01, resolution=0.01, orient=HORIZONTAL, variable=czas, length=500,
                    bg='black', troughcolor='gray', sliderlength=20, highlightthickness=0, fg='white', showvalue=False,
                    state='disabled')
czas_muzyki.pack(pady=10)
dlugosc1 = StringVar(window)
dlugosc2 = StringVar(window)
czas_max = Label(window, textvariable=dlugosc2, bg='black', fg='white', font=('arial', 12))
czas_max.place(x=550, y=375)

glosnosc_frame = Frame(window, bg='black')
glosnosc_frame.pack(anchor=W)
sound = PhotoImage(file='sound.png')
Label(glosnosc_frame, image=sound, bg='black').grid(column=0, row=0)
deafult = DoubleVar(window, value=1)
glosnosc = Scale(glosnosc_frame, showvalue=False, from_=0.0, to=10.0, resolution=0.01, orient=HORIZONTAL,
                 variable=deafult, length=150, bg='black', troughcolor='green', sliderlength=10, highlightthickness=0,
                 fg='white')
glosnosc.grid(column=1, row=0)
listbox.bind("<<ListboxSelect>>", lambda event: play_1())
window.bind("<space>", lambda event: play())
window.mainloop()
