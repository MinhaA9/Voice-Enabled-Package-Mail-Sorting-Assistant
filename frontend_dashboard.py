from customtkinter import *
import pandas as pd
from backend_dashboard import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

selected_pkg_mail = None
selectd_sort_method="Total Count"
selected_time = None
selected_year = "All Years"

def dashboard_body(main_body, cnt_mng):
    for child in cnt_mng.get("dashboard").winfo_children():
        child.destroy()
    main_body.pack_propagate(False)
    cnt_mng.dashboard_show("dashboard")
    container_dashboard = cnt_mng.get("dashboard")
    container_dashboard.grid_propagate(False)
    container_dashboard.grid_rowconfigure(0, weight=0)
    container_dashboard.grid_rowconfigure(1, weight=1)
    container_dashboard.grid_columnconfigure(0, weight=1)
    top_container = CTkFrame(
        container_dashboard,
        fg_color="lightblue",
        height=100
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
    top_container.grid_columnconfigure(1, weight=1)
    top_container.grid_columnconfigure(2, weight=1)
    top_container.grid_columnconfigure(3, weight=1)
    mail_graph_container = CTkFrame(
        container_dashboard,
        fg_color="lightblue"
    )
    mail_graph_container.grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        sticky="nsew"
    )
    package_graph_container = CTkFrame(
        container_dashboard,
        # fg_color="transparent"
        fg_color="lightblue"
    )
    package_graph_container.grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        sticky="nsew"
    )
    hide_all(mail_graph_container,package_graph_container)
    dropdown_opt = CTkComboBox(
        top_container,
        values=["Select Item", "Mail", "Package"],
        width=160,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: get_selected_pkg_mail(value,mail_graph_container,package_graph_container,dropdown_opt_year)
    )
    dropdown_opt.grid(row=0, column=0, padx=40, pady=20, sticky="ew")
    dropdown_opt_method = CTkComboBox(
        top_container,
        values=["Total Count", "Individual Count", "Department Count"],
        width=160,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: get_selected_sort_method(value, mail_graph_container,package_graph_container)
    )
    dropdown_opt_method.grid(row=0, column=1, padx=40, pady=20, sticky="ew")
    dropdown_opt_time = CTkComboBox(
        top_container,
        values=["Select D/M/Y", "Day", "Month", "Year"],
        width=160,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: get_selected_time(value,mail_graph_container,package_graph_container)
    )
    dropdown_opt_time.grid(row=0, column=2, padx=40, pady=20, sticky="ew")

    dropdown_opt_year = CTkComboBox(
        top_container,
        values=["All Years"],
        width=160,
        height=30,
        font=CTkFont("Georgia", size=20, weight="normal"),
        command=lambda value: get_selected_year(value,mail_graph_container,package_graph_container)
    )
    dropdown_opt_year.grid(row=0, column=3, padx=40, pady=20, sticky="ew")

def hide_all(mail_graph_container,package_graph_container):
    mail_graph_container.grid_remove()
    package_graph_container.grid_remove()

def get_selected_pkg_mail(value, mail_graph_container,package_graph_container,dropdown_opt_year):
    global selected_pkg_mail
    selected_pkg_mail = value
    if(selected_pkg_mail=="Package"):
        mail_graph_container.grid_remove()
        package_graph_container.grid()
        years = get_years("Package")
    elif(selected_pkg_mail=="Mail"):
        mail_graph_container.grid()
        package_graph_container.grid_remove()
        years = get_years("Mail")
    else:
        years = ["All Years"]
    dropdown_opt_year.configure(values=years)
    dropdown_opt_year.set("All Years")
    if(selected_time != None):
        display_plot(mail_graph_container,package_graph_container)

def get_selected_sort_method(value, mail_graph_container,package_graph_container):
    global selectd_sort_method
    selectd_sort_method = value
    if(selected_pkg_mail != None and selected_time != None):
        display_plot(mail_graph_container,package_graph_container)

def get_selected_time(value,mail_graph_container,package_graph_container):
    global selected_time
    selected_time = value
    if(selected_time!=None and selected_pkg_mail!=None):
        display_plot(mail_graph_container,package_graph_container)
def get_selected_year(value,mail_graph_container,package_graph_container):
    global selected_year
    selected_year = value
    if(selected_time!="Year"):
        display_plot(mail_graph_container,package_graph_container)

def display_plot(mail_graph_container,package_graph_container):
    if (selected_pkg_mail == "Package"):
        csv_file = "databases/package_data.csv"
        frame=package_graph_container
    elif (selected_pkg_mail == "Mail"):
        csv_file = "databases/mail_data.csv"
        frame=mail_graph_container
    else:
        return
    df = load_data(csv_file)
    if(selected_time=="Day"):
        fig = plot_by_day(df, selected_pkg_mail,selectd_sort_method, selected_year)
    if(selected_time=="Month"):
        fig = plot_by_month(df, selected_pkg_mail,selectd_sort_method, selected_year)
    if(selected_time=="Year"):
        fig = plot_by_year(df, selected_pkg_mail,selectd_sort_method)

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def get_years(pkg_or_mail):
    if(pkg_or_mail=="Package"):
        df = pd.read_csv("databases/package_data.csv")
    elif(pkg_or_mail=="Mail"):
        df = pd.read_csv("databases/mail_data.csv")
    else:
        return ["All Years"]
    years = sorted(df["Year"].dropna().unique().tolist())
    years.insert(0, "All Years")
    return [str(y) for y in years]
