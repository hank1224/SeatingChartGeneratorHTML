import pandas as pd
import random
import os

def generate_frontloaded_seating_html(csv_filepath, rows, cols, exam_subject, classroom, exam_date, exam_time, output_filename="seating_chart_frontloaded.html", random_state=None, language='zh'):
    """
    Reads student names and ID numbers from a CSV, generates a front-loaded seating chart, and saves it as an HTML file.
    The HTML page displays the exam subject, classroom, date, and time.

    Args:
        csv_filepath (str): Path to the CSV file containing student data (should include 'First name' and 'ID number' columns).
        rows (int): Number of rows in the classroom.
        cols (int): Number of seats per row in the classroom.
        exam_subject (str): Name of the exam subject.
        classroom (str): Name of the classroom.
        exam_date (str): Exam date.
        exam_time (str): Exam time.
        output_filename (str): Filename to save the HTML (suggested extension: .html).
        random_state (int, optional): Seed value for randomizing student order.
                                      Using the same value will produce the same random result.
                                      If None, results will vary on each execution.
        language (str, optional): Language for the HTML output, 'zh' for Chinese, 'en' for English. Defaults to 'zh'.

    Returns:
        str: Returns the HTML filename on success, None on failure.
    """
    # --- 1. Read CSV file ---
    try:
        # Specify dtype as str to prevent ID numbers from being parsed as numbers
        df = pd.read_csv(csv_filepath, encoding='utf-8', dtype=str)
        # Check if required columns exist
        required_cols = ['First name', 'ID number']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Error: Required columns not found in CSV file '{csv_filepath}': {', '.join(missing_cols)}.")
            return None

        # Get student data (name, ID number) and remove rows with empty names or ID numbers
        df_filtered = df[required_cols].dropna()
        students = list(zip(df_filtered['First name'], df_filtered['ID number']))
        n_students = len(students)

        if n_students == 0:
             print(f"Warning: No valid student data found in '{csv_filepath}' (check if 'First name' and 'ID number' columns are empty).")
             # Continue to generate an empty seating chart even with no students
        else:
            print(f"Successfully read data for {n_students} students.")

    except FileNotFoundError:
        print(f"Error: File not found '{csv_filepath}'. Please check the filename and path.")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    # --- 2. Check if there are enough seats ---
    total_seats = rows * cols
    if n_students > total_seats:
        print(f"Error: Number of students ({n_students}) exceeds total seats ({total_seats}).")
        return None

    # --- 3. Randomly shuffle students ---
    if random_state is not None:
        random.seed(random_state)
    random.shuffle(students)
    print(f"Student order randomized using Random State = {random_state}.")

    # --- 4. Create an empty seating chart (data structure) ---
    seating_data = [["Empty"] * cols for _ in range(rows)] # Initialize with "Empty" in English
    student_idx = 0
    seats_filled = 0

    # --- 5. Fill in students in the front rows ---
    for r in range(rows):
        for c in range(cols):
            if student_idx < n_students:
                first_name, id_number = students[student_idx]
                # Use HTML <br> for line break
                seating_data[r][c] = f"{first_name}<br>{id_number}"
                student_idx += 1
                seats_filled += 1
            else:
                break # All students are seated
        if student_idx >= n_students:
            break # Break outer loop

    print(f"Successfully seated {seats_filled} students.")

    # --- 6. Generate HTML content ---
    if language == 'zh':
        html_title = "考試座位表"
        seat_label_prefix = "座位 "
        row_label_prefix = "第"
        row_label_suffix = "排"
        empty_seat_text = "空"
        random_state_text = "Random State: "
    elif language == 'en':
        html_title = "Exam Seating Chart"
        seat_label_prefix = "Seat "
        row_label_prefix = "Row "
        row_label_suffix = ""
        empty_seat_text = "Empty"
        random_state_text = "Random State: "
    else:
        print(f"Warning: Unknown language code '{language}'. Defaulting to Chinese ('en').")
        html_title = "Exam Seating Chart"
        seat_label_prefix = "Seat "
        row_label_prefix = "Row "
        row_label_suffix = ""
        empty_seat_text = "Empty"
        random_state_text = "Random State: "


    html_content = f"""
<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_title}</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
            margin: 20px;
        }}
        h1 {{
            text-align: center;
            color: #333;
        }}
        table {{
            width: 95%; /* Adjust table width */
            margin: 20px auto;
            border-collapse: collapse;
            border: 2px solid #666;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 10px 8px; /* Adjusted padding */
            text-align: center;
            min-height: 50px; /* Ensure cells have a minimum height */
            vertical-align: middle; /* Center content vertically */
            font-size: 11pt; /* Slightly larger font */
            word-wrap: break-word; /* Allow long words to break */
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        td {{
            background-color: #fff;
            line-height: 1.4; /* Improve readability for two lines */
        }}
        td:empty {{ /* Style empty cells differently if needed */
            background-color: #fafafa;
        }}
        .empty-seat {{
             color: #999;
             font-style: italic;
        }}
        /* Header row and column styles */
        thead th {{
             position: sticky;
             top: 0; /* Stick the header row to the top when scrolling */
             background-color: #e0e0e0;
             z-index: 10;
        }}
        tbody th {{
            background-color: #f2f2f2;
            font-weight: bold;
            position: sticky;
            left: 0; /* Stick the row label column to the left */
            z-index: 5;
        }}
         /* Top-left corner cell */
        thead th:first-child {{
             position: sticky;
             left: 0;
             top: 0;
             z-index: 15; /* Ensure it's above both sticky row and column */
        }}
    </style>
</head>
<body>

<h1>{html_title} - {exam_subject} | {classroom} | {exam_date} {exam_time} ({random_state_text}{random_state})</h1>

<table>
    <thead>
        <tr>
            <th></th> <!-- Corner cell -->
"""
    # Add column headers (Seat 1, Seat 2, ...)
    for c in range(cols):
        html_content += f"            <th>{seat_label_prefix}{c+1}</th>\n"
    html_content += """
        </tr>
    </thead>
    <tbody>
"""
    # Add seating data rows
    for r in range(rows):
        row_label = f"{row_label_prefix}{r+1}{row_label_suffix}"
        html_content += f"        <tr>\n            <th>{row_label}</th>\n" # Row header
        for c in range(cols):
            cell_content = seating_data[r][c]
            if cell_content == "Empty": # Compare with "Empty" in English
                html_content += f'            <td class="empty-seat">{empty_seat_text}</td>\n'
            else:
                 html_content += f"            <td>{cell_content}</td>\n"
        html_content += "        </tr>\n"

    html_content += """
    </tbody>
</table>

</body>
</html>
"""

    # --- 7. Save HTML file ---
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Seating chart HTML successfully saved to: {output_filename}")
        return output_filename
    except Exception as e:
        print(f"Error saving HTML file: {e}")
        return None

#################### --- Configuration parameters --- ##########################

CSV_FILE_PATH = "courseid_14612_participants.csv"

NUM_ROWS = 7 # Number of rows in the classroom
NUM_COLS = 8 # Number of seats per row in the classroom

# Set a fixed number to get the same random arrangement every time
RANDOM_SEED = 42

# --- Add exam information ---
EXAM_SUBJECT = "IM1201302 計算機程式"
CLASSROOM = "MA-215"
EXAM_DATE = "2025/4/16"
EXAM_TIME = "10:20 ~ 12:00"

# --- Language setting ---
LANGUAGE = 'zh'  # Set to 'zh' for Chinese, 'en' for English

# Set the output HTML filename based on language
OUTPUT_HTML_FILE = f"seating_chart_frontloaded_{LANGUAGE}_rs{RANDOM_SEED}.html"

################################################################################

# --- Execute and save HTML (based on selected language) ---
output_file = generate_frontloaded_seating_html(
    CSV_FILE_PATH,
    NUM_ROWS,
    NUM_COLS,
    exam_subject=EXAM_SUBJECT,
    classroom=CLASSROOM,
    exam_date=EXAM_DATE,
    exam_time=EXAM_TIME,
    output_filename=OUTPUT_HTML_FILE,
    random_state=RANDOM_SEED,
    language=LANGUAGE  # Use the LANGUAGE variable here
)

if output_file:
    print(f"\nProgram finished, please open the file in your browser: {os.path.abspath(output_file)}")
else:
    print("\nProgram failed.")