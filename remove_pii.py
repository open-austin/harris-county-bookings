import csv
import os

def make_new_file(dirpath, filename):
    """This function takes a CSV of Harris County arrest records, removes
    the columns containing the defendant's address, and makes a new file
    in a subdirectory of the folder where the original file was found."""

    input_filename = os.path.join(dirpath,filename)

    # files with address columns removed go in a new subdirectory
    output_filename = os.path.join(dirpath,"new",filename) 
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with open(input_filename, "r", errors="ignore") as file_in:
        with open(output_filename, "w") as file_out:
            writer = csv.writer(file_out)
            for row in csv.reader((line.replace('\0','') for line in file_in), delimiter=","):
                writer.writerow(row[:4] + row[9:]) # omitting most address columns

for dirpath, dirs, files in os.walk("./data/"):
    for filename in files:
        make_new_file(dirpath, filename)
