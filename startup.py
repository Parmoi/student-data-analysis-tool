from enum import Enum

"""
startup.py

Run this function with python3.10 startup.py

Upon running, you will be greeted with some option settings.
- Year Group (7, 8, 9, 10, 11)
- Report Type (Half Yearly / Yearly)

NOTE: This program assumes that the files has the following column names (although it may have more):
- For the Half Yearly Report:
    - ['Name','Class',<Commitment_1>,<Commitmemnt_2>,<Commitment_3>,<Commitment_4>,<Commitment_5>,'Half Yearly Grade']
- For the Yearly Report:
    - ['Name','Class',<Commitment_1>,<Commitmemnt_2>,<Commitment_3>,<Commitment_4>,<Commitment_5>,'Yearly Grade']

The program will quit out if the column names are not correct.
"""

class Report_Type(Enum):
    HALF_YEARLY = 0
    YEARLY = 1

def main():
    # Declaring a bunch of variables that we will use as settings for our program
    year = 0
    report_type = 0

    try:    # This is a try statement for programming, but for the real thing I'd like to have a drop down menu for the options.
        year = int(input("Please enter the Year group (7, 8, 9, 10 , 11): "))

        if year < 7 or year > 11:
            raise ValueError
        
        report_type = int(input("Please enter the number corresponding to the report type (Half Yearly = 0, Yearly = 1): "))
        
        if report_type not in [0,1]:
            raise ValueError

    except ValueError:
        print("Invalid input. Please enter a valid integer.")
    
    # print("Year: {}, Report Type: {}".format(year, Report_Type(report_type).name))



if __name__ == "__main__":
    main()