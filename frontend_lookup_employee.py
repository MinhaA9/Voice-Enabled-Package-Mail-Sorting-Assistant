from customtkinter import *
from backend_mail_package import *
from frontend_startpage import db

def lookup_empInfo_body(main_body, cnt_mng):
    main_body.pack_propagate(False)
    cnt_mng.show("lookup")
    container_lk = cnt_mng.get("lookup")
    container_lk.grid_propagate(False)
    container_lk.grid_rowconfigure(0, weight=0)
    container_lk.grid_rowconfigure(1, weight=0)
    container_lk.grid_rowconfigure(2, weight=1)
    container_lk.grid_columnconfigure(0, weight=0)
    container_lk.grid_columnconfigure(1, weight=0)
    container_lk.grid_columnconfigure(2, weight=1)
    container_lk.grid_columnconfigure(3, weight=2)
    texts_label = CTkLabel(
        container_lk,
        text="Info Type:",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    texts_label.grid(row=0, column=0, padx=(20,5), pady=20, sticky="e")

    dropdown_opt = CTkComboBox(
        container_lk,
        values=["Select", "Name", "Employee ID"],
        width=160,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: get_selected_info_type(value)
    )
    dropdown_opt.grid(row=0, column=1, padx=(0,0), pady=20, sticky="e")


    info_label = CTkLabel(
        container_lk,
        text="Enter 'Name' or 'Employee ID':",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    info_label.grid(row=0, column=2, padx=(20,5), pady=20, sticky="e")
    text_info = CTkEntry(
        container_lk,
        width=150,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    text_info.grid(row=0, column=3, padx=(0,20), pady=20, sticky="ew")

    listbox_frame = CTkScrollableFrame(
        container_lk,
        height=200
    )
    listbox_frame.grid(row=1, column=3, padx=(0,20), pady=20, sticky="ew")
    employee_info_container = CTkFrame(
        container_lk,
        fg_color="transparent"
    )
    employee_info_container.grid(
        row=1,
        column=1,
        columnspan=2,
        padx=20,
        pady=20,
        sticky="nsew"
    )
    employee_info_label = CTkTextbox(
        employee_info_container,
        width=400,
        height=300,
        text_color="#0B053D",
        fg_color="transparent",
        font=CTkFont("Consolas", size=20),
        wrap="none"
    )
    employee_info_label.pack(expand=True, fill="both")
    text_info.bind("<KeyRelease>", lambda e: update_listbox(e,text_info,listbox_frame, employee_info_label))
    return container_lk

def update_listbox(event, info_entry, listbox_frame, employee_info_label):    
    if(sel_info_type=="Name"):
        list_info = get_all_names()
        input_entry = info_entry.get().lower()
    elif(sel_info_type=="Employee ID"):
        list_info_org = get_all_empIDs()
        list_info = [str(empid) for empid in list_info_org]
        input_entry = info_entry.get()

    for widget in listbox_frame.winfo_children():
        widget.destroy()

    for info in list_info:
        if(sel_info_type=="Name" and input_entry in info.lower()):
            btn = CTkButton(
                listbox_frame,
                text=info,
                width=200,
                height=35,
                anchor="center",
                font=CTkFont("Georgia", size=20, weight="normal"),
                command=lambda sel_info=info: on_listbox_select(sel_info, employee_info_label)
            )
            btn.pack(fill="x", padx=20, pady=2)
        elif(sel_info_type=="Employee ID" and input_entry in info):
            btn = CTkButton(
                listbox_frame,
                text=info,
                width=200,
                height=35,
                anchor="center",
                font=CTkFont("Georgia", size=20, weight="normal"),
                command=lambda sel_info=info: on_listbox_select(int(sel_info), employee_info_label)
            )
            btn.pack(fill="x", padx=20, pady=2)
def on_listbox_select(sel_info, employee_info_label):
    lk_emp_info = Lookup_Employee_Info(db,sel_info_type, sel_info)
    emp_info = lk_emp_info.get_all_info()
    info_lines = []
    info_lines.append("\n========== Employee Information ==========\n")

    for k, v in emp_info.items():
        info_lines.append(f"{k:<12} : {v}")
        
    info_lines.append("\n==========================================")

    formatted_text = "\n".join(info_lines)
    employee_info_label.configure(state="normal")
    employee_info_label.delete("0.0", "end")
    employee_info_label.insert("0.0", formatted_text)
    employee_info_label.configure(state="disabled")
    print(emp_info)
    
def get_all_names():
    return list(db.names_dict.keys())

def get_all_empIDs():
    return list(db.empID_dict.keys())

def get_selected_info_type(selected_info_type):
    global sel_info_type
    sel_info_type = selected_info_type