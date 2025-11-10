import pandas as pd
from datetime import datetime
import sys # Import sys to allow clean exit
import argparse
import glob
import os

def normalize_time_slot(slot):
    """Normalize a time slot string to handle spacing variations"""
    import re
    # Collapse multiple spaces into single spaces
    normalized = re.sub(r'\s+', ' ', slot.strip())
    return normalized

def parse_availability(availability_str):
    """Parse the availability string into a list of time slots"""
    if pd.isna(availability_str) or availability_str == "None of the above":
        return []
    
    # Split by semicolon and clean up each slot
    slots = [normalize_time_slot(slot) for slot in availability_str.split(';') if slot.strip()]
    return slots

def normalize_date(date_str):
    """
    Extract month and day numbers from a date string
    Returns tuple of (month_num, day_num) or (None, None)
    """
    date_str = date_str.strip().lower()
    
    # Month name to number mapping
    months = {
        'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
        'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
        'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9,
        'october': 10, 'oct': 10, 'november': 11, 'nov': 11, 'december': 12, 'dec': 12
    }
    
    # Try to parse format: 10/8, 10/08
    if '/' in date_str:
        parts = date_str.split('/')
        if len(parts) == 2:
            try:
                month = int(parts[0])
                day = int(parts[1])
                return (month, day)
            except:
                pass
    
    # Try to parse format: October 8, Oct 8
    for month_name, month_num in months.items():
        if month_name in date_str:
            # Extract day number from the string
            import re
            day_match = re.search(r'\b(\d+)', date_str)
            if day_match:
                day = int(day_match.group(1))
                return (month_num, day)
    
    return (None, None)

def dates_match(slot_str, search_month, search_day):
    """
    Check if a slot string contains the given month and day
    """
    if search_month is None or search_day is None:
        return False
    
    slot_lower = slot_str.lower()
    
    # Month name to number mapping
    months = {
        'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
        'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
        'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9,
        'october': 10, 'oct': 10, 'november': 11, 'nov': 11, 'december': 12, 'dec': 12
    }
    
    # Check if slot contains numeric format (10/8)
    if f"{search_month}/{search_day}" in slot_lower:
        return True
    
    # Check if slot contains month name format (October 8)
    import re
    for month_name, month_num in months.items():
        if month_num == search_month and month_name in slot_lower:
            # Look for the day number near the month name
            day_pattern = rf'\b{search_day}(?:st|nd|rd|th)?\b'
            if re.search(day_pattern, slot_lower):
                return True
    
    return False

def find_available_guides(csv_file, search_date, include_past=False):
    """
    Find all tour guides available for a specific date
    
    Args:
        csv_file: Path to the CSV file
        search_date: Date to search for
        include_past: If True, include results from past years. If False, only show current year.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"\nERROR: CSV file not found!")
        print(f"Please ensure '{csv_file}' is in the same directory as this script.")
        # Return an empty dictionary to signal failure without crashing
        return None 
    
    # Get the availability column (6th column)
    availability_col = df.columns[5]
    
    # Dictionary to store results: {time_slot: [list of guides]}
    available_guides = {}
    
    # Parse the search date into month and day numbers
    search_month, search_day = normalize_date(search_date)
    
    if search_month is None or search_day is None:
        print(f"Warning: Could not parse date '{search_date}'. Try format like '10/8' or 'October 8'")
        return available_guides
    
    # Get the current year
    current_year = datetime.now().year
    
    # Process each row
    for idx, row in df.iterrows():
        name = row['Name']
        email = row['Email']
        availability = row[availability_col]
        completion_time = str(row["Completion time"])
        
        # Extract year from completion time (format typically: "M/D/YYYY H:MM:SS")
        form_year = None
        import re
        year_match = re.search(r'/(\d{4})', completion_time)
        if year_match:
            form_year = int(year_match.group(1))
        
        # Filter by year unless include_past is True
        if not include_past:
            # Check if the completion time contains a year that is less than current year
            if f"/{current_year - 1}" in completion_time or any(f"/{current_year - i}" in completion_time for i in range(2, 10)):
                continue
        
        # Parse availability slots
        slots = parse_availability(availability)
        
        # Check each slot for the search date
        for slot in slots:
            
            # Check if this slot matches the search date
            if dates_match(slot, search_month, search_day):
                # Normalize the slot key to group similar time slots together
                normalized_slot = normalize_time_slot(slot)
                
                # Add this guide to the time slot
                if normalized_slot not in available_guides:
                    available_guides[normalized_slot] = []
                
                # Get the additional comments (7th column)
                comments = row[df.columns[6]] if pd.notna(row[df.columns[6]]) else ""
                
                guide_info = {
                    'name': name,
                    'email': email,
                    'comments': comments,
                    'year': form_year
                }
                
                # Check if this person is already in this time slot (avoid duplicates)
                already_added = False
                for existing_guide in available_guides[normalized_slot]:
                    if existing_guide['email'] == email:
                        already_added = True
                        # If new entry has a comment and old one doesn't, update it
                        if comments and not existing_guide['comments']:
                            existing_guide['comments'] = comments
                        # Update year if newer entry has a year
                        if form_year and not existing_guide.get('year'):
                            existing_guide['year'] = form_year
                        break
                
                if not already_added:
                    available_guides[normalized_slot].append(guide_info)
    
    return available_guides

def display_results(results, search_date, include_past=False):
    """Display the results in a readable format"""
    # Check if results is None (which happens on FileNotFoundError)
    if results is None:
        # The error message was already printed by find_available_guides
        return

    print(f"\n{'='*60}")
    print(f"Tour Guide Availability for: {search_date}")
    if include_past:
        print(f"(Including past years)")
    else:
        print(f"(Current year: {datetime.now().year})")
    print(f"{'='*60}\n")
    
    if not results:
        print(f"No guides available for '{search_date}'")
        return
    
    # Sort by time slot
    for time_slot in sorted(results.keys()):
        guides = results[time_slot]
        print(f"\n {time_slot}")
        print(f"   {len(guides)} guide(s) available:")
        
        for guide in guides:
            comment_text = f" - {guide['comments']}" if guide['comments'] else ""
            year_text = f" [{guide['year']}]" if guide.get('year') else ""
            print(f"   • {guide['name']} ({guide['email']}){year_text}{comment_text}")
    
    print(f"\n{'='*60}\n")

# Main execution
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Search for tour guide availability by date.')
    parser.add_argument('--past', action='store_true', help='Include results from past years')
    args = parser.parse_args()
    
    # Find CSV files in the current directory
    csv_files = glob.glob("*.csv")
    
    if not csv_files:
        print("\nERROR: No CSV files found in the current directory!")
        print("Please ensure there is at least one CSV file in the same directory as this script.")
        sys.exit(1)
    elif len(csv_files) == 1:
        csv_file = csv_files[0]
        print(f"Using CSV file: {csv_file}")
    else:
        print(f"\nFound {len(csv_files)} CSV files:")
        for i, file in enumerate(csv_files, 1):
            print(f"  {i}. {file}")
        print("\nSelect a file number (or press Enter for first file):")
        choice = input("> ").strip()
        
        if choice == "":
            csv_file = csv_files[0]
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(csv_files):
                    csv_file = csv_files[idx]
                else:
                    print(f"Invalid choice. Using first file: {csv_files[0]}")
                    csv_file = csv_files[0]
            except ValueError:
                print(f"Invalid input. Using first file: {csv_files[0]}")
                csv_file = csv_files[0]
        
        print(f"Using: {csv_file}")
    
    include_past = args.past
    
    # Show status message
    if include_past:
        print("Mode: Including past years")
    else:
        print(f"Mode: Current year only ({datetime.now().year})")
        print("Tip: Use --past flag to include past years")
    
    print("\nEnter dates to search (e.g., '10/28', 'October 29', 'Jan 27')")
    print("Type 'quit' or 'exit' to stop\n")
    
    # Continuous loop for date searches
    while True:
        search_date = input("> ").strip()
        
        # Check for exit commands
        if search_date.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        # Skip empty inputs
        if not search_date:
            continue
        
        # Search and display results
        results = find_available_guides(csv_file, search_date, include_past)
        
        # Check for failure (file not found)
        if results is None:
            break
        
        display_results(results, search_date, include_past)