# Copyright (c) 2023, Dyllanson So
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import pandas as pd
from data_scrapper import YEAR_7_TO_10, YEAR_11

"""
How the program works:
- First we load in the "aggregated_data.xlsx" file that we made from data scrapping
- Find all unique names within the data, and create a dataframe where only rows that have that name appear
- Loop through each name:
    - Find the "Consistently" and "Usually" counts
    - Find number of "A's" and "B's"
    - Find the number of subjects that student has taken
- All this data is then formatted and saved in "student_stats.xlsx"

NOTE: This program should be run AFTER data_scrapper.py
"""

stat_columns = ["Name", "Gender","Number of Subjects", "Max Consistencies", 
                "Consistently Count", "Usually Count", "A's", "B's", 
                "Consistently Percentage", "Usually Percentage", 
                "A's Percentage", "B's Percentage"]

def find_stats(year_group):
    grade_label = ""
    if year_group == YEAR_7_TO_10:
        grade_label = "Yearly Grade"
    elif year_group == YEAR_11:
        grade_label = "Grade"
    
    # Load in our data that we scrapped
    df = pd.read_excel("aggregated_data.xlsx")

    # Find the list of name (duplicates removed, alphabetically sorted)
    names = list(set(df["Name"].tolist()))
    names.sort()

    data_list = []

    # Find values for each name:
    for name in names:
        count_frame = df.loc[df["Name"] == name] # Limit frame to rows with just the current name
        consistent_count = 0
        usually_count = 0
        grade_a_count = 0
        grade_b_count = 0
        try:
            consistent_count += count_frame.groupby("Comm_1").size()["Consistently"]
            usually_count += count_frame.groupby("Comm_1").size()["Usually"]
        except:
            try:
                usually_count += count_frame.groupby("Comm_1").size()["Usually"]
            except:
                pass
            pass
        try:
            consistent_count += count_frame.groupby("Comm_2").size()["Consistently"]
            usually_count += count_frame.groupby("Comm_2").size()["Usually"]
        except:
            try:
                usually_count += count_frame.groupby("Comm_2").size()["Usually"]
            except:
                pass
            pass
        try:
            consistent_count += count_frame.groupby("Comm_3").size()["Consistently"]
            usually_count += count_frame.groupby("Comm_3").size()["Usually"]
        except:
            try:
                usually_count += count_frame.groupby("Comm_3").size()["Usually"]
            except:
                pass
            pass
        try:
            consistent_count += count_frame.groupby("Comm_4").size()["Consistently"]
            usually_count += count_frame.groupby("Comm_4").size()["Usually"]
        except:
            try:
                usually_count += count_frame.groupby("Comm_4").size()["Usually"]
            except:
                pass
            pass
        try:    
            consistent_count += count_frame.groupby("Comm_5").size()["Consistently"]
            usually_count += count_frame.groupby("Comm_5").size()["Usually"]
        except:
            try:
                usually_count += count_frame.groupby("Comm_5").size()["Usually"]
            except:
                pass
            pass
        try:
            grade_a_count += count_frame.groupby(grade_label).size()["A"]
            grade_b_count += count_frame.groupby(grade_label).size()["B"]
        except:
            try:
                grade_b_count += count_frame.groupby(grade_label).size()["B"]
            except:
                pass
            pass
        numb_of_subjects = count_frame.groupby("Name").size()[name]

        # Other random statistics that might be useful
        max_consistencies = numb_of_subjects * 5
        percent_consistencies = consistent_count / max_consistencies * 100
        percent_usually = usually_count / max_consistencies * 100
        percent_a = grade_a_count / numb_of_subjects * 100
        percent_b = grade_b_count / numb_of_subjects * 100

        # If year 7-10, find their gender
        gender = ""
        gender_frame = count_frame.iloc[0]
        class_code = gender_frame["Class"]
        code_end = class_code[-1]
        if code_end.isnumeric():
            gender = "M"
        elif code_end.isalpha():
            gender = "F"

        data_list.append([name, gender, numb_of_subjects, max_consistencies, 
                        consistent_count, usually_count,
                        grade_a_count, grade_b_count,
                        percent_consistencies, percent_usually,
                        percent_a, percent_b])

    # Now we want to save the data to the "student_stats.xlsx" sheet
    final_df = pd.DataFrame(data_list, columns=stat_columns)
    with pd.ExcelWriter("student_stats.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
        final_df.to_excel(excel_writer=writer, sheet_name="students", header=True, index=False)


if __name__ == '__main__':
    # command_line_args = sys.argv
    find_stats(YEAR_7_TO_10)