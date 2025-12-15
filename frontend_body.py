from customtkinter import *
from frontend_navigation_items import *
from frontend_startpage import *

def title_body(app):
    border_frame = CTkFrame(app, fg_color="black", height=104, corner_radius=0)
    border_frame.grid(row=0, column=1, sticky="EW", padx=(5,10), pady=(10,5))
    tbody = CTkFrame(border_frame, fg_color="#86cdf7")
    tbody.pack(fill="both", expand=True)
    title = CTkLabel(tbody, text="Voice-Enabled Package & Mail Sorting Assistant", text_color="#0B053D", font=CTkFont("Georgia", size=35, weight="bold"),height=100, corner_radius=10)
    title.pack()
    return tbody

def navigation_bar(app, main_body, cnt_mng):
    border_frame = CTkFrame(app, fg_color="black", width=154, corner_radius=0)
    border_frame.grid(row=0, column=0, rowspan=2, sticky="NS", padx=5, pady=10)
    nav_bar = CTkFrame(border_frame, fg_color="#0B053D", width=150, corner_radius=10)
    nav_bar.pack(fill="both", expand=True)
    navigation_items(app, nav_bar, main_body, cnt_mng)
    return nav_bar

def main_body(app):
    border_frame = CTkFrame(app, fg_color="black", corner_radius=0)
    border_frame.grid(row=1, column=1, sticky="EWNS", padx=(5,10), pady=(5,10))
    global mbody
    mbody = CTkFrame(border_frame, fg_color="#e3f1ff", corner_radius=10)
    mbody.pack(fill="both", expand=True)
    return mbody