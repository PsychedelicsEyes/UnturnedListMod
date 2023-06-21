import os
import csv
from datetime import datetime
import time
import threading
import sys

def list_csv_files(directory):

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_file_name = f"file_list_{timestamp}.csv"

    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Name', 'ID', 'Type'])

        traverse_directories(directory, csvwriter)

def traverse_directories(directory, csvwriter):

    for file_name in os.listdir(directory):
        absolute_path = os.path.join(directory, file_name)
        
        if os.path.isfile(absolute_path):

            if file_name.endswith('.dat') and file_name not in ['English.dat', 'English(1).dat', 'Japanese.dat', 'Asset.dat', 'MasterBundle.dat']:

                with open(absolute_path, 'r', encoding='latin-1') as file:
                    lines = file.readlines()
                    item_id = ''
                    file_type = ''

                    for line in lines:
                        if line.startswith('ID'):
                            item_id = line.strip()
                        elif line.startswith('Type'):
                            file_type = line.strip()

                csvwriter.writerow([file_name[:-4], item_id.strip('ID'), file_type.strip('Type')])

        elif os.path.isdir(absolute_path):

            traverse_directories(absolute_path, csvwriter)

def display_loading_animation():
    animation = "|/-\\"
    idx = 0
    while loading_active:
        sys.stdout.write("Processing " + animation[idx % len(animation)] + "\r")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

try:
    specified_directory = input("Enter the directory path: ")
    loading_active = True
    loading = threading.Thread(target=display_loading_animation)
    loading.start()
    list_csv_files(specified_directory)
    loading_active = False
    loading.join()
    print("\nProcessing completed. The CSV file has been created.")
except KeyboardInterrupt:
    print("\nProcessing interrupted.")
