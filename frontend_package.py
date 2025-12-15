from customtkinter import *
from datetime import datetime
from backend_mail_package import *
from frontend_startpage import db

pkg_prs = Package_Process()

def package_body(main_body, cnt_mng):
    for child in cnt_mng.get("package").winfo_children():
        child.destroy()
    main_body.pack_propagate(False)
    cnt_mng.show("package")
    container_package = cnt_mng.get("package")
    container_package.grid_propagate(False)
    container_package.grid_rowconfigure(0, weight=0)
    container_package.grid_rowconfigure(1, weight=0)
    container_package.grid_rowconfigure(2, weight=0)
    container_package.grid_rowconfigure(3, weight=0)
    container_package.grid_rowconfigure(4, weight=0)
    container_package.grid_rowconfigure(5, weight=0)
    container_package.grid_columnconfigure(0, weight=0)
    container_package.grid_columnconfigure(1, weight=0)
    container_package.grid_columnconfigure(2, weight=0)
    container_package.grid_columnconfigure(3, weight=0)

    name_label=CTkLabel(
        container_package,
        text="Name:",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    name_label.grid(row=0, column=0, padx=(20,5), pady=20, sticky="e")

    name_entry = CTkEntry(
        container_package,
        width=400,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    name_entry.grid(row=0, column=1, padx=(0,5), pady=20, sticky="ew")
    listbox_frame = CTkScrollableFrame(
        container_package,
        width=400,
        height=200
    )
    listbox_frame.grid(
        row=1,
        rowspan=2,
        column=1,
        padx=(0,20),
        pady=20,
        sticky="ew"
    ) 
    name_entry.bind("<KeyRelease>", lambda e: update_listbox(e,name_entry,email_entry,listbox_frame))
    package_type_label=CTkLabel(
        container_package,
        text="Package Type:",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    package_type_label.grid(row=0, column=2, padx=(0,5), pady=20, sticky="e")
    dropdown_opt_package = CTkComboBox(
        container_package,
        values=["Select", "Amazon","FedEx","UPS","USPS"],
        width=160,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: selected_package_type_val(value)
    )
    dropdown_opt_package.grid(row=0, column=3, padx=(0,0), pady=20, sticky="w")

    track_num_label=CTkLabel(
        container_package,
        text="Tracking Number:",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    track_num_label.grid(row=1, column=2, padx=(20,5), pady=20, sticky="e")
    track_num_entry = CTkEntry(
        container_package,
        width=300,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    track_num_entry.grid(row=1, column=3, padx=(0,20), pady=20, sticky="w")

    date_label=CTkLabel(
        container_package,
        text="Date:",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    date_label.grid(row=2, column=2, padx=(20,5), pady=20, sticky="e")
    date_current=CTkLabel(
        container_package,
        text=f"{str(datetime.now())}",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    date_current.grid(row=2, column=3, padx=(5,5), pady=20, sticky="w")
    track_num_entry.bind("<KeyRelease>", lambda event,date=date_current: track_num_entry_val(event, date))
    email_label=CTkLabel(
        container_package,
        text="Email:",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    email_label.grid(row=3, column=0, padx=(20,5), pady=20, sticky="e")

    email_entry = CTkEntry(
        container_package,
        width=400,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
    )
    email_entry.grid(row=3, column=1, padx=(0,5), pady=20, sticky="ew")
    email_entry.bind("<KeyRelease>", lambda event,date=date_current:update_email(event,date))

    send_email_bttn = CTkButton(
        container_package,
        text="Send Email",
        width=100,
        height=30,
        anchor="center",
        font=CTkFont("Georgia", size=20, weight="normal"),
        cursor="hand2",
        command=lambda:send_email_and_update(success_label)
    )
    send_email_bttn.grid(row=4, column=1, padx=(0,5), pady=20, sticky="ew")
    
    success_label=CTkLabel(
        container_package,
        text="",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    success_label.grid(row=5, column=1, padx=(20,5), pady=20, sticky="e")
    return container_package
def send_email_and_update(success_label):
    pkg_prs.send_pickup_email()
    if pkg_prs.success:
        success_label.configure(text="Email was successfully sent!")
    else:
        success_label.configure(text="Email cannot be sent!")
def update_listbox(event, name_entry, email_entry,listbox_frame):   
    name_input = name_entry.get().lower()
    names_list = get_all_names()
    for widget in listbox_frame.winfo_children():
        widget.destroy()
    for name in names_list:
        if(name_input in name.lower()):
            btn = CTkButton(
                listbox_frame,
                text=name,
                width=200,
                height=35,
                anchor="center",
                font=CTkFont("Georgia", size=20, weight="normal"),
                command=lambda sel_name=name: update_name_entry(sel_name, name_entry, email_entry)
            )
            btn.pack(fill="x", padx=20, pady=2)
def update_name_entry(sel_name,name_entry, email_entry):
    name_entry.delete(0, "end")
    name_entry.insert(0, sel_name)    
    pkg_prs.set_name(sel_name)
    email = get_email(sel_name)
    if(not pd.isna(email)):
        pkg_prs.set_email(email)
        email_entry.delete(0, "end")
        email_entry.insert(0, email) 

    
def get_all_names():
    return list(db.names_dict.keys())

def get_email(name):
    return db.names_dict[name]["Email"]

def update_email(event,current_date):
    email = event.widget.get()
    pkg_prs.set_email(email)
    pkg_prs.set_update_email()
    print(pkg_prs.email)
    date=datetime.now()
    current_date.configure(text=f"{date}")
    pkg_prs.set_received_date(date)

def selected_package_type_val(sel_pkg_tp):
    pkg_prs.set_package_type(sel_pkg_tp)
    
def track_num_entry_val(event, current_date):
    trk_num = event.widget.get()
    pkg_prs.set_tracking_num(trk_num)
    print(pkg_prs.get_tracking_num())
    date=datetime.now()
    current_date.configure(text=f"{date}")
    pkg_prs.set_received_date(date)
    print(pkg_prs.get_received_date())