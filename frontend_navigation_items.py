from customtkinter import *
from PIL import Image
from frontend_startpage import *
from frontend_lookup_employee import *
from frontend_mail import *
from frontend_package import *
from frontend_voicemode import *
from frontend_dashboard import *

def navigation_items(app, nav_bar, main_body, cnt_mng):
    home_img = Image.open("images/home_icon.png")
    home_icon = CTkImage(dark_image=home_img, light_image=home_img, size=(70, 70))
    home_bttn= CTkButton(
        nav_bar, 
        image=home_icon,
        text="",
        fg_color="#d3f8b0",
        height=98,
        corner_radius=10,
        cursor="hand2",
        command=lambda: cnt_mng.show("start")
    )
    home_bttn.pack(fill="both", padx=2, pady=2)

    lookup_bttn = CTkButton(
        nav_bar, 
        text="Lookup Employee Info",
        text_color="white",
        fg_color="#1E73BE",
        height=50,
        corner_radius=10,
        font=CTkFont("Georgia", size=20, weight="normal"),
        cursor="hand2",
        command=lambda:lookup_empInfo_body(main_body, cnt_mng)
    )
    lookup_bttn.pack(fill="both", padx=2, pady=(50,0))

    mail_bttn = CTkButton(
        nav_bar, 
        text="Mail Assistance",
        text_color="white",
        fg_color="#1E73BE",
        height=50,
        corner_radius=10,
        font=CTkFont("Georgia", size=20, weight="normal"),
        cursor="hand2",
        command=lambda:mail_body(main_body, cnt_mng)
    )    
    mail_bttn.pack(fill="both", padx=2, pady=(0,0))

    package_bttn = CTkButton(
        nav_bar, 
        text="Package Assistance",
        text_color="white",
        fg_color="#1E73BE",
        height=50,
        corner_radius=10,
        font=CTkFont("Georgia", size=20, weight="normal"),
        cursor="hand2",
        command=lambda:package_body(main_body, cnt_mng)
    )
    package_bttn.pack(fill="both", padx=2, pady=(0,0))

    voice_img = Image.open("images/mic_icon.png")
    voice_icon = CTkImage(dark_image=voice_img, light_image=voice_img, size=(50, 20))
    voice_mode_bttn = CTkButton(
        nav_bar, 
        text="Voice Mode",
        text_color="white",
        image=voice_icon,
        compound="right",
        fg_color="#68B115",
        height=40,
        corner_radius=10,
        font=CTkFont("Georgia", size=20, weight="normal"),
        cursor="hand2",
        command=lambda:voice_mode_body(main_body, cnt_mng)
    )
    voice_mode_bttn.pack(fill="both", padx=2, pady=(0,10))
    dashboard_img = Image.open("images/dashboard_icon.png")
    dashboard_icon = CTkImage(dark_image=dashboard_img, light_image=dashboard_img, size=(70, 70))

    instruction_text = "Instruction:\n\n1. Click 'Start' to Load\n    Databases\n2. Choose an option from\n    the top to continue."
    instruction_box = CTkTextbox(
        nav_bar,
        width=200,
        height=200,
        text_color="yellow",
        font=CTkFont("Georgia", size=18, weight="normal")
    )
    instruction_box.insert("0.0", instruction_text)
    instruction_box.configure(state="disabled")  # make it read-only
    instruction_box.pack(fill="both", padx=2, pady=(40,10))

    dashboard_bttn= CTkButton(
        nav_bar, 
        image=dashboard_icon,
        compound="bottom",
        text="Dashboard",
        text_color="yellow",
        fg_color="#6366F1",
        height=98,
        corner_radius=10,
        font=CTkFont("Georgia", size=20, weight="normal"),
        cursor="hand2",
        command=lambda:dashboard_body(main_body, cnt_mng)
        )
    dashboard_bttn.pack(fill="both", padx=2, pady=2, side="bottom")
    return