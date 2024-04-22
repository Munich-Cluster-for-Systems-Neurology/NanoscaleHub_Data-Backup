# Backup_script
Download all files and place them in one folder.
Update path to txt files in script.
Update parameters of interest such as paths to back-up location, date range, file extensions to be backed up etc in text files.
Run script in environment with python version > 3.8.

If multithreaded version make sure "ThreadPoolExecutor(max_workers=64)" is set to an appropriate value (e.g. max available cores on your PC)

Working_groups.txt needs the following format:
AG_Someone
AG_Anotherone
... so one group per line.

Surnames_to_wg.txt needs the following format:
John, AG_Someone
Jeff, AG_Someone
Max, AG_Anotherone
... so one mapping of surname to group per line.

File_extensions.txt expects one extension per line:
.tif
.jpg
.png
...

paths.txt expects the following:
source_path=Y:\
backup_path=F:\Backup_2023-01-01_2024-04-18\

or similar...

date_range.txt expects the following:
start_date=2023-01-01
end_date=2024-04-18

Once set up, the script will go through all files in the directory source_path, the paths.txt points to.
It will select the files to be copied by the following criteria:

1.file was created in the specified date range and 
2.has one of the surnames from surnames_to_wg.txt in the file name

If both criteria are met the script will create the following dir_structure in backup_path:

├── AG_someone
│   ├── John
│   │   ├── MS001
│   │   │   └── MS001_John_cx.tif
│   │   ├── MS002
│   │   │   └── MS002_John_cx.tif
│   │   └── MS_missing
│   │       └── John_cx.tif
│   ├── Jeff
│   │   ├── MS001
│   │   │   └── MS001_Jeff_cx.tif
│   │   ├── MS002
│   │   │   └── MS002_Jeff_cx.tif
│   │   └── MS_missing
│   │       └── Jeff_cx.tif
│   └── [others]
│       ├── MS001
│       │   └── MS001_[name]_cx.tif
│       ├── MS002
│       │   └── MS002_[name]_cx.tif
│       └── MS_missing
│           └── [name]_cx.tif
└── AG_anotherone
    ├── Lisa
    │   ├── MS001
    │   │   └── MS001_Lisa_cx.tif
    │   ├── MS002
    │   │   └── MS002_Lisa_cx.tif
    │   └── MS_missing
    │       └── MS_missing_Lisa_cx.tif
    ├── Mary
    │   ├── MS001
    │   │   └── MS001_Mary_cx.tif
    │   ├── MS002
    │   │   └── MS002_Mary_cx.tif
    │   └── MS_missing
    │       └── Mary_cx.tif
    └── [others]
        ├── MS001
        │   └── MS001_[name]_cx.tif
        ├── MS002
        │   └── MS002_[name]_cx.tif
        └── MS_missing
            └── [name]_cx.tif

    
      
