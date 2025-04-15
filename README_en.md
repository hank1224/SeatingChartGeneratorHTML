# NTUST Moodle: Generate Exam Seating Chart

Given a CSV file with `First name` and `ID number` columns, this script generates a randomly assigned exam seating chart in HTML format.

It allows customization of the number of seat rows, the number of seats per row, exam subject name, exam date, and exam time.

[Seating Chart Preview](https://hank1224.github.io/SeatingChartGeneratorHTML/seating_chart_frontloaded_zh_rs42.html)

## Usage

### Requires Pandas Package
```bash
pip install pandas
```

### Obtain Student List:
You can directly use **NTUST Moodle to export the student list** and use it as input to generate the seating chart.
1. Select the course.
2. `Participants` > `Enrolled users`
3. Filter for enrolled students and select all students (checkboxes).
4. At the bottom, in the `With selected users...` dropdown menu, choose to download as CSV.

Other CSV files can also be used, but the file must contain these two columns: [CSV File Example](./courseid_12345_participants.csv)
- `First name`: The student's name.
- `ID number`: The student's ID number.

### Configuration Parameters:
- `CSV_FILE_PATH`: **Path to the CSV file.**
- `NUM_ROWS`: Number of seat rows in the classroom.
- `NUM_COLS`: Number of seats per row.
- `RANDOM_SEED`: Random seed for reproducibility.
- `EXAM_SUBJECT`: Name of the exam subject.
- `CLASSROOM`: Classroom name.
- `EXAM_DATE`: Exam date (Example: `"2025/4/16"`).
- `EXAM_TIME`: Exam time (Example: `"10:20 - 12:00"`).
- `LANGUAGE`: Language of the seating chart. Set to `'zh'` for Chinese, and `'en'` for English.