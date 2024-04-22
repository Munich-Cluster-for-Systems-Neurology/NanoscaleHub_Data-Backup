import os
import re
import shutil
from datetime import datetime

# Configuration files
ext_file = r'E:\Backup_script\file_extensions.txt'
wg_file = r'E:\Backup_script\working_groups.txt'
surname_file = r'E:\Backup_script\surnames_to_wg.txt'
path_file = r'E:\Backup_script\paths.txt'
date_range_file = r'E:\Backup_script\date_range.txt'

# Load file extensions to backup
with open(ext_file, 'r') as file:
    extensions = [line.strip() for line in file if line.strip()]

# Load working groups
with open(wg_file, 'r') as file:
    working_groups = [line.strip() for line in file if line.strip()]

# Load surname to working group mapping
surname_to_wg = {}
with open(surname_file, 'r') as file:
    for line in file:
        surname, wg = line.strip().split(',')
        surname_to_wg[surname] = wg

# Load paths for source and backup
with open(path_file, 'r') as file:
    paths = {}
    for line in file:
        key, value = line.strip().split('=')
        paths[key.strip()] = value.strip()

source_network_drive = paths['source_path']
backup_root = paths['backup_path']

# Load date range for file selection
with open(date_range_file, 'r') as file:
    date_config = {}
    for line in file:
        key, value = line.strip().split('=')
        date_config[key.strip()] = datetime.strptime(value.strip(), '%Y-%m-%d')

start_date = date_config['start_date']
end_date = date_config['end_date']

def get_wg_and_ms_folder(filename):
    for surname, wg in surname_to_wg.items():
        if surname in filename:
            ms_match = re.search(r'MS(\d{3})', filename)
            ms_folder = f"MS{ms_match.group(1)}" if ms_match else "MS_number_missing"
            return wg, surname, ms_folder
    return None, None, None

def backup_files(source_dir, backup_root):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file.endswith(ext) for ext in extensions):
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if start_date <= file_mtime <= end_date:
                    wg, surname, ms_folder = get_wg_and_ms_folder(file)
                    if wg and surname and ms_folder:
                        print(f"Backing up {file} to {wg}/{surname}/{ms_folder}")  # Debugging output
                        destination_dir = os.path.join(backup_root, wg, surname, ms_folder)
                        os.makedirs(destination_dir, exist_ok=True)
                        destination_file = os.path.join(destination_dir, file)
                        # Handling file name conflicts
                        counter = 1
                        while os.path.exists(destination_file):
                            name, ext = os.path.splitext(file)
                            destination_file = os.path.join(destination_dir, f"{name}_{counter}{ext}")
                            counter += 1
                        shutil.copy2(file_path, destination_file)
                    else:
                        print(f"No matching WG or surname for {file}")  # Debugging output
                else:
                    print(f"File {file} outside date range")  # Debugging output
            else:
                print(f"Skipping {file}, does not match extensions")  # Debugging output

backup_files(source_network_drive, backup_root)
