import time
import random
import threading
import tkinter as tk
from tkinterweb import HtmlFrame
from tkinter import messagebox

html_fin = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; background-color: #494949; color: #ffffff; text-align: center; }
    </style>
</head>
<body>
    <h1>Fin du programme</h1>
    <p>Vous avez mis fin à l'exécution du programme, vous pouvez le relancer en appuyant sur le bouton start.</p>
    <p>Pour retourner sur la page des explications du logiciel, cliquez sur <b><i>Tutoriel</i></b> dans le menu déroulant.</p>
</body>
</html>
"""

html_tuto = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; background-color: #494949; color: #ffffff; overflow: auto; }
        h1 { text-align: center; }
        .desc { text-align: center; }
    </style>
</head>
<body>
    <h1>Bienvenue sur WeBot !</h1>
    <p class="desc">Ce logiciel a pour but d'automatiser l'ouverture de sites internet de votre choix afin d'améliorer leur référencement sur les différents navigateurs par le nombre de visites. <b>Attention</b>, certains sites ne peuvent pas être ouverts en raison de contenus trop lourds, vous verez donc une page d'erreur, mais cela n'arrétera pas le programme.</p>
    <p>Cette page est accessible depuis le menu déroulant situé en haut, catégorie <i>Tutoriel</i></p>
    <h2>1 - Rentrer une URL :</h2>
    <li><ul>Rentrer une URL dans la case dédiée.</ul></li>
    <li><ul>Cliquer sur le bouton <i>Ajouter</i> (Vous pouvez rentrer plusieurs URL).</ul></li>
    <li><ul>Pour supprimer, sélectionner l'URL voulue et appuyer sur <i>Supprimer URL</i>.</ul></li>
    <h2>2 - Définir le delta et le timer:</h2>
    <p>Le delta correspond au temps qui s'écoulera avant de changer de fenêtre. Il est choisi aléatoirement entre les deux chiffres rentrés dans les cases <i>Delta minimum</i> et <i>Delta maximum</i>. Un petit écart est déconseillé car les navigateurs pourraient détecter plus facilement l'utilisation d'un bot.
    <BR>Le timer est le temps que durera le programme avant de s'arréter automatiquement (il n'est pas obligatoire).</p>
    <li><ul>Rentrer les valeurs (en secondes) de départ et de fin du delta dans les cases dédiées.</ul></li>
    <li><ul>Activer ou non le timer.</ul></li>
    <li><ul>Rentrer (en minutes) le temps d'exécution si le timer est activé.</ul></li>
    <h2>3 - Exécution du programme :</h2>
    <li><ul>Lancer le programme avec le bouton <i>Start</i>.</ul></li>
    <li><ul>Arrêter le programme avec le bouton <i>Stop</i>.</ul></li>
    <li><ul>Une page indiquera l'arrêt du programme.</ul></li>
</body>
</html>
"""

html_credits = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; background-color: #494949; color: #ffffff; overflow: auto; }
        h1 { text-align: center; }
        p { font-size: 20px; }
        .cre { text-align: center; font-size: 20px; }
        .v { text-align: right; }
        .suivre { display: inline; }
    </style>
</head>
<body>
    <div style="text-align: center;">
        <p class="suivre" style="font-size: 50px;">WeBot </p>
        <p class="suivre" style="font-size: 30px;">Version 1</p>
    </div>
    <hr>
    <div style="text-align: center; padding: 15px;">
        <h2 class="suivre">Développé par :</h2>
        <p class="suivre">Marceau</p>
    </div>
    <div style="text-align: center; padding: 15px;">
        <h2 class="suivre">Mon Github :</h2>
        <p class="suivre">MarceauMRS</p>
    </div>
    <div style="text-align: center; padding: 15px; font-size: 20px;">
        <h2 class="suivre cre">Licence :</h2>
        <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" style="color: DeepSkyBlue2;">GNU-GPL v3</a>
        <p class="suivre cre" style="font-size:15px;">(https://www.gnu.org/licenses/gpl-3.0.en.html)</p>
    </div>
    <div>
        <p>Copyright 2025 - Marceau</p>
    </div>
</body>
</html>
"""

root = tk.Tk()
root.title("WeBot")
window_width = 1420
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.config(background="#202020")
frame = tk.Frame(root, background='#202020')
frame.grid(row=0, column=0, sticky='nsew')
frame_url = tk.Frame(frame, background='#202020')
frame_url.grid(row=0, column=0, pady=10)
frame_time = tk.Frame(frame, background='#202020')
frame_time.grid(row=1, column=0, sticky='w', padx=50)
frame_button = tk.Frame(frame, background='#202020')
frame_button.grid(row=2, column=0, sticky='ne')
frame_web = tk.Frame(root, background='#202020', width=800, height=580)
frame_web.grid_propagate(False)
frame_web.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
frame_site = HtmlFrame(frame_web)
frame_site.grid(row=0, column=0)
frame_site.load_html(html_tuto)
menubar = tk.Menu(root)
menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=menu)
menu.add_command(label="Tutoriel...", command=lambda: html(h=html_tuto))
menu.add_command(label="A propos...", command=lambda: html(h=html_credits))
menu.add_separator()
menu.add_command(label="Quitter", command=root.quit)
root.config(menu=menubar)
is_start = False
start_time = 0

def html(h):
    '''
    Ouvre une page html dans la frame web.
    '''
    if not is_start:
        frame_site.load_html(h)
    else:
        messagebox.showinfo(title='Attention !', message="Le programme est en cours d'exécution, cette action n'est pas disponible.")
def ajouter_element():
    '''
    Ajoute une URL à la liste des URL déjà existantes.
    '''
    global urls
    text = entry_url.get()
    if text != "":
        list_url.insert(tk.END, text)
        entry_url.delete(0, tk.END)
        urls = list(list_url.get(first=0, last=list_url.size()))
def suppr():
    '''
    Supprime l'URL sélectionner dans le liste des URL.
    '''
    try:
        list_url.delete(list_url.curselection())
    except:
        if list_url.size() == 0:
            messagebox.showinfo(title='Attention !', message="Il n'y a aucune URL de rentrée.")
        else:
            messagebox.showinfo(title='Attention !', message="Veuillez sélectionner une URL à supprimer.")
def start_on_button():
    '''
    Lance le programme principal lorsque le boutton Start est pressé et vérifie les erreurs potentielles.
    '''
    global is_start, start_time, thr
    if list_url.size() != 0:
        if int(entry_delta_min.get()) <= int(entry_delta_max.get()):
            try:
                if is_start == False:
                    is_start = True
                    start_time = time.time()
                thr = threading.Thread(target=start_site)
                thr.start()
            except:
                messagebox.showinfo(title='Attention !', message="Une erreur s'est produite, veuillez réessayer.")
        else:
            messagebox.showinfo(title='Attention !', message="Le delta minimum doit être plus petit que le delta maximum.")
    else:
        messagebox.showinfo(title='Attention !', message="Veuillez indiquer une URL au minimum.")
def start_site():
    '''
    Charge un site (en fonction des URL données par l'utilisateur) sur la frame web.
    '''
    global is_start, urls
    while is_start:
        if coche_value.get() == True:
            for url in urls:
                a = time.time()
                if a - start_time >= float(entry_timer.get())*60:
                    stop_on_button()
                else:
                    for url in urls:
                        delta = random.randint(int(entry_delta_min.get()), int(entry_delta_max.get()))
                        frame_site.load_website(url)
                        time.sleep(delta)
        else:
            for url in urls:
                delta = random.randint(int(entry_delta_min.get()), int(entry_delta_max.get()))
                frame_site.load_website(url)
                time.sleep(delta)
def stop_on_button():
    '''
    Arrête le programme principal lorsque le boutton Stop est pressé.
    '''
    global is_start, thr
    if is_start:
        is_start = False
        frame_site.load_html(html_fin)

list_url = tk.Listbox(frame_url, background='#494949', foreground='#ffffff', width=40)
list_url.grid(row=0, column=0, padx=10, rowspan=4, sticky='ns')
label_url = tk.Label(frame_url, text="URL's : ", background='#202020', foreground='#ffffff')
label_url.grid(row=0, column=1, sticky='ws')
entry_url = tk.Entry(frame_url, width=40)
entry_url.grid(row=1, column=1, sticky='nwe')
button_url = tk.Button(frame_url, text='Ajouter', background='#494949', foreground='#ffffff', command=ajouter_element)
button_url.grid(row=1, column=2, padx=10, sticky='n')
suppr_button = tk.Button(frame_url, text='Suprimer URL', background='#494949', foreground='#ffffff', command=suppr)
suppr_button.grid(row=4, column=0, sticky='nw', padx=10, pady=10)
label_delta = tk.Label(frame_time, text='Changement de site au bout de :', background='#202020', foreground='#ffffff')
label_delta.grid(row=0, column=0, sticky='e')
label_delta_min = tk.Label(frame_time, text='Delta minimum (sec): ', background='#202020', foreground='#ffffff')
label_delta_min.grid(row=0, column=1)
label_delta_max = tk.Label(frame_time, text='Delta maximum (sec): ', background='#202020', foreground='#ffffff')
label_delta_max.grid(row=1, column=1)
min_time_base = tk.StringVar(value='5')
entry_delta_min = tk.Entry(frame_time, textvariable=min_time_base, width=4)
entry_delta_min.grid(row=0, column=2, pady=10, sticky='we')
max_time_base = tk.StringVar(value='60')
entry_delta_max = tk.Entry(frame_time, textvariable=max_time_base, width=4)
entry_delta_max.grid(row=1, column=2, sticky='we')
label_coche = tk.Label(frame_time, text='Activer le AutoStop : ', background='#202020', foreground='#ffffff')
label_coche.grid(row=2, column=0, sticky='e', padx=25)
coche_value = tk.BooleanVar()
coche_timer = tk.Checkbutton(frame_time, variable=coche_value, background='#202020')
coche_timer.grid(row=2, column=0, sticky='e')
label_timer = tk.Label(frame_time, text="AutoStop au bout de (min): ", background='#202020', foreground='#ffffff')
label_timer.grid(row=2, column=1, sticky='e')
timer_base = tk.StringVar(value='10')
entry_timer = tk.Entry(frame_time, textvariable=timer_base, width=5)
entry_timer.grid(row=2, column=2, pady=30, sticky='we')
start_button = tk.Button(frame_button, text='Start', background="#494949", foreground='#ffffff', command=start_on_button, width=10)
start_button.grid(row=3, column=3, sticky='nsew', padx=5)
stop_button = tk.Button(frame_button, text='Stop', background="#494949", foreground='#ffffff', command=stop_on_button, width=10)
stop_button.grid(row=3, column=4, sticky='nsew')

root.mainloop()