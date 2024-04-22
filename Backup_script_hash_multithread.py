import os
import re
import shutil
from datetime import datetime
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading

# Configuration files
ext_file = r'E:\Backup_script\file_extensions.txt'
wg_file = r'E:\Backup_script\working_groups.txt'
surname_file = r'E:\Backup_script\surnames_to_wg.txt'
path_file = r'E:\Backup_script\paths.txt'
date_range_file = r'E:\Backup_script\date_range.txt'

# Load configurations
with open(ext_file, 'r') as file:
    extensions = [line.strip() for line in file if line.strip()]

with open(wg_file, 'r') as file:
    working_groups = [line.strip() for line in file if line.strip()]

surname_to_wg = {}
with open(surname_file, 'r') as file:
    for line in file:
        surname, wg = line.strip().split(',')
        surname_to_wg[surname] = wg

with open(path_file, 'r') as file:
    paths = {key.strip(): value.strip() for key, value in (line.split('=') for line in file)}

with open(date_range_file, 'r') as file:
    date_config = {key.strip(): datetime.strptime(value.strip(), '%Y-%m-%d') for key, value in (line.split('=') for line in file)}

source_network_drive = paths['source_path']
backup_root = paths['backup_path']
start_date = date_config['start_date']
end_date = date_config['end_date']

def file_md5(file_path):
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

def copy_file(file_info):
    file_path, destination_dir = file_info
    file_name = os.path.basename(file_path)
    destination_file = os.path.join(destination_dir, file_name)

    os.makedirs(destination_dir, exist_ok=True)
    if not os.path.exists(destination_file) or file_md5(file_path) != file_md5(destination_file):
        shutil.copy2(file_path, destination_file)
        return f"Copied: {file_path}"
    else:
        return f"Skipped (Duplicate): {file_path}"

def file_finder(directory, extensions, start_date, end_date, queue):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if start_date <= file_mtime <= end_date:
                    wg, surname, ms_folder = get_wg_and_ms_folder(file)
                    if wg and surname and ms_folder:
                        destination_dir = os.path.join(backup_root, wg, surname, ms_folder)
                        queue.put((file_path, destination_dir))
    queue.put(None)  # Signal end of processing

def copy_worker(queue):
    while True:
        item = queue.get()
        if item is None:
            break  # End signal
        result = copy_file(item)
        print(result)

def main():
    file_queue = Queue(maxsize=50)  # Adjust size as needed for memory management
    finder_thread = threading.Thread(target=file_finder, args=(source_network_drive, extensions, start_date, end_date, file_queue))
    finder_thread.start()

    # Start multiple copy workers
    num_workers = 4  # Adjust number of workers as needed
    workers = []
    for _ in range(num_workers):
        worker = threading.Thread(target=copy_worker, args=(file_queue,))
        worker.start()
        workers.append(worker)

    # Wait for the finder to finish
    finder_thread.join()

    # Signal to workers to stop processing
    for _ in range(num_workers):
        file_queue.put(None)

    # Wait for all workers to finish
    for worker in workers:
        worker.join()

if __name__ == '__main__':
    main()
