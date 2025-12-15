from customtkinter import *
from backend_voicemode import *
from backend_mail_package import *
from frontend_startpage import db
from rapidfuzz import process, fuzz
import re


import time

pkg_prs = Package_Process()
ml_prs = Mail_Process(db, "Select")
voice_result = {"value": None}
pkg_or_mail = {"value":None}

def voice_mode_body(main_body, cnt_mng):
    for child in cnt_mng.get("dashboard").winfo_children():
        child.destroy()
    main_body.pack_propagate(False)
    cnt_mng.show("voice")
    container_voice = cnt_mng.get("voice")
    container_voice.grid_propagate(False)
    container_voice.grid_rowconfigure(0, weight=0)
    container_voice.grid_rowconfigure(1, weight=1)
    container_voice.grid_columnconfigure(0, weight=1)
    top_container = CTkFrame(
        container_voice,
        fg_color="lightblue",
        height=80
    )
    top_container.grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky="ew"
    )
    top_container.grid_propagate(False)
    top_container.grid_rowconfigure(0, weight=1)
    top_container.grid_columnconfigure(0, weight=1)
    bottom_container = CTkFrame(
        container_voice,
        # fg_color="transparent"
        fg_color="lightblue"
    )
    bottom_container.grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        sticky="nsew"
    )
    bottom_container.grid_rowconfigure(0, weight=1)
    bottom_container.grid_columnconfigure(0, weight=1)
    voice_instr = "To Begin: Say 'Help with mail' or 'Help with package'\nTo Exit: Say 'Exit' to exit voice mode"
    instr_label = CTkLabel(
        top_container,
        text=voice_instr,
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    instr_label.grid(row=0, column=0, padx=(20,5), pady=20, sticky="ew")
    speak(voice_instr)
    result_label = CTkLabel(
        bottom_container,
        text="",
        text_color="#0B053D",
        font=CTkFont("Georgia", size=20, weight="normal")
    )
    result_label.grid(row=0, column=0, padx=(20,5), pady=20, sticky="ew")
    start_voice(result_label)

def start_voice(result_label):
    speak("Say 'Help with Packages' or 'Help with mail' or 'Exit'")
    time.sleep(5)
    start_listening_thread(command=None, callback=lambda result: get_selection(result,result_label))
    


def get_selection(result,result_label):
    print("Voice mode result:", result)
    pkg_or_mail["value"]=result
    result_label.configure(text=f"You have selected {result}")
    if result == "packages":
        package_process(result_label)
    elif result == "mails":
        speak("You selected mails and Entering Mail Process Mode")
        instr = "Give me the Employee Name and then say 'done'"
        time.sleep(3)
        speak(instr)
        append_result(instr,"",result_label)
        mail_process(result_label)
    elif result == "exit":
        speak("Exiting voice mode. Click on Voice Mode to continue voice mode")

def mail_process(result_label):    
    text="Employee Name: "
    command = "done"
    time.sleep(4)
    listen(command,text,result_label)
    

def show_employee_info(result_label):
    emp_dep_info = ml_prs.get_box_num()
    result_label.configure(text="")
    info_lines = []
    info_lines.append("\n========== Employee Information ==========\n")
    for k, v in emp_dep_info.items():
        info_lines.append(f"{k:<12} : {v}")
    info_lines.append("\n==========================================")   
    formatted_text = "\n".join(info_lines)
    result_label.configure(font=CTkFont(family="Consolas", size=18, weight="normal"),justify="left")
    result_label.after(0, lambda: append_result("", formatted_text, result_label))
    speak(f"Mail Box Number: {emp_dep_info["Mailbox Num"]}")
    ml_prs.collect_mail_data()    
    time.sleep(5)
    mail_process(result_label)

def get_name_result(text,result, result_label):
    if("exit" in result):
        speak("You have exited the voice mode")
    else:
        voice_result["value"] = split_names(result)
        print(voice_result["value"])
        if(voice_result["value"]!=[]):
            name = get_closest_name(voice_result["value"][0])
            speak(f"Employee Name: {name}")    
            result_label.after(0, lambda: append_result(text, name, result_label))
        else:
            speak(f"Please repeat the name")
            command = "done"
            listen(command,text,result_label)
        if(pkg_or_mail["value"]=="packages"):
            pkg_prs.set_name(name)
            pkg_prs.set_email(db.names_dict[name]["Email"])
            print(pkg_prs.get_email())
            speak("Give me the Package Type")
            append_result("Give me the Package Type", "", result_label)
            time.sleep(4)
            start_listening_thread(command="Package Type",callback=lambda result:get_package_type(result, result_label))
        elif(pkg_or_mail["value"]=="mails"):
            ml_prs.set_dep_or_name("Name")
            ml_prs.set_info(name)        
            ml_prs.set_mail_type("Address to Company")
            ml_prs.set_law_mail(None)
            ml_prs.set_return_to_sender(None)
            show_employee_info(result_label)



def get_package_type(result, result_label):
    voice_result["value"] = result
    result_label.after(0, lambda: append_result("Package Type: ", voice_result["value"], result_label))
    pkg_prs.set_package_type(voice_result["value"])
    speak(f"Package Type: {voice_result["value"]}")
    time.sleep(4)
    speak("Give me the Tracking Number")
    append_result("Give me the Tracking Number", "", result_label)
    time.sleep(3)
    start_listening_thread(command="done",callback=lambda result:get_tracking_num(result, result_label))

def filter_numbers(text):
    mapping = {"zero":"0","one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":7,"eight":"8","nine":"9"}
    digits = "".join(mapping[w] for w in text.split())
    print("Digits: ", digits)
    return digits

def get_tracking_num(result, result_label):
    text = re.sub(r"\s*done$", "", result)
    print(text)
    voice_result["value"] = filter_numbers(text)
    print(voice_result["value"])
    append_result("Tracking Number: ", str(voice_result["value"]), result_label)
    speak("Check the Tracking number to make sure it is correct")
    time.sleep(5)
    speak("Say 'Send Email' to send email for pickup")
    time.sleep(3)
    pkg_prs.set_tracking_num(voice_result["value"])
    start_listening_thread(command="Send Email",callback=lambda result:send_email_pickup(result, result_label))

def send_email_pickup(result, result_label):
    pkg_prs.send_pickup_email()    
    if(pkg_prs.success):
        msg = "Email was succesfully sent"
        speak(msg)
    else:
        msg = "Email cannot be sent"
        speak(msg)
    append_result(msg, "", result_label)
    speak("Say 'Help with Packages' or 'Help with mail' or 'Exit'")
    time.sleep(3)
    start_voice(result_label)

def append_result(text, result, result_label):
    current_text = result_label.cget("text")
    result_label.configure(text=current_text + "\n"+text + result)

def package_process(result_label):
    speak("You selected packages")
    instr = "Give me the Employee Name and then say 'done'"
    time.sleep(3)
    speak(instr)
    append_result(instr,"",result_label)
    text="Employee Name: "
    command = "done"
    time.sleep(4)
    listen(command,text,result_label)
    
def listen(command,text,result_label):
    listen_for_info_thread(command,callback=lambda result:get_name_result(text, result, result_label))

def split_names(name_str):        
    cleaned_names = re.findall(r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)+", name_str)
    return cleaned_names
def get_closest_name(input_name):
    name_list = list(db.names_dict.keys())
    match = process.extractOne(
        input_name,
        name_list,
        scorer=fuzz.ratio
    )
    if match is None:
        return None
    best_name, score, index = match
    if score < 50:
        return None
    return best_name