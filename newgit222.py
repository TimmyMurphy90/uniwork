from pyexpat.errors import codes
import re
from statistics import median
import pandas as pd
import math
from collections import Counter
import json

# GUI imports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk  

# matplotlib for graph drawing
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib import style
import numpy as np
import os

# GLOBAL VARIABLES (FOR INSPECTIONS & VIOLATIONS)
airports = None
airports_frequencies = None
runways = None

# Flag to know if JSON file is imported or not
isJSON = False

# Getting a path of the current directory
current_dir = os.getcwd()
    
    # Output path of the backup
path1 = f"{current_dir}\\airpors_json.json"
path2 = f"{current_dir}\\airorts_frequencies_json.json"
path3 = f"{current_dir}\\runways_json.json"
paths = [path1, path2, path3]

    # Storing the cleaned and translated data for further processing
backup_data_df = []
load_clicked = False
    
def load_csv_files(self):
    # Storing the csv files in a list
    csv_files_list = []
    csv_files_paths = filedialog.askopenfilenames(title = "Choose the three csv files", filetypes=[("CSV files", ".csv")])
                
    # Allowing only three files
    if len(csv_files_paths) == 3:
        for csv_file in csv_files_paths:
            csv_files_list.append(csv_file)
    elif not csv_files_paths:
        pass
    else:
        tk.messagebox.showwarning("Warning", "You have to choose only three csv files!")

        # Reading the csv files
        dfs = [pd.read_csv(path) for path in csv_files_list]
    
        # Copying the dataframe to another object to not modify the original file
        dfs_copy = dfs.copy()

        # Replace the white spaces in the column names before loading the files
        for i in range(0, 3):
            try:
                dfs_copy[i].columns = dfs_copy[i].columns.str.strip()
                dfs_copy[i].columns = dfs_copy[i].columns.str.replace(' +', ' ', regex = True)
                dfs_copy[i].columns = dfs_copy[i].columns.str.upper()
            except IndexError:
                pass
        
        # Disabling the internal chaining error
        pd.set_option('chained_assignment',None)
        
        airports_column_header = ['id', 'ident', 'type', 'name',
       'latitude_deg', 'Longitude_deg', 'elevation_ft', 'continent',
       'iso_country', 'iso_region', 'municipality',
       'scheduled_service', 'gps_code', 'iata_code', 'local_code',
       'home_link', 'wikipedia_link', 'keywords']
        
        airports_frequencies_column_header = ['id', 'airport_ref', 'airport_ident', 'type',
       'description', 'frequency_mhz']
        
        runways_column_header = ['id', 'airport_ref', 'airport_ident',
       'length_ft', 'width_ft' 'surface', 'lighted',
       'closed', 'le_ident', 'le_longitude_deg', 'le_elevation_ft',
       'le_heading_degT','le_displaced_threshold_ft','he_ident','he_latitude_deg','he_longitude_deg','he_elevation_ft',
       'he_heading_degT','he_displaced_threshold_ft']
        
        # Storing pre-defined column headers
        all_column_headers = [airports_column_header, airports_frequencies_column_header, runways_column_header]
        
        # Retrieving the list of files that have correct column names
        loaded_files = []
        
        #Checking the column names to ensure that the right files are uploaded         
        for i in range(0, 3):
            for j in range(0, 3):
                try:
                    if set(all_column_headers[i]).issubset(dfs_copy[j].columns):
                        loaded_files.append(dfs_copy[j])
                except IndexError:
                    pass
                
        try:
            if len(loaded_files) == 3:
                tk.messagebox.showinfo("Info", "CSV files are being uploaded. Please wait...")
                for i in range(0, 3):
                    if set(airports_column_header).issubset(loaded_files[i].columns):
                        loaded_files[i] = loaded_files[i][lambda x: x["type"] == "closed"]
                        self.extract_airport_size_(loaded_files[i])
                        self.airports_csv = loaded_files[i]
                        
                    elif set(airports_frequencies_column_header).issubset(loaded_files[i].columns):
                        self.extract_frequencies_numbers(loaded_files[i])
                        self.airport_frequencies_csv = loaded_files[i]
                        
                    elif set(runways_column_header).issubset(loaded_files[i].columns):
                        self.runways_csv = loaded_files[i]
            
                self.clean_data()
                tk.messagebox.showinfo("Info", "Data is successfully loaded and cleaned.")
                self.load_clicked = True
            elif not loaded_files:
                pass
            else:
                tk.messagebox.showwarning("Warning", "Please make sure that you upload the right CSV files!")
        except:
            pass
           
    def save_data(self):
        # Confirming or denying a user action
        message = tk.messagebox.askquestion("Save","Would you like to create a backup?")
        if message == "yes":   
            # Checking if all the files are uploaded
            if self.airports_csv is not None and self.airports_frequencies_csv is not None and self.runways_csv is not None:
                tk.messagebox.showinfo("Info", "Saving process started. Please wait...")
                
                # Saving files to JSON
                self.airports_csv.to_json(self.path1, indent = 4, orient = "records")
                self.airports_frequencies_csv(self.path2, indent = 4, orient = "records")
                self.runways_csv.to_json(self.path3, indent = 4, orient = "records")
                tk.messagebox.showinfo("Info", "Saving process finished.")
                
                # Checking if the load button is clicked
                self.load_clicked = False
            else:
                tk.messagebox.showwarning("Warning", "Backup won't be created if you don't upload all three CSV files.")
    

def get_airports():
    #Reads the airports.csv file via asking for the file name
    filename = filedialog.askopenfilename(
        initialdir="./", title="Select airport file", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    airports = pd.read_csv(filename)

    count = 0
    droplist = []
    for i in airports["type"]:
        if i == "closed":
            droplist.append(count)  # Remove inactive entries
        count += 1
    airports = airports.drop(droplist)

    return airports

    

def get_runways():
    #Reads the runways.csv file, asks for file name
    filename = filedialog.askopenfilename(
        initialdir="./", title="Select Runways File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    runways = pd.read_csv(filename)

    return runways

def get_airport_frequencies():
    #Reads the runways.csv file, asks for file name
    filename = filedialog.askopenfilename(
        initialdir="./", title="Select Airport frequencies File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    airports_frequencies = pd.read_csv(filename)

    return airports_frequencies



def get_airpor_size(airports):
    #gets the airport size in airports.csv
    airport_size = []
    if not isJSON:
        for item in airports["type"]:
            airport_size.append(re.findall(r'\((.*?)\)', item))
    else:
        airport_size = airports["type"].tolist()

    return airport_size


def airport_type(airports):
    # Manipulates the data

    size =airports["type"]
    countries = airports["iso_country"]

    sizes_ = []
    for size in size:
        if "small_airport" in size:
            sizes_.append("SMALL")
        elif "medium_airport" in size:
            sizes_.append("MEDIUM")
        elif "large_airport" in size:
            sizes_.append("LARGE")
        elif "heliport" in size:
            sizes_.append("HELIPCOPTER")
        else:
            sizes_.append("closed")

    countries_ = []
    for country in countries:
        countries_.append(country)

        data = {'Airport size': size, 'Country': countries_}

    unique_country = list(set(country))

    type_airport = ["SMALL", "MEDIUM", "LARGE", "HELICOPTER", "closed"]

    data_for_type = [] #A DataFrame that hold the data for each of the airport types
    for sizes_ in type_airport:
        for country in unique_country:
            data_for_type.append(data.loc[(data['Airport size'] == sizes_) & (data['Country'] == countries_)])

    final_type_data = []
    for data_ in data_for_type:
        if data_.empty:
            continue
        mean = data_.mean()
        mode = data_.mode()
        median = data_.median()
        mode_country = 0
        try:
            mode_country = mode["Country"][0]
        except IndexError:
            pass
        median_ = median[0]
        if math.isnan(median_):
            median_ = 0
        type_data = [data_["Airport size"].tolist()[0], data_["Country"]tolist()[0], mean[0], mode_country, median_]]]
        final_type_data.np.append(type_data)
    
    return final_type_data
        
            



def mhz_airport(airport_frequencies_csv):
#create a list of frequencies

    frequencies= []
    if not isJSON:
        for item in airport_frequencies_csv["frequency_mhz"]:
            frequencies.append(re.findall(r'\((.*?)\)', item))
    else:
        frequencies = airport_frequencies_csv["frequency_mhz"].tolist()

    return frequencies


def manipulate_mhz_frequency(airport_frequencies_csv):
    # Manipulates the data of the Inspection Score for each zip code per year

    mhz = airport_frequencies_csv["frequency_mhz"]
    airRef = airport_frequencies_csv["airport_ref"]
    description = airport_frequencies_csv["description"]

    desc = []
    for description_ in description:
        desc.append(description_)
    airRef_ = []
    for airport_ref in airRef:
        airRef_.append(airport_ref)
    freMhz = []
    for freq in mhz:
        freMhz.append(freq)
    d = {'airportReference': airRef_, 'Description': desc, 'freMhz': freq}
    data = pd.DataFrame(data=d)     # A DataFrame which holds the data for each frequency with a description of each airport

    unique_description = list(set(desc))
   
    unique_mhz = []

    for freq in mhz:
        if freq not in unique_mhz and not math.isnan(freq):
            unique_mhz.append(freq)

    data_for_mhz = []
    for freq in unique_mhz:
        for desc in unique_description:
            data_for_mhz.append(
                data.loc[(data['freMhz'] ==freMhz) & (data['Description'] == description_)])

    final_mhz_data = []
    for data_ in data_for_mhz:
        if data_.empty:
            continue
        mean = data_.mean()
        mode = data_.mode()
        median = data_.median()
        mode_description = 0
        try:
            mode_description = mode["Description"][0]
        except IndexError:
            pass
        median_ = median[0]
        if math.isnan(median_):
            median_ = 0
        mhz_data = [data_["Description"].tolist()[0], data_["freMhz"].tolist()[
            0], mean[0], mode_description, median_]

    return final_mhz_data


def get_runways_code(runways):
    codes = runways["airport_ref"].tolist()

    unique_codes = lest(set(codes))

    # get count of each code
    counts = Counter(codes)
    return unique_codes, counts

def get_correlation(airport, airport_frequency):
    id = airports["ident"].tolist()
    airport_identity = airport_frequency["airport_identity"].tolist()
    mhz = airport_frequency["frequency_mhz"]

    mhz_ = []

    id = counter(id)
    for ids in id:
        count = 0
        for s in airport_identity:
            if id == s and not math.isnan(mhz[count]):
                mhz_.append((mhz[count], ids[id]))
            count += 1
    return mhz_


def load_data():
    # loads the data into the program

    global Fre_mhz, Airport_size, isJSON

    isJSON = False

    fre_mhz = mhz_airport()
    Airport_size = airport_type()
    frames = [fre_mhz, Airport_size]
    show["state"] = NORMAL
    graph_mhz_btn["state"] = NORMAL
    graph_AIRPORT_TYPE_btn["state"] = NORMAL

def load_saved():

        global fre_mhz, Airport_size

        isJSON = True

        airportFile = filedialog.askopenfilename( initialdir="./", title="Import airport.json File", filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        airportFrequencyFile = filedialog.askopenfilename( initialdir="./", title="Import airportFrequency.json File", filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))        
        
        Airport_data = json.load(open(airportFile))
        frequencyData = json.load(open(airportFrequencyFile))

        fre_mhz = pd.DataFrame(frequencyData["data"])
        Airport_size = pd.DataFrame(Airport_data["data"])

        show["state"] = NORMAL
        graph_mhz_btn["state"] = NORMAL
        graph_AIRPORT_TYPE_btn["state"] = NORMAL

def show_data():

    global fre_mhz

    frequency = get_airport_frequencies(airports_frequencies)

    dataWindow = Toplevel(root)
    dataWindow.title("Show Data")

    verscrlbar = ttk.Scrollbar(dataWindow, orient="vertical")
    verscrlbar.pack(side='right', fill='y')
    horscrlbar = ttk.Scrollbar(dataWindow, orient="horizontal")

    save = Button(dataWindow, text="Save Data", font=(
        "Arial", 14), command=lambda: save_data(frequency))
    save.pack(side='bottom')

    saved = Label(dataWindow, text="Data Saved Successfully!",
                  font=("Arial", 12), fg='green')

    horscrlbar.pack(side='bottom', fill='x')

    treev = ttk.Treeview(dataWindow, selectmode='browse',
                         yscrollcommand=verscrlbar.set, xscrollcommand=horscrlbar.set)
    treev.pack(side='left', fill=BOTH)

    verscrlbar.configure(command=treev.yview)
    horscrlbar.configure(command=treev.xview)

    treev["columns"] = tuple(fre_mhz.columns)
    treev['show'] = 'headings'

    for column in tuple(fre_mhz.columns):
        treev.column(column, width=200, anchor='c')
        treev.heading(column, text=column)

    for index, row in fre_mhz.iterrows():
        row[5] = frequency[index]
        treev.insert("", 'end', text="L"+str(index), values=tuple(row))

    def save_data(frequency):
        data = fre_mhz
        data['type'] = frequency
        airData = data.to_json(orient='table', index=False)
        airfreData = airfreData.to_json(orient='table', index=False)
        parsedAir = json.loads(airData)
        parsedfreData= json.loads(airfreData)
        with open('air.json', 'w') as f:
            json.dump(parsedAir, f)
        with open('airfre.json' 'w') as f:
            json.dump(parsedAirfre, f)
        saved.pack(side='bottom', fill=BOTH, expand=True)

def plot_mhz():
    # Plots the first graph

    plotWindow = Toplevel(root)
    plotWindow.title(graph for mhz)

    btn_frame = Frame(plotWindow)
    btn_frame.pack(side='bottom')

    data = manipulate_data_mhz(frequency)

    #defining containers for plot data 
    mhz_data = []
    mean_data = []
    mode_data = []
    median_data = []

    for data_ in data:
        year = data_[0]
        if country not in unique_country
            unique_country.np.append(country)


#### needs doing
    unique_mhz.sort()
    for mhz in unique_mhz:
        Button(btn_frame, text=frequency, command=lambda frequency=mhz: update_graph(
            mhz)).pack(side='left')
        seats = []
        means = []
        modes = []
        medians = []
        for data_ in data:
            if mhz == data_[0]:
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
    plot_mean.bar(mhz_data[0], mean_data[0])
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
        index = unique_mhz.index(mhz)
        print(mhz)

        fig.clf()

        plot_mean = fig.add_subplot(131)
        plot_mean.title.set_text('Mean Data')
        plot_mean.bar(seat_data[index], mean_data[index])
        plot_mode  = fig.add_subplot(132)
        plot_mode.title.set_text('mode Data')
        plot_mode.bar(seat_data[index], mode_data[index])
        plot_median =fig.add_subplot(133)
        plot_median.title.set_text('Median Data')
        plot_median.bar(seat_data[index], median_data[index])

        canvas.draw()


def plot_zips():
    #

    plotWindow = Toplevel(root)
    plotWindow.title("Graph data for Zip code")


    btn_frame = Frame(plotWindow)
    btn_frame.pack(side='bottom')

    data = manipulate_type_data(airport_frequeincies)

    #Defining containers for plot data
    unique_data = []
    mhz_data = []
    mean_data = []
    mode_data = []

   

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


    

    


        

    

