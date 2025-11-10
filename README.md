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

## Installation

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

The tool expects a CSV file with the following columns:
- Name
- Email
- Additional columns (3-5)
- Availability (6th column) - Contains semicolon-separated time slots
- Comments (7th column) - Optional additional information
- Completion time - Used to extract the year of form submission

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
