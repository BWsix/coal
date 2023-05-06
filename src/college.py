import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from .record import Record

ENDPOINT = "https://tyc1.fdhs.tyc.edu.tw/tyc1/interview_search.php"
COLLEGES = {
    "國立中山大學": "13",
    "國立中央大學": "12",
    "國立中正大學": "15",
    "國立中興大學": "10",
    "國立交通大學": "11",
    "國立成功大學": "9",
    "國立宜蘭大學": "33",
    "國立東華大學": "22",
    "國立金門大學": "53",
    "國立屏東大學": "42",
    "國立政治大學": "5",
    "國立高雄大學": "21",
    "國立高雄師範大學": "16",
    "國立國防大學": "169",
    "國立清華大學": "6",
    "國立陽明大學": "18",
    "國立新竹教育大學": "40",
    "國立嘉義大學": "20",
    "國立彰化師範大學": "17",
    "國立暨南國際大學": "23",
    "國立臺中教育大學": "41",
    "國立臺北大學": "19",
    "國立臺北教育大學": "39",
    "國立臺北藝術大學": "30",
    "國立臺北護理健康大學": "48",
    "國立臺東大學": "32",
    "國立臺南大學": "38",
    "國立臺南藝術大學": "37",
    "國立臺灣大學": "7",
    "國立臺灣師範大學": "8",
    "國立臺灣海洋大學": "14",
    "國立臺灣藝術大學": "31",
    "國立臺灣體育運動大學": "1916",
    "國立聯合大學": "34",
    "國立體育大學": "46",
    "臺北市立大學": "167",
    "臺北市立體育學院(併臺北市立大學)": "168",
    "大同大學": "79",
    "大葉大學": "69",
    "中山醫學大學": "86",
    "中原大學": "61",
    "中國文化大學": "63",
    "中國醫藥大學": "92",
    "中華大學": "68",
    "元智大學": "67",
    "世新大學": "72",
    "正修科技大學": "94",
    "玄奘大學": "96",
    "立德管理學院": "117",
    "佛光大學": "107",
    "亞洲大學": "105",
    "明道大學": "115",
    "東吳大學": "60",
    "東海大學": "58",
    "長庚大學": "66",
    "長榮大學": "90",
    "南華大學": "77",
    "致遠管理學院": "116",
    "真理大學": "78",
    "馬偕醫學院": "1934",
    "高雄醫學大學": "76",
    "淡江大學": "62",
    "逢甲大學": "64",
    "華梵大學": "70",
    "開南大學": "106",
    "慈濟大學": "84",
    "義守大學": "71",
    "實踐大學": "74",
    "臺北醫學大學": "85",
    "輔仁大學": "59",
    "銘傳大學": "73",
    "興國管理學院": "118",
    "靜宜大學": "65",
    "國立虎尾科技大學": "35",
    "國立屏東科技大學": "26",
    "國立屏東商業技術學院": "49",
    "國立高雄科技大學": "1952",
    "國立高雄海洋科技大學(現 國立高雄科技大學)": "36",
    "國立高雄第一科技大學(現 國立高雄科技大學)": "28",
    "國立高雄餐旅學院": "51",
    "國立高雄應用科技大學(現 國立高雄科技大學)": "29",
    "國立雲林科技大學": "25",
    "國立勤益科技大學": "45",
    "國立臺中科技大學": "50",
    "國立臺中護理專科學校": "55",
    "國立臺北科技大學": "27",
    "國立臺北商業技術學院": "52",
    "國立臺東專科學校": "57",
    "國立臺南護理專科學校": "56",
    "國立臺灣科技大學": "24",
    "國立臺灣戲曲學院": "54",
    "國立臺灣體育學院": "47",
    "國立澎湖科技大學": "44",
    "大仁科技大學": "100",
    "大同技術學院": "148",
    "大華科技大學": "119",
    "大漢技術學院": "122",
    "中州技術學院": "133",
    "中國科技大學": "103",
    "中華技術學院": "120",
    "中華醫事科技大學": "112",
    "中臺科技大學": "104",
    "仁德醫護管理專校": "157",
    "元培科技大學": "110",
    "文藻外語學院": "121",
    "北台灣科學技術學院": "127",
    "台北海洋技術學院": "154",
    "台南科技大學": "108",
    "弘光科技大學": "91",
    "永達技術學院": "124",
    "吳鳳技術學院": "135",
    "育英醫護管理專校": "163",
    "育達商業技術學院": "126",
    "亞東技術學院": "130",
    "和春技術學院": "125",
    "明志科技大學": "98",
    "明新科技大學": "89",
    "東方技術學院": "144",
    "東南科技大學": "113",
    "法鼓佛教研修學院": "153",
    "長庚技術學院": "146",
    "南台科技大學": "80",
    "南亞技術學院": "131",
    "南開技術學院": "140",
    "南榮技術學院": "141",
    "建國科技大學": "97",
    "美和技術學院": "136",
    "致理技術學院": "128",
    "修平技術學院": "137",
    "耕莘健康管理專科學校": "160",
    "馬偕醫護管理專科學校": "156",
    "高美醫護管理專校": "162",
    "高苑科技大學": "99",
    "高鳳技術學院": "150",
    "崇仁醫護管理專科學校": "164",
    "崇右技術學院": "147",
    "崑山科技大學": "81",
    "康寧醫護暨管理專校": "155",
    "敏惠醫護管理專校": "161",
    "清雲科技大學": "93",
    "景文科技大學": "111",
    "朝陽科技大學": "75",
    "華夏技術學院": "151",
    "慈惠醫護管理專校": "159",
    "慈濟技術學院": "123",
    "新生醫護管理專科學校": "166",
    "萬能科技大學": "95",
    "經國管理暨健康學院": "145",
    "聖母醫護管理專科學校": "165",
    "聖約翰科技大學": "101",
    "僑光技術學院": "132",
    "嘉南藥理大學": "82",
    "臺灣觀光學院": "152",
    "輔英科技大學": "88",
    "遠東科技大學": "109",
    "德明財經科技大學": "114",
    "德霖技術學院": "139",
    "稻江科技暨管理學院": "138",
    "黎明技術學院": "143",
    "樹人醫護管理專校": "158",
    "樹德科技大學": "83",
    "親民技術學院": "149",
    "醒吾技術學院": "129",
    "龍華科技大學": "87",
    "嶺東科技大學": "102",
    "環球技術學院": "134",
    "蘭陽技術學院": "142",
    "國防醫學院": "1936",
    "中央警察大學": "1937",
    "空軍軍官學校": "1940",
    "海軍官校": "1941",
    "國防大學": "1935",
    "海外大學(大陸)": "1946",
    "海外大學(日本)": "1944",
    "海外大學(加拿大)": "1950",
    "海外大學(其他)": "1951",
    "海外大學(東南亞)": "1948",
    "海外大學(美國)": "1947",
    "海外大學(香港、澳門)": "1945",
    "海外大學(歐洲)": "1943",
    "海外大學(韓國)": "1949",
}


@dataclass
class College:
    """A college."""

    idx: str
    name: str
    records: list[Record]

    def __init__(self, idx: str, name: str):
        self.idx = idx
        self.name = name
        self.records = []

        self._init()

    def _init(self):
        res = requests.post(
            ENDPOINT,
            self.get_form_data(),
            timeout=5,
        )
        soup = BeautifulSoup(res.text, "html.parser")
        page_count = self.extract_page_count_from_soup(soup)

        records = self.extract_records_from_soup(soup)
        self.records.extend(records)

        for page in range(2, page_count + 1):
            res = requests.post(
                ENDPOINT,
                self.get_form_data(page),
                timeout=5,
            )
            soup = BeautifulSoup(res.text, "html.parser")

            records = self.extract_records_from_soup(soup)
            self.records.extend(records)

    def get_departments(self) -> set[str]:
        return set(record.department for record in self.records)

    def filter_records_by_department_name(self, department_name: str) -> list[Record]:
        records = []

        for record in self.records:
            if record.department == department_name:
                record.fetch()
                records.append(record)

        if not records:
            raise KeyError("No such department.")

        return records

    def extract_page_count_from_soup(self, soup: BeautifulSoup) -> int:
        center_element = soup.find("center")
        text = center_element.get_text()
        match = re.search(r"\b\d+\b", text)

        if match:
            return int(match.group()) // 100 + 1
        else:
            return -1

    def extract_records_from_soup(self, soup: BeautifulSoup) -> list[Record]:
        records: list[Record] = []

        table_element: list[BeautifulSoup] = soup.find(
            "table",
            {"border": "1", "align": "center", "cellpadding": "5", "cellspacing": "0"},
        )
        tr_elements: list[BeautifulSoup] = table_element.find_all("tr")[1:]
        for tr_element in tr_elements:
            td_elements = tr_element.find_all("td")
            input_elements = tr_element.find_all("input")

            year = int(td_elements[1].get_text().strip())
            applicant_school: str = td_elements[2].get_text().strip()
            interview_type: str = td_elements[3].get_text().strip()
            department: str = td_elements[4].get_text().strip()
            record_id: str = input_elements[1]["value"]

            if len(department.split(" ")) == 1:
                department = f"{department} (沒有填寫系名)"

            record = Record(
                year, applicant_school, interview_type, department, record_id
            )
            records.append(record)

        return records

    def get_form_data(self, page=1) -> dict[str, str]:
        return {
            "s_university": "Y",
            "s_university_value": self.idx,
            "p_i": str(page),
            "p_l": "100",
            "submit": "Y",
        }
