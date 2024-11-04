import json
import os
from collections import OrderedDict

filename = ""

def setFileName(new_filename):
    global filename
    filename = new_filename

def get_questions():
    data = read_json()
    if "questions" not in data:
        return []
    
    return data["questions"]

def read_json():
    """
    Reads a JSON file and returns the data as a dictionary.
    If the file does not exist, creates an empty JSON file and returns an empty dictionary.
    """
    if not os.path.exists(filename):
        # Create an empty JSON file
        with open(filename, "w") as file:
            json.dump({}, file)
        return {}

    with open(filename, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}

    return data

def write_json(question):
    """
    Updates dictionary of questions 
    """
    # Load existing data
    data = read_json()
    
    # append question to {"questions" : ["abs?", "abc?"]}
    if "questions" not in data:
        data["questions"] = []

    data["questions"].append(question)

    # Check the file size and update with trimmed data if needed
    data = check_file_size(data, filename)

    # Write the updated dictionary back to the JSON file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def check_file_size(data, filename="police_tweet_map.json", max_records=200, records_to_remove=40):
    """
    Checks if the JSON file has more than max_records. If so, removes the oldest
    records_to_remove records from the data and returns the updated data.
    """
    # Only proceed if the data exceeds max_records
    if len(data) > max_records:
        print(f"File has {len(data)} records, trimming to {max_records - records_to_remove}.")

        # Convert to an OrderedDict to maintain insertion order (Python 3.7+ dicts preserve order)
        ordered_data = OrderedDict(data)

        # Remove the oldest records
        for _ in range(records_to_remove):
            ordered_data.popitem(last=False)

        return ordered_data  # Return the trimmed data

    return data  # Return data as-is if no trimming was needed
