from backend_package_pickup_email import *
from datetime import datetime
import pandas as pd


class Lookup_Employee_Info:
    def __init__(self, db, info_type, info):
        self.db = db
        self.info_type = info_type
        self.info = info
    def set_info_type(self,info_type):
        self.info_type = info_type
    def get_info_type(self):
        return self.info_type
    def set_info(self, info):
        self.info = info
    def get_info(self):
        return self.info
    def get_all_info(self):
        if(self.info_type == "Name"):
            record = self.db.names_dict[self.info]
        elif(self.info_type == "Employee ID"):
            record = self.db.empID_dict[self.info]
        else:
            record = None
        print("\n========== Employee Information ==========")
        for k, v in record.items():
            print(f"{k:<12} : {v}")
        print("==========================================\n")
        return record
class Mail_Process:
    def __init__(self, db, mail_type):
        self.db = db
        self.mail_type = mail_type 

    def set_dep_or_name(self, dep_or_name):
        self.dep_or_name = dep_or_name

    def get_dep_or_name(self):
        return self.dep_or_name
    
    def set_info(self, info):
        self.info = info
        if(self.dep_or_name=="Name"):
            self.name = self.info
        if(self.dep_or_name=="Department"):
            self.department = self.info
            
    def get_info(self):
        return self.info
    
    def set_mail_type(self, mail_type):
        self.mail_type = mail_type

    def get_mail_type(self):
        return self.mail_type
    
    def set_return_to_sender(self, return_to_sender_mail):
            self.return_to_sender_mail = return_to_sender_mail
    
    def get_return_to_sender(self):
        return self.return_to_sender_mail

    def set_law_mail(self, law_mail):
        self.law_mail = law_mail

    def get_law_mail(self):
        return self.law_mail

    def get_box_num(self):
        if(self.dep_or_name=="Department"):
            record = self.db.deps_dict[self.department]
        elif(self.dep_or_name=="Name"):
            record = self.db.names_dict[self.name]
        else:
            record = None        
        return record
    def reset_all_vars_outside_mail(self):
        self.dep_or_name = None
        self.name = None
        self.department = None
        self.info = None
        self.return_to_sender_mail = None
        self.law_mail = None
    def collect_mail_data(self):
        now = datetime.now()
        day_name = now.strftime("%A")
        day = now.day
        month = now.month
        year = now.year
        print(self.mail_type)
        new_row={
            "Mail Type":self.mail_type,
            "Info Type":self.dep_or_name,
            "Info":self.info,
            "Return to Sender Mail":self.return_to_sender_mail,
            "Law Mail":self.law_mail,
            "Day Name":day_name,
            "Day":day,
            "Month":month,
            "Year":year
        }
        df = pd.read_csv("databases/mail_data.csv")
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("databases/mail_data.csv", index=False)
        print("New data has been added to mail data!")




class Package_Process:    
    def __init__(self):
        self.name = None
        self.email = None
        self.package_type = None
        self.tracking_num = None
        self.received_date = None

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_update_email(self):
        df = pd.read_csv("databases/employees.csv")
        df.loc[df["Name"]==self.name,"Email"]=self.email
        df.to_csv("databases/employees.csv", index=False)

    def set_email(self,email):
        self.email = email

    def get_email(self):
        return self.email
    
    def set_package_type(self, package_type):
        self.package_type = package_type

    def get_package_type(self):
        return self.package_type
    
    def set_tracking_num(self, tracking_num):
        self.tracking_num = tracking_num

    def get_tracking_num(self):
        return self.tracking_num
    
    def set_received_date(self, received_date):
        self.received_date = received_date

    def get_received_date(self):
        return self.received_date
    
    def send_pickup_email(self):
        self.collect_package_data()
        Subject="Package Pickup"
        Body=f"Hello {self.name},\n\nYour package is ready for pickup.\nPackage Type: {self.package_type}\nTracking Number: {self.tracking_num}"
        self.success = send_email_thread(self.email,Subject,Body)

    def set_pickedup(self):
        self.pickedup = True
        self.name = None
        self.email = None
        self.package_type = None
        self.tracking_num = None
        self.received_date = None

    def collect_package_data(self):
        now = datetime.now()
        day_name = now.strftime("%A")
        day = now.day
        month = now.month
        year = now.year
        new_row={
            "Name":self.name,
            "Email":self.email,
            "Package Type":self.package_type,
            "Tracking Number":self.tracking_num,
            "Received Date":self.received_date,
            "Day Name":day_name,
            "Day":day,
            "Month":month,
            "Year":year
        }
        df = pd.read_csv("databases/package_data.csv")
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("databases/package_data.csv", index=False)
        print("New data has been added to package data!")
