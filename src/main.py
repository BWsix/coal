from prompt_toolkit import print_formatted_text, HTML

from .college import COLLEGES, College
from .prompt import Prompt


def main():
    print("\033c", end="")
    print_formatted_text(HTML("<b><skyblue>Welcome to Coal!</skyblue></b>"))
    print("- You can hit Tab to autocomplete, or")
    print("- use Ctrl-C to exit.\n")

    college_name_prompt = Prompt("Enter the college's name: ", list(COLLEGES.keys()))
    college_name = college_name_prompt()
    try:
        college_id = COLLEGES[college_name]
    except KeyError:
        print("Invalid college name.")
        return

    print("Fetching departments...")
    college = College(college_id, college_name)
    departments = college.get_departments()

    department_name_prompt = Prompt("Enter the department's name: ", departments)
    department_name = department_name_prompt()

    print("Fetching records...")
    try:
        records = college.filter_records_by_department_name(department_name)
    except KeyError:
        print("Invalid department name.")
        return

    for record in records[::-1]:
        title = f"\n[{record.year}] {record.interview_type} - {record.applicant_school}"
        print_formatted_text(HTML(f"<b><skyblue>{title}</skyblue></b>"))
        print()
        print_formatted_text(HTML(record.composed_data))
