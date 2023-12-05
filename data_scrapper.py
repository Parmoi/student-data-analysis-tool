# Copyright (c) 2023, Dyllanson So
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import pandas as pd
import sys
import xlsxwriter

"""
How the program works:
- First we create a new xlsx file called "aggregated_data.xlsx", with sheet "students"
- Loop through all csv files found in directory "raw_data"
    - Scrap the following data: Name, Class, Comm_1, Comm_2, Comm_3, Comm_4, Comm_5, Grade
    - The Comm are the committment stuff ("Consistently", "Usually")
    - Save the scrapped data into a list
- After looping through all the files, save it into the file called "aggregated_data.xlsx"

NOTE: Running the program will wipe "aggregated_data.xlsx", so save the data before running it again
"""

COMMITMENT_1 = "Applies themselves to their studies through the completion of classwork, homework and assessment."
COMMITMENT_2 = "Is attentive and participates in class."
COMMITMENT_3 = "Is cooperative and respectful towards teachers and peers."
COMMITMENT_4 = "Is well-prepared, punctual and brings equipment."
COMMITMENT_5 = "Collaborates effectively to meet individual and collective learning goals."

YEAR_7_TO_10 = 1
YEAR_11 = 2

final_table_columns = []
rows_to_remove = ["Minimum", "Maximum", "Standard Deviation", "Mean", "Median"]
some_directory = "raw_data"

data_list = []

def setup(year_group):
    # Set up file to hold scrapped data (if it doesn't exist already)
    if os.path.isfile("aggregated_data.xlsx"):
        workbook = xlsxwriter.Workbook("aggregated_data.xlsx")
        workbook.add_worksheet("students")
        workbook.close()
    
    # Set up file to hold found student stats (if it doesn't exist already)
    if os.path.isfile("student_stats.xlsx"):
        workbook = xlsxwriter.Workbook("student_stats.xlsx")
        workbook.add_worksheet("students")
        workbook.close()

    global final_table_columns
    if year_group == YEAR_7_TO_10:
        final_table_columns = ["Name", "Class", "Comm_1", "Comm_2", "Comm_3", "Comm_4", "Comm_5", "Yearly Grade"]
    elif year_group == YEAR_11:
        final_table_columns = ["Name", "Class", "Comm_1", "Comm_2", "Comm_3", "Comm_4", "Comm_5", "Grade"]

def find_students():
    """Function that takes in the HR list, and returns a list of students"""
    df = pd.read_csv("student_list.csv")
    df = df.loc[~df["Name"].isin(rows_to_remove)]
    print(df["Name"])
    # df = df.loc[df["Name"]]
    # print(df)

def loop_files(directory, year_group):
    # Loop through all files in raw_data and grab their data
    for filename in os.listdir(directory):
        global data_list
        f = os.path.join(directory, filename)
        is_glo = "glo" in f.lower()
        # checking if it is a file
        if os.path.isfile(f) and f.endswith(".csv") and is_glo == False:
            # Opens the csv file
            df = pd.read_csv(f, encoding="utf-8", header=1) # header=1 just means we don't need need to read the first row
            # Removes uneeded rows, and any excluded students
            df = df.loc[~df["Name"].isin(rows_to_remove)]

            # (Specific to Maths) rename "Yearly Course Grade" to "Yearly Grade"
            try:
                df = df.rename(columns={"Yearly Course Grade": "Yearly Grade"})
            except:
                pass
            
            comm_list = [COMMITMENT_1, COMMITMENT_2, COMMITMENT_3, 
                         COMMITMENT_4, COMMITMENT_5]
            
            # If we have duplicate tables, remove the first one
            # Also renames our columns to nicer names
            if (COMMITMENT_1 + ".1") in df.columns:
                df = df.drop([COMMITMENT_1, COMMITMENT_2, COMMITMENT_3, 
                              COMMITMENT_4, COMMITMENT_5], axis=1)
                for idx, comm in enumerate(comm_list):
                    df = df.rename(columns={comm + ".1": f"Comm_{idx + 1}"})
            else:
                for idx, comm in enumerate(comm_list):
                    df = df.rename(columns={comm: f"Comm_{idx + 1}"})

            if year_group == 1:
                df = df.loc[df["Yearly Grade"] != "(Excluded)"] # Removes entries that either left the school or no longer attend that class
                df = df.loc[~df["Yearly Grade"].isna()] # Removes entries with no final grade (possibly joined late)
                df = df.loc[df["Comm_1"] != "(Excluded)"] # Remove entries where committment is excluded
                df = df.loc[~df["Comm_1"].isna()] # Remove entries where committment is empty
            elif year_group == 2:
                df = df.loc[df["Grade"] != "(Excluded)"] # Removes entries that either left the school or no longer attend that class
                df = df.loc[~df["Grade"].isna()] # Removes entries with no final grade (possibly joined late)
                df = df.loc[df["Comm_1"] != "(Excluded)"] # Remove entries where committment is excluded
                df = df.loc[~df["Comm_1"].isna()] # Remove entries where committment is empty

            # Only take columns that we want
            df = df[final_table_columns]

            # Add the student information into the data_list
            data_list += df.values.tolist()
        elif is_glo == True:
            df = pd.read_csv(f, encoding="utf-8", header=1) 
            df = df.loc[~df["Name"].isin(rows_to_remove)]

            df = df.rename(columns={"Applies themselves to their studies through the completion of coursework.": "Comm_1",
                                    "Is attentive and participates in class.": "Comm_2",
                                    "Is cooperative and respectful towards teachers and peers.": "Comm_3",
                                    "Is well-prepared, punctual and brings equipment.": "Comm_4",
                                    "Collaborates effectively to meet individual and collective learning goals.": "Comm_5"})
            # print(df)
            df = df[["Name", "Class", "Comm_1", "Comm_2", "Comm_3", "Comm_4", "Comm_5"]]

            data_list += df.values.tolist()

    # After going through all the files, save the data into the aggregated_data.xlsx file
    final_df = pd.DataFrame(data_list, columns=final_table_columns)
    with pd.ExcelWriter("aggregated_data.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
        final_df.to_excel(excel_writer=writer, sheet_name="students", header=True, index=False)

if __name__ == '__main__':
    args = sys.argv
    year_group = int(args[1])
    setup(year_group)
    loop_files(some_directory, year_group)


# # If aggregated_data.xlsx exists, count the rows. If not, set rows = 0
# global start_row
# if os.path.isfile("aggregated_data.xlsx"):
#     count_df = pd.read_excel("aggregated_data.xlsx")
#     start_row = len(count_df) + 2 # Accounts for row for column names, and that we don't want to override the last result
#     print(start_row)