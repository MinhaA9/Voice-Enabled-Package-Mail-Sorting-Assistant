from customtkinter import *
from backend_mail_package import *
from frontend_startpage import db


ml_prs = Mail_Process(db, "Select")

def mail_body(main_body, cnt_mng):
    for child in cnt_mng.get("mail").winfo_children():
        child.destroy()

    main_body.pack_propagate(False)
    cnt_mng.show("mail")
    container_mail = cnt_mng.get("mail")
    container_mail.grid_propagate(False)
    container_mail.grid_rowconfigure(0, weight=0)
    container_mail.grid_rowconfigure(1, weight=0)
    container_mail.grid_rowconfigure(2, weight=1)
    container_mail.grid_columnconfigure(0, weight=0)
    container_mail.grid_columnconfigure(1, weight=0)
    container_mail.grid_columnconfigure(2, weight=1)
    container_mail.grid_columnconfigure(3, weight=2)
    """
    Define all containers
    ---------------------------------------------------------
    """
    return_container = CTkFrame(
        container_mail,
        fg_color="transparent"
    )
    return_container.grid(
        row=0,
        column=2,
        padx=10,
        pady=20,
        sticky="nsew"
    )
    law_container = CTkFrame(
        container_mail,
        fg_color="transparent"
    )
    law_container.grid(
        row=0,
        column=3,
        padx=10,
        pady=20,
        sticky="nsew"
    )
    dep_name_container = CTkFrame(container_mail,fg_color="transparent")
    dep_name_container.grid(
        row=1,
        column=0,
        columnspan=3,
        padx=(0,20),
        pady=20,
        sticky="nsew"
    )
    employee_info_container = CTkFrame(
        container_mail,
        fg_color="transparent"
    )
    employee_info_container.grid(
        row=1,
        column=1,
        columnspan=2,
        padx=(0,20),
        pady=20,
        sticky="nsew"
    )
    listbox_frame_container = CTkFrame(
        container_mail,
        fg_color="transparent"
    )
    listbox_frame_container.grid(
        row=2,
        column=2,
        columnspan=3,
        padx=(160,20),
        pady=(40,20),
        sticky="nsew"
    )
    hide_all(employee_info_container,return_container, law_container, dep_name_container, listbox_frame_container)
    """
    ---------------------------------------------------------
    """
    texts_label = CTkLabel(
        container_mail,
        text="Mail Type:",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    texts_label.grid(row=0, column=0, padx=(20,5), pady=20, sticky="e")
    dropdown_opt = CTkComboBox(
        container_mail,
        values=["Select", "Address to Company", "Address to another place"],
        width=280,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: initialize_mail_process(value, employee_info_container, employee_info_label, return_container, law_container, dep_name_container, dropdown_opt_rt,listbox_frame_container)
    )
    dropdown_opt.grid(row=0, column=1, padx=(0,0), pady=20, sticky="w")
    """
    Return to sender mail
    """
    return_label = CTkLabel(
        return_container,
        text="Return to sender mail:",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    return_label.grid(row=0, column=0, padx=(20,5), pady=20, sticky="e")
    dropdown_opt_rt = CTkComboBox(
        return_container,
        values=["Select", "Yes", "No"],
        width=100,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: nextstep_mail_process(value, employee_info_container, employee_info_label, law_container, dep_name_container, listbox_frame_container, dropdown_opt_lw)
    )
    dropdown_opt_rt.grid(row=0, column=1, padx=(0,0), pady=20, sticky="w")
    """
    Law mail
    """
    law_label = CTkLabel(
        law_container,
        text="Law mail?",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    law_label.grid(row=0, column=0, padx=(20,5), pady=20, sticky="e")
    dropdown_opt_lw = CTkComboBox(
        law_container,
        values=["Select", "Yes", "No"],
        width=100,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: return_sender_process(value, employee_info_container, employee_info_label)
    )
    dropdown_opt_lw.grid(row=0, column=1, padx=(0,0), pady=20, sticky="w")

    """
    Looking up Mailbox Num by Department or Name
    ---------------------------------------------------------
    """
    texts_info_label = CTkLabel(
        dep_name_container,
        text="Info Type:",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    texts_info_label.grid(row=0, column=0, padx=(20,5), pady=20, sticky="e")

    dropdown_opt_info = CTkComboBox(
        dep_name_container,
        values=["Select", "Name", "Department"],
        width=160,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: get_selected_info_type(value)
    )
    dropdown_opt_info.grid(row=0, column=1, padx=(0,0), pady=20, sticky="e")
    info_label = CTkLabel(
        dep_name_container,
        text="Enter 'Name' or 'Department':",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    info_label.grid(row=0, column=2, padx=(20,5), pady=20, sticky="e")
    text_info = CTkEntry(
        dep_name_container,
        width=400,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    text_info.grid(row=0, column=3, padx=(0,20), pady=20, sticky="ew")
    
    listbox_frame = CTkScrollableFrame(
        listbox_frame_container,
        width=400,
        height=200
    )
    listbox_frame.grid(row=0, column=0, padx=(0,20), pady=20, sticky="ew")    
    """
    ---------------------------------------------------------
    """
   
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
    return container_mail

def update_listbox(event, info_entry, listbox_frame, employee_info_label):   
    input_entry = info_entry.get().lower()
    if(sel_info_type=="Name"):
        list_info = get_all_names()
    elif(sel_info_type=="Department"):
        list_info = get_all_departments()

    for widget in listbox_frame.winfo_children():
        widget.destroy()

    for info in list_info:
        if(input_entry in info.lower()):
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

def on_listbox_select(sel_info, employee_info_label):
    ml_prs.set_info(sel_info)
    emp_dep_info = ml_prs.get_box_num()
    info_lines = []
    info_lines.append("\n========== Employee Information ==========\n")
    if(sel_info_type=="Name"):
        for k, v in emp_dep_info.items():
            info_lines.append(f"{k:<12} : {v}")
    elif(sel_info_type=="Department"):
        for dep_info in emp_dep_info:
            for k, v in dep_info.items():
                info_lines.append(f"{k:<12} : {v}")
            info_lines.append("-" * 40)
    info_lines.append("\n==========================================")   
    formatted_text = "\n".join(info_lines)    
    set_employee_info_label(employee_info_label, formatted_text)
    ml_prs.collect_mail_data()
    print(emp_dep_info)

def get_all_names():
    return list(db.names_dict.keys())
def get_all_departments():
    return list(db.deps_dict.keys())

def return_sender_process(is_law_mail,employee_info_container, employee_info_label):
    set_grid_employee_container(employee_info_container, 1, 2, 3, 20)
    if(is_law_mail=="Yes"):
        text="Return mail to Law Department"
        ml_prs.set_law_mail(True)
    elif(is_law_mail=="No"):
        text="Place mail in shredding bin"
        ml_prs.set_law_mail(False)      
    set_employee_info_label(employee_info_label, text)
    ml_prs.collect_mail_data()

def nextstep_mail_process(return_to_sender_mail, employee_info_container, employee_info_label, law_container, dep_name_container, listbox_frame_container, dropdown_opt_lw):
    dropdown_opt_lw.set("Select")    
    if(return_to_sender_mail=="Yes"):
        ml_prs.set_return_to_sender(True)
        ml_prs.set_dep_or_name(None)
        ml_prs.set_info(None)
        dep_name_container.grid_remove()
        listbox_frame_container.grid_remove()
        law_container.grid()
    elif(return_to_sender_mail=="No"):
        ml_prs.set_return_to_sender(False)
        ml_prs.set_law_mail(None)
        law_container.grid_remove()
        set_employee_info_label(employee_info_label,"")
        set_grid_employee_container(employee_info_container, 2, 0, 3, 20)
        dep_name_container.grid()
        listbox_frame_container.grid()
            
def emp_content_label(employee_info_container,employee_info_label, return_container, law_container, dep_name_container, listbox_frame_container):
    set_grid_employee_container(employee_info_container, 1, 1, 2, 0)
    return_container.grid_remove()
    law_container.grid_remove()
    dep_name_container.grid_remove()
    listbox_frame_container.grid_remove()
    text = ""
    if(ml_prs.get_mail_type()=="Address to another place"):
        text="Place mail in misdirected mailbox"
        ml_prs.reset_all_vars_outside_mail()
        ml_prs.collect_mail_data()
    elif(ml_prs.get_mail_type()=="Address to Company"):
        return_container.grid()
        text=""
    set_employee_info_label(employee_info_label, text)
    
def initialize_mail_process(selected_mail_type, employee_info_container,employee_info_label, return_container, law_container, dep_name_container,dropdown_opt_rt, listbox_frame_container): 
    if selected_mail_type == "Select":
        return
    dropdown_opt_rt.set("Select")
    ml_prs.set_mail_type(selected_mail_type)
    emp_content_label(employee_info_container, employee_info_label, return_container, law_container, dep_name_container, listbox_frame_container)

def set_employee_info_label(employee_info_label, text):
    employee_info_label.configure(state="normal")
    employee_info_label.delete("0.0", "end")
    employee_info_label.insert("0.0", text)
    employee_info_label.configure(state="disabled")

def set_grid_employee_container(employee_info_container, row, col, colspan, xleft):
    employee_info_container.grid(
        row=row,
        column=col,
        columnspan=colspan,
        padx=(xleft,20),
        pady=20,
        sticky="nsew"
    )

def get_selected_info_type(selected_info_type):
    global sel_info_type
    sel_info_type = selected_info_type
    ml_prs.set_dep_or_name(sel_info_type)

def hide_all(employee_info_container,return_container, law_container, dep_name_container,listbox_frame_container):
        employee_info_container.grid_remove()
        return_container.grid_remove()
        law_container.grid_remove()
        dep_name_container.grid_remove()
        listbox_frame_container.grid_remove()