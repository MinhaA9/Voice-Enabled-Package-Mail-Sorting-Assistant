from customtkinter import *
from frontend_body import *
from frontend_startpage import *
from container_manager import ContainerManager

cnt_mng = ContainerManager()
set_appearance_mode("dark")
app = CTk()
app.geometry("1500x900")
def force_redraw(event=None):
    app.update_idletasks()
    app.attributes("-alpha", 1.0)

app.bind("<Configure>", force_redraw)
app.title("Voice-Enabled Package & Mail Sorting")
app.grid_rowconfigure(0, weight=0)
app.grid_rowconfigure(1, weight=1)  
app.grid_columnconfigure(0, weight=0)
app.grid_columnconfigure(1, weight=1)
title_body(app)
mbody = main_body(app)
cnt_start = CTkFrame(mbody, fg_color="#e3f1ff")
cnt_lookup = CTkFrame(mbody, fg_color="#dcebfa", height=600, width=1100)
cnt_mail = CTkFrame(mbody, fg_color="#dcebfa", height=600, width=1100)
cnt_package = CTkFrame(mbody, fg_color="#dcebfa", height=600, width=1100)
cnt_dashboard = CTkFrame(mbody,fg_color="#dcebfa")
cnt_voice_mode = CTkFrame(mbody, fg_color="#dcebfa", height=600, width=1100)

cnt_mng.register("start", cnt_start)
cnt_mng.register("lookup", cnt_lookup)
cnt_mng.register("mail", cnt_mail)
cnt_mng.register("package", cnt_package)
cnt_mng.register("voice",cnt_voice_mode)
cnt_mng.register("dashboard",cnt_dashboard)

cnt_mng.hide_all()

navigation_bar(app, mbody, cnt_mng)
start_body(mbody,app, cnt_mng)
def on_exit():
    import matplotlib.pyplot as plt
    plt.close("all")
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_exit)
app.mainloop()