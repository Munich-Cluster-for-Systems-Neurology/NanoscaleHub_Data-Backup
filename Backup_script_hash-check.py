import os
import re
import shutil
from datetime import datetime
import hashlib

# Configuration files
ext_file = 'file_extensions.txt'
wg_file = 'working_groups.txt'
surname_file = 'surnames_to_wg.txt'
path_file = 'paths.txt'
date_range_file = 'date_range.txt'

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

def file_md5(file_path):
    """ Computes MD5 hash of a file """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

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
                        destination_dir = os.path.join(backup_root, wg, surname, ms_folder)
                        os.makedirs(destination_dir, exist_ok=True)
                        destination_file = os.path.join(destination_dir, file)

                        if not os.path.exists(destination_file) or file_md5(file_path) != file_md5(destination_file):
                            shutil.copy2(file_path, destination_file)
                        else:
                            print(f"Skipping duplicate file: {file}")

backup_files(source_network_drive, backup_root)
