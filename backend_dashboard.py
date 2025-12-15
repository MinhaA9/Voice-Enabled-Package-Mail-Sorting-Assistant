import pandas as pd
import matplotlib.pyplot as plt
import calendar

def load_data(csv_file):
    df = pd.read_csv(csv_file)
    df["Date"] = pd.to_datetime(df[["Year","Month","Day"]])
    df["DayName"] = df["Date"].dt.day_name()
    return df

def plot_by_day(df,pkg_mail, method = "Total Count", year="All Years"):
    if(year!="All Years"):
        df = df[df["Year"] == int(year)]
    if(pkg_mail=="Mail" and method=="Individual Count"):
        df=df[df["Info Type"]=="Name"]
    elif(pkg_mail=="Mail" and method=="Department Count"):
        df=df[df["Info Type"]=="Department"]
    
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts_by_day = (
        df["DayName"]
        .value_counts()
        .reindex(weekdays, fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    counts_by_day.plot(kind="bar", ax=ax)

    ax.set_xticklabels(weekdays,rotation=0)
    ax.set_xlabel("Day of Week")
    ax.set_ylabel(f"Number of {pkg_mail}")    
    title_year = f" ({year})" if year else ""
    ax.set_title(f"{pkg_mail} by Day of Week{title_year}")
    plt.tight_layout()
    # plt.show()
    return fig


def plot_by_month(df,pkg_mail, method = "Total Count", year="All Years"):
    if(year!="All Years"):
        df = df[df["Year"] == int(year)]
    if(pkg_mail=="Mail" and method=="Individual Count"):
        df=df[df["Info Type"]=="Name"]
    elif(pkg_mail=="Mail" and method=="Department Count"):
        df=df[df["Info Type"]=="Department"]
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    counts_by_month = (
        df["Month"]
        .value_counts()
        .reindex(months, fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    counts_by_month.plot(kind="bar", ax=ax)
    month_labels = [calendar.month_abbr[m] for m in months]
    ax.set_xticks(range(len(months)))
    ax.set_xticklabels(month_labels,rotation=0)
    ax.set_xlabel("Month")
    ax.set_ylabel(f"Number of {pkg_mail}")    
    title_year = f" ({year})" if year else ""
    ax.set_title(f"{pkg_mail} by Month {title_year}")
    plt.tight_layout()
    # plt.show()
    return fig

def plot_by_year(df,pkg_mail,method = "Total Count"):
    if(pkg_mail=="Mail" and method=="Individual Count"):
        df=df[df["Info Type"]=="Name"]
    elif(pkg_mail=="Mail" and method=="Department Count"):
        df=df[df["Info Type"]=="Department"]
    years = sorted(set(list(df["Year"])))
    counts_by_year = (
        df["Year"]
        .value_counts()
        .reindex(years, fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    counts_by_year.plot(kind="bar", ax=ax)
    ax.set_xticklabels(years,rotation=0)
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Number of {pkg_mail}")    
    ax.set_title(f"{pkg_mail} by Year")
    plt.tight_layout()
    # plt.show()
    return fig

