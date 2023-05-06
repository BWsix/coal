from dataclasses import dataclass
from bs4 import BeautifulSoup

import requests

ENDPOINT = "https://tyc1.fdhs.tyc.edu.tw/tyc1/interview_detail.php"


@dataclass
class Record:
    """A record of an applicant's interview experience."""

    year: int
    applicant_school: str
    interview_type: str
    department: str
    record_id: str
    data: dict[str, str]

    def __init__(
        self,
        year: int,
        applicant_school: str,
        interview_type: str,
        department: str,
        record_id: str,
    ):
        self.year = year
        self.applicant_school = applicant_school
        self.interview_type = self.parse_interview_type(interview_type)
        self.department = department.split(" ")[-1]
        self.record_id = record_id
        self.data = {}

    def parse_interview_type(self, interview_type: str) -> str:
        remap = {
            "個人一次...": "個人一次面試",
            "團體一次...": "團體一次面試",
            "個人兩場...": "個人二場或多場面試",
            "團體兩場...": "團體二場或多場面試",
            "其他": "其他",
            "無面試": "無面試",
        }
        return remap[interview_type]

    def fetch(self):
        if self.data:
            return

        res = requests.post(
            ENDPOINT,
            data={
                "data_type": "S",
                "cr_id": self.record_id,
            },
            timeout=5,
        )

        soup = BeautifulSoup(res.text, "html.parser")
        table_element: BeautifulSoup = soup.find(
            "table",
            {"width": "775", "border": "0", "cellspacing": "0", "cellpadding": "0"},
        )
        tr_elements: list[BeautifulSoup] = table_element.find_all(
            "tr", {"height": "30"}
        )

        for tr_element in tr_elements:
            title = tr_element.find("font").text
            content = tr_element.find("td", {"colspan": "3"}).text

            keywords = ["場地", "準備", "注意", "問題", "建議", "叮嚀", "題目", "測試"]
            for keyword in keywords:
                if keyword in title:
                    self.data[title] = content.strip().replace("\r\n", "\n")
                    break

    @property
    def composed_data(self) -> str:
        if not self.data:
            self.fetch()

        paragraph = ""

        for title, content in self.data.items():
            sanitized_content = content.replace("<", "(").replace(">", ")")
            paragraph += f"<seagreen><b>{title}</b></seagreen>\n{sanitized_content}\n"

        return paragraph
