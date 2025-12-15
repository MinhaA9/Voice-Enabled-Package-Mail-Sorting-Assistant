import pandas as pd
import time

class Database:
    def __init__(self):
        self.dict_dep_mail_db = None
        self.dict_emp_mail_db = None
        self.deps_dict = None
        self.names_dict = None
        self.empID_dict = None

    def read_databases(self, progress=None):
        steps = 4
        stp_count = 0
        df_dept = pd.read_csv("databases/mail_department.csv")
        self.dict_dep_mail_db = df_dept.to_dict(orient="records")

        self.deps_dict=dict()
        for dic in self.dict_dep_mail_db:
            if(dic["Department"] in self.deps_dict.keys()):
                self.deps_dict[dic["Department"]].append(dic)
            else:
                self.deps_dict[dic["Department"]] = []
                self.deps_dict[dic["Department"]].append(dic)
                stp_count+=1

        if(progress):
            progress(stp_count/steps, "Loaded Departments")
        time.sleep(0.1)

        df_emp = pd.read_csv("databases/employees.csv")  
        self.dict_emp_mail_db = df_emp.to_dict(orient="records")
        stp_count+=1
        if(progress):
            progress(stp_count/steps, "Loaded Employees")
        time.sleep(0.1)

        self.names_dict = {emp["Name"]: emp for emp in self.dict_emp_mail_db}
        stp_count+=1
        if(progress):
            progress(stp_count/steps, "Built 'Name' based Employee Database")
        time.sleep(0.1)

        self.empID_dict = {emp["EmpID"]: emp for emp in self.dict_emp_mail_db}
        stp_count+=1
        if(progress):
            progress(stp_count/steps, "Built 'Employee ID' based Employee Database") 
        time.sleep(0.1)