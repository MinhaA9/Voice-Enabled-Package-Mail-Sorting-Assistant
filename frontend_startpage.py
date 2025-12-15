from customtkinter import *
from backend_datalayer import *
from threading import Thread

db = Database()
def start_loading(progress_bar, start_label, app):
    def run():
        db.read_databases(lambda val, txt: update_progress(val, txt, progress_bar, start_label, app))
        update_progress(1, "Databases Loaded!", progress_bar, start_label, app)
    Thread(target=run, daemon=True).start()

def update_progress(value, text,progress_bar,start_label,app):
    progress_bar.set(value)
    start_label.configure(text=text)
    app.update_idletasks()

def start_body(main_body, app, cnt_mng):
    main_body.pack_propagate(False)
    cnt_mng.show("start")
    container_stpg = cnt_mng.get("start")
    start_label = CTkLabel(
        container_stpg, 
        text="Click Start to Load the Databases",
        text_color="black",
        font=CTkFont("Georgia", size=20, weight="normal", slant="italic")
    )
    start_label.pack(pady=10)

    progress_bar = CTkProgressBar(container_stpg, width=400, height=20)
    progress_bar.pack(pady=30)
    progress_bar.set(0)

    start_bttn = CTkButton(
        container_stpg, 
        text="Start",
        text_color="white",
        fg_color="#278F12",
        height=50,
        corner_radius=10,
        font=CTkFont("Georgia", size=20, weight="normal"),
        cursor="hand2",
        command=lambda: start_loading(progress_bar, start_label, app)
    )
    start_bttn.pack(pady=10)
    return container_stpg