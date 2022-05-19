from email import message
from logging import root
import tkinter as tk  
import tkinter.ttk as ttk
from typing_extensions import IntVar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
from tkinter import filedialog
import pandas as pd
import os
import numpy as np


# main class for global variables
class mainGuiForCustomer(tk.frame):

    airports_csv = None
    airports_frequencies_csv = None
    runways_csv = None

    #getting the path for current directory
    path_current_directory = os.getcwd()

    ## store backup data 

    path1 = f"{current_dir}\\airpors_json.json"
    path2 = f"{current_dir}\\airorts_frequencies_json.json"
    path3 = f"{current_dir}\\runways_json.json"
    paths = [path1, path2, path3]

    # Storage place for the the clean data
    backup_data_df = []
    load_clicked = False

    def load_csv_files(self):
        #Storing the csv files in a list
        csv_list = []
        csv_paths = filedialog.askopenfilenames(title = "Choose csv files", filetypes=[("CSV files", ".csv")])


        # make sure only 3 csv files are chosen
        if len(csv_paths) == 3:
            for csv_file in csv_paths:
                csv_list.append(csv_file)
        elif not csv_paths:
            pass
        else:
            tk.messagebox.showwarning("Warning", "You have to choose only three csv files!")

    # Reading the csv files
    dfs = [pd.read_csv(path) for path in csv_list]

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
            
    
    # Disable the internal Chaining error
    pd.set_option('chained_assignment', None)

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

    # Retrieving the list of files that have corrct column names
    loaded_files = []

    #Checking the column names to ensure that the right files are uploaded
    for i in range(0, 3):
        for j in range(0,3):
            try:
                if set(all_column_headers[i].issubset(dfs_copy[j].columns):
                    loaded_files.append(dfs_copy[j])
            except IndexError:
                pass

    try:
        if len(loaded_files) == 3:
            tk.messagebox.showinfo("Info", "CSV files are being uploaded. Please wait...")
            for i in range (0, 3):
                if set(airports_column_header).issubset(loaded_files[i].columns):
                    loaded_files[i] = loaded_files[i][lambda x: x["PROGRAM STATUS"] == "ACTIVE"]
                    loaded_files[i]["ACTIVITY DATE"] = pd.to_datetime(loaded_files[i]["ACTIVITY DATE"]).astype(str)
                    self.np.extract_airport_type_(loaded_files[i])
                    self.airports_csv = loaded_files[i]

                elif set(airports_frequencies_column_header).issubset(loaded_files[i].columns):
                    self.np.extract_airports_frequienceies_frequency_mhz(loaded_files[i])
                    self.airports_frequencies_csv = loaded_files[i]

                elif set(runways_column_header).issubset(loaded_files[i].columns):
                    self.runways_csv = loaded_files[i]


                self.clean_data()
                tk.messagebox.showinfo("Info", "Data is successfully loaded and cleaned.")
                self.load_clicked = True
            elif not loaded_files:
                pass
            else:
                tk.messagebox.showwarning("warning", "Please make sure that you upload the right CSV files!")
            except:
                pass

        def save_data(self):
            # Confirming or denying a user action
            message = tk.message.box.askquestion("Save", "Would you like to create a backup?")
            if message =="yes":
                #Checking if all the files are uploaded
                if self.airports_csv is None and self.airports_frequencies_csv is not None and self.runways_csv is not None:
                    tk.messagebox.showinfo("info", "Saving process Started.")



                    # saving files to Json
                    Runways_csv_file = r'/Users/timothy/Downloads/AP Data set 21-22 2/runways.csv'
                    Runways_df = pd.read_csv(Runways_csv_file)
                    Runways_json_output = r'/Users/timothy/Downloads/AP Data set 21-22 2/runways242.json'
                    Runways_output = runways_df.to_json(json_output, indent = 4, orient= 'records')
                     
                    Frequencie_csv_file = r'/Users/timothy/Downloads/AP Data set 21-22 2/airport-frequencies.csv'
                    Frequencies_df = pd.read_csv(csv_file)
                    Frequencies_json_output = r'/Users/timothy/Downloads/AP Data set 21-22 2/airport-frequencies.json'
                    Frequencies_output = Frequencies_df.to_json(json_output, indent = 1, orient= 'records') 

                    Airports_csv_file = r'/Users/timothy/Downloads/AP Data set 21-22 2/airports.csv'
                    Airports_df = pd.read_csv(Airports_csv_file)
                    Airports_json_output = r'/Users/timothy/Downloads/AP Data set 21-22 2/runways242.json'
                    Airports_output = Airports_df.to_json(json_output, indent = 4, orient= 'records')

                    # Checking if the load button is clicked
                    self.load_clicked = False
                else:
                    tk.messagebox.showwarning("Warning", "Backup won't be created if you don't upload all three CSV files.")

        def clean_data(self):
            if Airports_csv_file is not None and Airports_frequencies_csv is not None and Runways_csv is not None:
                Airports_csv_file.dropna(inplace = True)
                Frequencies_csv_file.dropna(inplace = True)
                Runways_csv_file.dropna(inplace = True)

                airport_columns = ["OWNER NAME", "FACILITY NAME", "PROGRAM NAME", "FACILITY ADDRESS", "FACILITY CITY"]
                runways_columns = airport_columns + ["OWNER ADDRESS", "OWNER CITY"]

                # Replace the erroneous values
                self.Airports_csv_file[airport_columns] = self.Airports_csv_file[airport_columns].apply(lambda x: x.str.replace("&.+;", " ", regex = True))
                self.Airports_csv_file[airport_columns] = self.airports_csv[airport_columns].apply(lambda x: x.str.replace(";S", "'S"))
                self.Runways_csv_file[runways_columns] = self.Runways_csv[runways_columns].apply(lambda x: x.str.replace("&.+;", " ", regex = True))
                self.Runways_csv_file[runways_columns] = self.Runways_csv[runways_columns].apply(lambda x: x.str.replace(";S", "'S"))
 
                # delete duplicates
                airports_duplicates = self.airports_csv[self.airports_csv.duplicated()]
                airports_frequencies_duplicates = self.airports_frequencies_csv[self.airports_frequencies_csv.duplicated()]
                runways_duplicates = self.runways_csv[self.runways_csv.duplicated()]

              # make a df list
                df_list = [self.airports_csv, self.airports_frequencies_csv, self.runways_csv]
                duplicate_list = [airports_duplicates, airports_frequencies_duplicates, runways_duplicates]

            # Dropping the duplicates if exists
                for i in range(0, 3):
                    if len(duplicate_list[i]):
                        df_list[i].drop_duplicates(inplace = True)
        else:
            tk.messagebox.showwarning("Warning", "Cleaning cannot be done if you don't upload all three CSV files!")

    def load_backup(self):
        is_path_exists = False
        if all(os.pth.isfile(each_path) for each_path in self.paths):
            is_path_exists = True

        if is_pathexists:
            tk.messagebox.showinfo ("info", "BAckup is being loaded. Please wait...")
            for path in self.paths:
                json_data = pd.read_json(path, orient = "records")
                self.backup_data_df.append(json_data)
            tk.messagebox.showinfo("Infor", "Backup is successfully loaded. Now you can load graphs")
        else: 
            tk.messagebox.showwarning("Warning", "Backup file was not found")

    def compute_average_frequencies(self):
        # Getting the inspections data frame
        airports_df = self.backup_data_df[0]

        
        ### need to find the average of the required spec
        ### Calculating the mean 
        output1 = airports_df.groupby("type")["frequencies"].mean
        type_code = output1["type"]
        mean_score_for_type_code = output1["MEAN"]

        #Calculate the mode
        output2 = airports_df.groupby("type")["frequencies"].agg(lambda x: pd.Series.mode(x)[0]).reset_index()
        mode_score_for_type_code = output2["mode"]

        #Calculate the median 
        output3 = airports_df.groupby("type")["frequencies"].median().reset_index()
        median_score_for_type_code = output3["SCORE"]

        return average(type_code, mean_score_for_type_code, mode_score_for_type_code, median_score_for_type_code)

        compute_airport_frequencies(self):
        #Getting the airports data frame
        airports_df = self.backup_data_df[0]



        ##maybe a 2nd way to find averges of the size of the airports

        ######### Calculating the mean of the scores grouped by the pe description
        output1 = airports_df.groupby("PE DESCRIPTION")["SCORE"].mean().round(2).round(2).reset_index()
        seating_types = output1["PE DESCRIPTION"]
        mean_score_for_seating_type = output1["SCORE"]
        
        # Calculating the mode of the scores grouped by the pe description
        output2 = inspections_df.groupby("PE DESCRIPTION")["SCORE"].agg(lambda x: pd.Series.mode(x)[0]).reset_index()
        mode_score_for_seating_type = output2["SCORE"]
        
        # Calculating the median of the scores grouped by the pe description
        output3 = inspections_df.groupby("PE DESCRIPTION")["SCORE"].median().reset_index()
        median_score_for_seating_type = output3["SCORE"]
        
        return zip(seating_types, mean_score_for_seating_type, mode_score_for_seating_type, median_score_for_seating_type)

    def extract_vendor_seating_numbers(self, dataframe):
            # Extracting the vendor seating numbers using regex
        seating_numbers = dataframe["PE DESCRIPTION"].str.extract("(\(.*?\))")
        # Removing the whitespaces after the extraction
        dataframe["PE DESCRIPTION"] = dataframe["PE DESCRIPTION"].str.replace("\(.*?\)\ *", "", regex = True)
        # Inserting the new column into the data
        dataframe.insert(10, "VENDOR SEATING NUMBERS", seating_numbers)

        
        
        #### gui
    def __init__(self, root):
        self.root = root
        self.create_interface()
        self.create_tree()
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

        ## Setting the interface configurations
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnfigure(0, weight=1)

    def create_interface(self):
        self.root.title("Format Translator")
        self.root.geometry("680x400")

        #Creating the frame widget
        main_frame = tk.Frame(self.root)
        main_frame.grid(row = 1, rowspan = 3, padx = 40)

       # Adding the labels and buttons
        data_set_label = tk.Label(main_frame, text = "Initial Data Set (CSVs)")
        data_set_label.grid(row = 0, column = 1, pady = 10)
        load_data_button = tk.Button(main_frame, text = "Load CSV files", command = self.load_csv_files)
        load_data_button.grid(row = 1, column = 1, sticky = "EW")
        
        backup_label = tk.Label(main_frame, text = "Backup Operations")
        backup_label.grid(row = 0, column = 2)
        backup_button = tk.Button(main_frame, text = "Create backup", command = self.save_data)
        backup_button.grid(row = 1, column = 2, padx = 30, ipadx = 15)
        load_backup_data = tk.Button(main_frame, text = "Load backup", command = self.load_backup)
        load_backup_data.grid(row = 2, column = 2, pady = 10, padx = 30, ipadx = 20)
        
        self.var = tk.IntVar()
        self.var2 = tk.IntVar()
        stats_label = tk.Label(main_frame, text = "Statistics Operations")
        stats_label.grid(row = 0, column = 3)
        
        zip_code_rb = tk.Radiobutton(main_frame, text = "For each zip code", variable = self.var, value = 1, \
                                     command = self.remove_tree_data)
        
        zip_code_rb.grid(row = 1, column = 3, sticky = "W")
        
        seating_type_rb = tk.Radiobutton(main_frame, text = "For each seating type", variable = self.var, value = 2, \
                                         command = self.remove_tree_data)
        
        seating_type_rb.grid(row = 2, column = 3, sticky = "W")
        compute_stats_button = tk.Button(main_frame, text = "Compute statistics", command = self.initialize_tree)
        compute_stats_button.grid(row = 3, column = 3, ipadx = 2, sticky = "W", padx = 5)
        
        visual_label = tk.Label(main_frame, text = "Visualization")
        visual_label.grid(row = 0, column = 4)
        bar_graph = tk.Radiobutton(main_frame, text = "Bar graph", variable = self.var2, value = 1)
        bar_graph.grid(row = 1, column = 4, sticky = "W", padx = 30)       
        scatter_plot = tk.Radiobutton(main_frame, text = "Scatter plot", variable = self.var2, value = 2)
        scatter_plot.grid(row = 2, column = 4, sticky = "W", padx = 30)
        graph_button = tk.Button(main_frame, text = "Generate graph", command = self.generate_graphs)
        graph_button.grid(row = 3, column = 4, padx = 35, ipadx = 10)
        
    def create_tree(self):
        #Setting the frame for the tree
        tree_frame= tk.Frame(self.root)
        tree_frame.grid(row = 4, columnspan = 4, column = 0, pady = 15)
        
        #Setting the columns
        self.tree = ttk.Treeview(tree_frame, columns=("Seating Type", "Zip Code", "Mean", "Mode", "Median"))
        self.tree.column("#0", minwidth = 0, width = 0, stretch = False)
        self.tree.column("Seating Type", anchor = "w", stretch = False, minwidth = 100, width = 100)
        self.tree.column("Zip Code", anchor = "center", stretch = False, width = 100)
        self.tree.column("Mean", anchor = "center", stretch = False, minwidth = 100, width = 100)
        self.tree.column("Mode", anchor = "center", stretch = False, minwidth = 100, width = 100)
        self.tree.column("Median", anchor = "center", stretch = False, minwidth = 100, width = 100)
        
        #Setting the headings
        self.tree.heading('#1', text="Seating Type")
        self.tree.heading('#2', text="Zip Code")
        self.tree.heading('#3', text="Mean")
        self.tree.heading('#4', text="Mode")
        self.tree.heading('#5', text="Median")
        self.tree.grid(row = 4, column = 0)
        
        #Setting the scrollbar
        sb = ttk.Scrollbar(tree_frame, orient = "vertical", command = self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.grid(row = 4, column = 3, sticky='nse')
        
    def initialize_tree(self): 
        try:
            is_button_selected = self.var.get()
            
            # Checking if the radio button is clicked
            if(is_button_selected == 1):
                for zip_codes, mean, mode, median in self.compute_statistics_for_zip_code():
                    self.tree.insert("", "end", values = ("", zip_codes, mean, mode, median))
            elif(is_button_selected == 2):
                for seating_types, mean, mode, median in self.compute_statistics_for_seating_types():
                    self.tree.insert("", "end", values = (seating_types, "", mean, mode, median))
            else:
                tk.messagebox.showwarning("Warning", "No choice made!")
        except:
            tk.messagebox.showwarning("Warning", "You need to load the backup file.")

    def remove_tree_data(self):
        # Getting all the data and removing them from the tree
        children = self.tree.get_children()
        if children != "()":
            for child in children:
                self.tree.delete(child)
 
    def generate_graphs(self):
        try:
            # Retrieving the columns from the respective dataframes
            violations_df = self.backup_data_df[2][["SERIAL NUMBER", "VIOLATION DESCRIPTION"]]
            inspections_df = self.backup_data_df[0][["SERIAL NUMBER", "ZIP CODES"]]
            
            # Merging the violations and inspections files
            merged = violations_df.merge(inspections_df, on = ["SERIAL NUMBER"], how = "left")
            
            # Creating the Figure widget
            fig = Figure(figsize=(10,4), dpi=70)
            axes = fig.add_subplot(111)
         
            # Getting the selected radio button value
            is_button_selected = self.var2.get()
            
            if(is_button_selected == 1):
                # Setting the labels and title
                axes.set_xlabel("Number of Establishments")
                axes.set_ylabel("Types of Violations")
                axes.set_title("10 Most Committed Violations")
                
                # Getting the number of zip codes grouped by the violation description
                number_of_vendors = merged.groupby(["VIOLATION DESCRIPTION"])["ZIP CODES"].count().reset_index()
                
                # Sorting the top 10 values
                sorted_vendors = number_of_vendors.sort_values("ZIP CODES", ascending = False).head(10)
                sorted_vendors.rename(columns = {"ZIP CODES" : "NUMBER OF RESTAURANTS"}, inplace = True)
            
                # Naming the axes
                x_axis = sorted_vendors["VIOLATION DESCRIPTION"]
                y_axis = sorted_vendors["NUMBER OF RESTAURANTS"]
                
                # Passing the axes to the barh function to create the bar chart
                axes.barh(x_axis, y_axis)
                
                # Adjusting the figure style
                fig.set_tight_layout(True)
                style.use("ggplot")

                # Creating the subwindow for the bar chart
                chart_window = tk.Toplevel(self.root)
                chart_window.title("Bar chart")
            
                # Drawing the bar chart onto the Canvas widget
                canvas = FigureCanvasTkAgg(fig, master = chart_window)
                fig.canvas.draw()
                canvas.get_tk_widget().pack()
            
            elif(is_button_selected == 2):
                #Setting the labels and title
                axes.set_xlabel("Zip Codes")
                axes.set_ylabel("Number of Violations")
                axes.set_title("Correlation")
                
                # Getting the number of violations grouped by the zip codes
                number_of_violations = merged.groupby(["ZIP CODES"])["VIOLATION DESCRIPTION"].count().reset_index()
                
                # Naming the axes
                x_axis = number_of_violations["ZIP CODES"]
                y_axis = number_of_violations["VIOLATION DESCRIPTION"] 
                
                # Calculating the correlation
                corr = x_axis.corr(y_axis)
                axes.annotate("r=%.2f" %corr, (0.6, 0.8), xycoords='axes fraction', ha='center', va='center')

                # Creating the scatter plot
                axes.scatter(x_axis, y_axis)
                axes.plot(np.unique(x_axis), np.poly1d(np.polyfit(x_axis, y_axis, 1))(np.unique(x_axis)))
                
                # Adjusting the figure style
                fig.set_tight_layout(True)
                style.use("ggplot")
                
                # Creating the subwindow for the scatter plot
                chart_window = tk.Toplevel(self.root)
                chart_window.title("Scatter plot")
            
                # Drawing the bar chart onto the Canvas widget
                canvas = FigureCanvasTkAgg(fig, master = chart_window)
                fig.canvas.draw()
                canvas.get_tk_widget().pack()
            else:
                tk.messagebox.showwarning("Warning", "No choice made!")
        except:
            tk.messagebox.showwarning("Warning", "You need to load the backup file.")

    def close_application(self):
        # Calling the saving funtion when a user closes the program after he/she clicked the load button
        if self.load_clicked == True:
            self.save_data()
            self.root.destroy()
        else:
            self.root.destroy()

my_app = GUIApplication(tk.Tk())
my_app.root.mainloop()