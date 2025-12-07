# CoGen_Scheduler

A Python tool to efficiently search and display tour guide availability for Cogen Plant tours based on CSV form responses.

## Features

- **Auto CSV Detection**: Automatically finds and uses CSV files in the directory
- **Date-based Search**: Search for available tour guides by specific dates (supports multiple date formats)
- **Smart Year Filtering**: Automatically filters results based on the current year
- **Command-line Flag**: Use `--past` flag to optionally include historical data
- **Form Year Display**: Shows which year each guide submitted their availability
- **Flexible Date Parsing**: Accepts dates in formats like "10/28", "October 29", "Jan 27"

## Requirements

- Python 3.x
- pandas (third-party library)
- Built-in modules: `datetime`, `sys`, `argparse`, `glob`, `os`, `re` (included with Python)
- Any CSV file with tour guide availability data

### First Time Setup - Check if Python is Installed

If you've never used Python before, follow these steps:

**Windows:**
1. Open Command Prompt (search for "cmd" in Start Menu)
2. Type: `python --version` and press Enter
3. If you see something like "Python 3.x.x" - you're good to go!
4. If you see an error or "command not found":
   - Open Microsoft Store (search for it in Start Menu)
   - Search for "Python 3.12" (or latest version)
   - Click "Get" or "Install"
   - Wait for installation to complete
   - Restart Command Prompt and try step 2 again

**Mac/Linux:**
1. Open Terminal
2. Type: `python3 --version` and press Enter
3. If you see "Python 3.x.x" - you're ready!
4. If not installed, download from [python.org/downloads](https://www.python.org/downloads/)

## Installation

### Option 1: Quick Setup (Single File)

Perfect for quick use - just download and run:

1. **Check Python is installed** (see "First Time Setup" above if needed)

2. Download `availability.py` from this repository
   - Click on `availability.py` in the file list above
   - Click the "Download" or "Raw" button and save the file

3. Install pandas (one-time setup):
   - Open Command Prompt (Windows) or Terminal (Mac/Linux)
   - Type: `pip install pandas` and press Enter
   - Wait for it to finish (you'll see "Successfully installed...")

4. Place your CSV file in the same folder as `availability.py`
   - Create a folder like "Tour Scheduler" on your Desktop
   - Put both `availability.py` and your CSV file in this folder

5. Run the script:
   - Open Command Prompt or Terminal
   - Type: `cd` followed by a space
   - Open the folder where you saved `availability.py` and your CSV
   - Drag the folder into the Command Prompt window (this pastes the full path)
   - Press Enter
   - Now type: `python availability.py` and press Enter
   
   **Alternative (easier):**
   - Open the folder containing `availability.py` and your CSV file
   - Type `cmd` in the address bar at the top of the folder window and press Enter
   - Command Prompt will open in that folder automatically
   - Type: `python availability.py` and press Enter

That's it! No need to clone the entire repository.

**Troubleshooting:**
- If `python` doesn't work, try `python3` instead
- If `pip` doesn't work, try `pip3` or `python -m pip install pandas`

### Option 2: Full Repository Clone

For development or if you want all files including tests and documentation:

1. Clone this repository:
```bash
git clone https://github.com/jessephasouk/CoGen_Scheduler.git
cd CoGen_Scheduler
```

2. Install required dependencies:
```bash
pip install pandas
```

All other dependencies are built-in Python modules and require no installation.

## Usage

1. Download the CSV file from the Excel sheet or Google Form
   - If using Microsoft Forms: Open your Forms response Excel file → File → Save As → CSV format
   - The Excel file is automatically generated from Microsoft Forms responses

2. Place the CSV file in the same directory as `availability.py`
   - The script will automatically detect any `.csv` file in the directory
   - If multiple CSV files exist, you'll be prompted to choose one

3. Run the script:
```bash
# For current year results only
python availability.py

# To include past years
python availability.py --past
```

3. Enter dates continuously:
   - Type a date to search (e.g., "10/28", "October 29", "Jan 27")
   - View available guides organized by time slot
   - Enter another date immediately - no confirmations needed!
   - Type 'quit', 'exit', or 'q' to stop

### Example Session

```
Using CSV file: example.csv
Mode: Current year only (2025)
Tip: Use --past flag to include past years

Enter dates to search (e.g., '10/28', 'October 29', 'Jan 27')
Type 'quit' or 'exit' to stop

> 10/28

============================================================
Tour Guide Availability for: 10/28
(Current year: 2025)
============================================================

 October 28, 2:00 PM - 3:00 PM
   2 guide(s) available:
   • John Doe (john@example.com) [2025]
   • Jane Smith (jane@example.com) [2025] - Prefer afternoon slots

============================================================

> 10/29

============================================================
Tour Guide Availability for: 10/29
(Current year: 2025)
============================================================

 October 29, 10:00 AM - 11:00 AM
   1 guide(s) available:
   • Bob Johnson (bob@example.com) [2025]

============================================================

> quit

Goodbye!
```

### Command Line Options

- `--past` : Include results from past years in addition to current year
  - Example: `python availability.py --past`

## How It Works

1. **Date Parsing**: The tool normalizes various date formats into a standardized format for matching
2. **Time Slot Matching**: Searches through all form responses to find guides available for the specified date
3. **Year Filtering**: By default, only shows current year submissions unless "include past years" is selected
4. **Results Display**: Groups guides by time slot and shows their contact information, submission year, and any additional comments

## CSV Format Expected

The tool expects a CSV file with columns and data similar to this (auto-generated from Microsoft Forms → Excel):

```
Id,Start time,Completion time,Email,Name,"I can go on a tour with these dates and times:","Anything else we should know before you get scheduled? (can't stay for whole time, looking to shadow, want to give walking tour, etc.)"
1,10/9/2024 11:02,10/9/2024 11:03,john.doe@example.com,John Doe,"Monday, 10/28:  10:10am-11am;Tuesday, 10/29: 12:30pm-1:20pm;",
```

**Note:** This tool is designed to work with CSV files exported from Microsoft Forms → Excel. The Excel workbook is auto-generated from a Microsoft Forms availability survey. If you're creating your own CSV file, make sure the column structure and order matches this format for the script to work correctly.

## File Structure

```
CoGen_Scheduler/
├── availability.py              # Main script
├── *.csv                        # Any CSV file with availability data
└── README.md                    # Documentation
```

## Notes

- The script automatically finds CSV files using `*.csv` wildcard pattern
- If multiple CSV files are present, you'll be prompted to choose which one to use
- The CSV file name doesn't need to match a specific pattern

## Contributing

Feel free to submit issues or pull requests for improvements.

## License

This project is open source and available for use.
