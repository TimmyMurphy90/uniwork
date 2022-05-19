import re
import pandas as pd
import math
from collections import Counter
import json

# GUI imports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# matplotlib for graph drawing
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


# GLOBAL VARIABLES (FOR INSPECTIONS & VIOLATIONS)
aiport = []
viol = []
inv = []

# Flag to know if JSON file is imported or not
isJSON = False


def get_inventory():
    # Reads the inventory.csv file via asking user to select the appropriate file
    filename = filedialog.askopenfilename(
        initialdir="./", title="Select Inventory File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    inventory = pd.read_csv(filename)

    return inventory


def get_inspections():
    # Reads the inspections.csv file via asking user to select the appropriate file
    filename = filedialog.askopenfilename(
        initialdir="./", title="Select Inspections File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    inspections = pd.read_csv(filename)

    count = 0
    droplist = []
    for i in inspections["PROGRAM STATUS"]:
        if i == "INACTIVE":
            droplist.append(count)  # Remove inactive entries
        count += 1
    inspections = inspections.drop(droplist)
    return inspections


def get_violations():
    # Reads the violations.csv file via asking user to select the appropriate file
    filename = filedialog.askopenfilename(
        initialdir="./", title="Select Violations File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    violations = pd.read_csv(filename)


    return violations


def get_seats(inventory):
    # Gets the seat types of each item in the inventory
    seat_types = []
    if not isJSON:
        for item in inventory["PE DESCRIPTION"]:
            seat_types.append(re.findall(r'\((.*?)\)', item))
    else:
        seat_types = inventory["PE DESCRIPTION"].tolist()

    return seat_types


def manipulate_data_zips(inspections):
    # Manipulates the data of the Inspection Score for each zip code per year

    dates = inspections["ACTIVITY DATE"]
    scores = inspections["SCORE"]
    zip_codes = inspections["Zip Codes"]

    zips = []
    for zip_ in zip_codes:
        zips.append(zip_)
    scores_ = []
    for score in scores:
        scores_.append(score)
    years = []
    for date in dates:
        year = ""
        for i in date:
            if i.isdigit():
                year += i
            else:
                year = ""
        years.append(year)
    d = {'Score': scores_, 'Year': years, 'Zip': zip_codes}
    data = pd.DataFrame(data=d)     # A DataFrame which holds the data for each zip for each year

    unique_years = list(set(years))

    unique_zips = []

    for zip_ in zip_codes:
        if zip_ not in unique_zips and not math.isnan(zip_):
            unique_zips.append(zip_)

    data_for_zips = []  
    for zip_ in unique_zips:
        for year in unique_years:
            data_for_zips.append(
                data.loc[(data['Zip'] == zip_) & (data['Year'] == year)])

    final_zip_data = []
    for data_ in data_for_zips:
        if data_.empty:
            continue
        mean = data_.mean()
        mode = data_.mode()
        median = data_.median()
        mode_year = 0
        try:
            mode_year = mode["Score"][0]
        except IndexError:
            pass
        median_ = median[0]
        if math.isnan(median_):
            median_ = 0
        zip_data = [data_["Year"].tolist()[0], data_["Zip"].tolist()[
            0], mean[0], mode_year, median_]
        final_zip_data.append(zip_data)

    return final_zip_data


def manipulate_data_seats(inspections):
    # Manipulates the inspections data for each seat type per year

    dates = inspections["ACTIVITY DATE"]
    scores = inspections["SCORE"]
    seats = inspections["PE DESCRIPTION"]

    seats_ = []
    for seat in seats:
        if "HIGH RISK" in seat:
            seats_.append("HIGH")
        elif "MODERATE RISK" in seat:
            seats_.append("MODERATE")
        elif "LOW RISK" in seat:
            seats_.append("LOW")
        else:
            seats_.append("UNSPECIFIED")

    scores_ = []
    for score in scores:
        scores_.append(score)

    years = []
    for date in dates:
        year = ""
        for i in date:
            if i.isdigit():
                year += i
            else:
                year = ""
        years.append(year)

    unique_years = list(set(years))

    d = {'Score': scores_, 'Year': years, 'Seat Risk': seats_}
    data = pd.DataFrame(data=d)

    seat_types = ["HIGH", "MODERATE", "LOW"]

    data_for_seats = []  # A DataFrame that hold the data for each seat type for each year
    for seat_ in seat_types:
        for year in unique_years:
            data_for_seats.append(
                data.loc[(data['Seat Risk'] == seat_) & (data['Year'] == year)])

    final_seat_data = []
    for data_ in data_for_seats:
        if data_.empty:
            continue
        mean = data_.mean()
        mode = data_.mode()
        median = data_.median()
        mode_year = 0
        try:
            mode_year = mode["Score"][0]
        except IndexError:
            pass
        median_ = median[0]
        if math.isnan(median_):
            median_ = 0
        seat_data = [data_["Year"].tolist()[0], data_["Seat Risk"].tolist()[
            0], mean[0], mode_year, median_]
        final_seat_data.append(seat_data)

    return final_seat_data


def get_violations_count(violations):
    codes = violations["VIOLATION CODE"].tolist()

    unique_codes = list(set(codes))

    # Get count of each item in the list
    counts = Counter(codes)
    return unique_codes, counts


def get_correlation(violations, inspections):
    # Tries to find a correlation between violations by each vendor and their zip codes
    serials = violations["SERIAL NUMBER"].tolist() # Get a list of all serial numbers
    insp_serials = inspections["SERIAL NUMBER"].tolist()
    zips = inspections["Zip Codes"].tolist()

    zips_ = []

    serials = Counter(serials) # Get number of violations for each vendor
    for serial in serials:
        count = 0
        for s in insp_serials:
            if serial == s and not math.isnan(zips[count]):
                zips_.append((zips[count], serials[serial]))
            count += 1
    return zips_


def load_data():
    # Loads the data into the program

    global insp, viol, inv, isJSON       # Loads data sets into global variables

    isJSON = False

    insp = get_inspections()                         
    viol = get_violations()
    inv = get_inventory()
    frames = [insp, viol, inv]
    show["state"] = NORMAL
    graph_seats_btn["state"] = NORMAL
    graph_zips_btn["state"] = NORMAL
    graph_viols_btn["state"] = NORMAL

def load_saved():
    # Loads the data from a JSON file instead

    global inv, insp, viol, isJSON

    isJSON = True # The files loaded now are imported from JSON files

    invfile = filedialog.askopenfilename( initialdir="./", title="Import inv.json File", filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))

    inspfile = filedialog.askopenfilename( initialdir="./", title="Import insp.json File", filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))

    violfile = filedialog.askopenfilename( initialdir="./", title="Import viol.json File", filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))

    invData = json.load(open(invfile))
    inspData = json.load(open(inspfile))
    violData = json.load(open(violfile))

    inv = pd.DataFrame(invData["data"])
    insp = pd.DataFrame(inspData["data"])
    viol = pd.DataFrame(violData["data"])

    show["state"] = NORMAL
    graph_seats_btn["state"] = NORMAL
    graph_zips_btn["state"] = NORMAL
    graph_viols_btn["state"] = NORMAL
    

def show_data():
    # Open a new window and show the data extracted

    global inv

    seats = get_seats(inv)

    dataWindow = Toplevel(root)
    dataWindow.title("Show Data")

    verscrlbar = ttk.Scrollbar(dataWindow, orient="vertical")
    verscrlbar.pack(side='right', fill='y')
    horscrlbar = ttk.Scrollbar(dataWindow, orient="horizontal")

    save = Button(dataWindow, text="Save Data", font=(
        "Arial", 14), command=lambda: save_data(seats))
    save.pack(side='bottom')

    saved = Label(dataWindow, text="Data Saved Successfully!",
                  font=("Arial", 12), fg='green')

    horscrlbar.pack(side='bottom', fill='x')

    treev = ttk.Treeview(dataWindow, selectmode='browse',
                         yscrollcommand=verscrlbar.set, xscrollcommand=horscrlbar.set)
    treev.pack(side='left', fill=BOTH)

    verscrlbar.configure(command=treev.yview)
    horscrlbar.configure(command=treev.xview)

    treev["columns"] = tuple(inv.columns)
    treev['show'] = 'headings'

    for column in tuple(inv.columns):
        treev.column(column, width=200, anchor='c')
        treev.heading(column, text=column)

    for index, row in inv.iterrows():
        row[5] = seats[index]
        treev.insert("", 'end', text="L"+str(index), values=tuple(row))

    def save_data(seats):
        data = inv
        data['PE DESCRIPTION'] = seats
        invData = data.to_json(orient='table', index=False)
        inspData = insp.to_json(orient='table', index=False)
        violData = viol.to_json(orient='table', index=False)
        parsedInv = json.loads(invData)
        parsedInsp = json.loads(inspData)
        parsedViol = json.loads(violData)
        with open('inv.json', 'w') as f:
            json.dump(parsedInv, f)
        with open('insp.json', 'w') as f:
            json.dump(parsedInsp, f)
        with open('viol.json', 'w') as f:            
            json.dump(parsedViol, f)
        saved.pack(side='bottom', fill=BOTH, expand=True)


def plot_seats():
    # Plots the first graph: Inspection Score Per Year for each type of vendor's seating

    plotWindow = Toplevel(root)
    plotWindow.title("Graph data for Vendor Seating")

    btn_frame = Frame(plotWindow)
    btn_frame.pack(side='bottom')

    data = manipulate_data_seats(insp)

    # Defining containers for plot data
    unique_years = []
    seat_data = []
    mean_data = []
    mode_data = []
    median_data = []

    for data_ in data:
        year = data_[0]
        if year not in unique_years:
            unique_years.append(year)

    unique_years.sort()
    for year in unique_years:
        Button(btn_frame, text=year, command=lambda year=year: update_graph(
            year)).pack(side='left')
        seats = []
        means = []
        modes = []
        medians = []
        for data_ in data:
            if year == data_[0]:
                seats.append(data_[1])
                means.append(data_[2])
                modes.append(data_[3])
                medians.append(data_[4])
        seat_data.append(seats)
        mean_data.append(means)
        mode_data.append(modes)
        median_data.append(medians)

    fig = Figure(figsize=(12, 6))

    plot_mean = fig.add_subplot(131)
    plot_mean.title.set_text('Mean Data')
    plot_mean.bar(seat_data[0], mean_data[0])
    plot_mode = fig.add_subplot(132)
    plot_mode.title.set_text('Mode Data')
    plot_mode.bar(seat_data[0], mode_data[0])
    plot_median = fig.add_subplot(133)
    plot_median.title.set_text('Median Data')
    plot_median.bar(seat_data[0], median_data[0])

    plot_mean.tick_params(axis='x', labelrotation=30)
    plot_mode.tick_params(axis='x', labelrotation=30)
    plot_median.tick_params(axis='x', labelrotation=30)

    canvas = FigureCanvasTkAgg(fig, master=plotWindow)
    canvas.draw()

    canvas.get_tk_widget().pack(side='top')
    toolbar = NavigationToolbar2Tk(canvas, plotWindow)
    toolbar.update()

    canvas.get_tk_widget().pack()

    def update_graph(year):
        index = unique_years.index(year)
        print(year)

        fig.clf()

        plot_mean = fig.add_subplot(131)
        plot_mean.title.set_text('Mean Data')
        plot_mean.bar(seat_data[index], mean_data[index])
        plot_mode = fig.add_subplot(132)
        plot_mode.title.set_text('Mode Data')
        plot_mode.bar(seat_data[index], mode_data[index])
        plot_median = fig.add_subplot(133)
        plot_median.title.set_text('Median Data')
        plot_median.bar(seat_data[index], median_data[index])

        canvas.draw()


def plot_zips():
    # Plot the second graph: Inspection Score Per Year for each Zip-Code

    plotWindow = Toplevel(root)
    plotWindow.title("Graph data for Zip Code")

    btn_frame = Frame(plotWindow)
    btn_frame.pack(side='bottom')

    data = manipulate_data_zips(insp)

    # Defining containers for plot data
    unique_years = []
    zip_data = []
    mean_data = []
    mode_data = []
    median_data = []

    for data_ in data:
        year = data_[0]
        if year not in unique_years:
            unique_years.append(year)

    unique_years.sort()
    for year in unique_years:
        Button(btn_frame, text=year, command=lambda year=year: update_graph(
            year)).pack(side='left')
        zips = []
        means = []
        modes = []
        medians = []
        for data_ in data:
            if year == data_[0]:
                zips.append(str(data_[1]))
                means.append(data_[2])
                modes.append(data_[3])
                medians.append(data_[4])
        zip_data.append(zips)
        mean_data.append(means)
        mode_data.append(modes)
        median_data.append(medians)

    fig = Figure(figsize=(20, 6))

    plot_mean = fig.add_subplot(131)
    plot_mean.title.set_text('Mean Data')
    plot_mean.bar(zip_data[0], mean_data[0])
    plot_mode = fig.add_subplot(132)
    plot_mode.title.set_text('Mode Data')
    plot_mode.bar(zip_data[0], mode_data[0])
    plot_median = fig.add_subplot(133)
    plot_median.title.set_text('Median Data')
    plot_median.bar(zip_data[0], median_data[0])

    plot_mean.tick_params(axis='x', labelrotation=45)
    plot_mode.tick_params(axis='x', labelrotation=45)
    plot_median.tick_params(axis='x', labelrotation=45)

    fig.set_tight_layout(True)

    canvas = FigureCanvasTkAgg(fig, master=plotWindow)
    canvas.draw()

    canvas.get_tk_widget().pack(side='top')
    toolbar = NavigationToolbar2Tk(canvas, plotWindow)
    toolbar.update()

    canvas.get_tk_widget().pack()

    def update_graph(year):
        index = unique_years.index(year)
        print(year)

        fig.clf()  # Clears the previous plot and plots new data

        plot_mean = fig.add_subplot(131)
        plot_mean.title.set_text('Mean Data')
        plot_mean.bar(zip_data[index], mean_data[index])
        plot_mode = fig.add_subplot(132)
        plot_mode.title.set_text('Mode Data')
        plot_mode.bar(zip_data[index], mode_data[index])
        plot_median = fig.add_subplot(133)
        plot_median.title.set_text('Median Data')
        plot_median.bar(zip_data[index], median_data[index])

        canvas.draw()  # Update the plot figure


def plot_violations():
    # Plot the third graph: Graph For Each Type of Violation

    plotWindow = Toplevel(root)
    plotWindow.title("Graph data for Violations")

    btn_frame = Frame(plotWindow)
    btn_frame.pack(side='bottom')

    codes, count = get_violations_count(viol)
    zips = get_correlation(viol, insp)

    counts = []
    for c in count:
        counts.append(count[c])
    fig = Figure(figsize=(12, 6))

    zips_ = []
    zip_count = []
    highest_zip = ""
    max = 0
    for i in zips:
        zips_.append(str(i[0]))
        zip_count.append(i[1])
        if i[1] > max:
            max = i[1]
            highest_zip = str(i[0])

    plot_viol = fig.add_subplot(121)
    plot_viol.title.set_text('Violations Data')
    plot_viol.bar(codes, counts)

    plot_viol.set_xlabel("Violation Code")
    plot_viol.set_ylabel("Number of Occurrences per Code")

    plot_viol.tick_params(axis='x', labelrotation=45)

    plot_corr = fig.add_subplot(122)
    plot_corr.title.set_text('Violations per Zip Code')
    plot_corr.scatter(zips_, zip_count)

    plot_corr.set_xlabel("Zip Code")
    plot_corr.set_ylabel("Number of Violations per Zip")

    plot_corr.tick_params(axis='x', labelrotation=45)
    
    fig.set_tight_layout(True)

    canvas = FigureCanvasTkAgg(fig, master=plotWindow)
    canvas.draw()

    canvas.get_tk_widget().pack(side='top')
    toolbar = NavigationToolbar2Tk(canvas, plotWindow)
    toolbar.update()

    canvas.get_tk_widget().pack()

    label_text = "Zip Code that has the highest \nnumber of violations:\n" + \
        highest_zip + "\nwith the number of violations being:\n" + str(max)
    Label(plotWindow, text=label_text, font=("Arial", 12)).pack(side='right')


if __name__ == "__main__":
    root = Tk()  # Create the GUI main window
    root.title("Python Prototype")

    f1 = Frame(root)  # Frame to contain load and show keys
    f1.pack(side='right')

    load = Button(f1, text="Load Data", font=("Arial", 14), command=load_data)
    load.pack(side='top')

    loadSaved = Button(f1, text="Load Saved Data", font=("Arial", 14), command=load_saved)
    loadSaved.pack(side='top')

    show = Button(f1, text="Show Data", font=("Arial", 14),
                  state=DISABLED, command=show_data)
    show.pack(side='top')

    f2 = Frame(root)  # Frame to contain the data plot keys
    f2.pack(side='left')

    #label for first graph output
    graph_seats_label = Label(
        f2, text="Plot Graph for Inspection Score Per Year \nfor each type of vendor's seating:", font=("Arial", 12))
    graph_seats_label.pack(side='top')
    
    #Button for first graph output
    graph_seats_btn = Button(f2, text="Plot", bg='black', fg='white', font=(
        "Arial", 14), state=DISABLED, command=plot_seats)
    graph_seats_btn.pack(side='top')
    
    #label for second graph output
    graph_zips_label = Label(
        f2, text="Plot Graph for Inspection Score Per Year \nfor each Zip-Code:", font=("Arial", 12))
    graph_zips_label.pack(side='top')
    
    #Button for second graph output
    graph_zips_btn = Button(f2, text="Plot", bg='black', fg='white', font=(
        "Arial", 14), state=DISABLED, command=plot_zips)
    graph_zips_btn.pack(side='top')

    #label for third graph output
    graph_viols_label = Label(
        f2, text="Plot Graph For Each Type of Violations:", font=("Arial", 12))
    graph_viols_label.pack(side='top')
    
    #Button for third graph output
    graph_viols_btn = Button(f2, text="Plot", bg='black', fg='white', font=(
        "Arial", 14), state=DISABLED, command=plot_violations)
    graph_viols_btn.pack(side='top')

    root.mainloop()