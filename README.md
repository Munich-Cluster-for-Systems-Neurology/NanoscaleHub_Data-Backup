# Backup_script
Download all files and place them in one folder.
Update path to txt files in script.
Update parameters of interest such as paths to back-up location, date range, file extensions to be backed up etc in text files.
Run script in environment with python version > 3.8.

If multithreaded version make sure "ThreadPoolExecutor(max_workers=64)" is set to an appropriate value (e.g. max available cores on your PC)
