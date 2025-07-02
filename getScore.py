import json
import random
import requests
import sys
import time
from pydantic import BaseModel, Field, ValidationError
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractScrollArea,
    QApplication,
    QHeaderView,
    QLabel,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
import yaml


class IntervalConfig(BaseModel):
    min: float = Field(..., description="最小冷却时间（秒）")
    max: float = Field(..., description="最大冷却时间（秒）")


class Config(BaseModel):
    year: str = Field(..., description="学年")
    semester: str = Field(..., description="学期")
    cookie: str = Field(
        ...,
        description="登录后的 Cookie：访问 https://app.buaa.edu.cn/buaascore/wap/default/index 后 F12 查看 Network 中的 Cookie",
    )
    interval: IntervalConfig = Field(
        IntervalConfig(min=60, max=360),
        description="冷却时间配置",
    )


def load_config_from_dict(d: dict) -> Config:  # type: ignore
    try:
        return Config(**d)  # type: ignore
    except ValidationError as e:
        print("❌ 配置加载失败，详细信息如下：")
        print(e)
        exit(1)


def get_score(year: str, semester: str) -> list[tuple[str, str, str, str]]:
    response = requests.post(
        "https://app.buaa.edu.cn/buaascore/wap/default/index",
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "19",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": config.cookie,
            "Host": "app.buaa.edu.cn",
            "Origin": "https://app.buaa.edu.cn",
            "Referer": "https://app.buaa.edu.cn/buaascore/wap/default/index",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Linux"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        },
        data={"year": year, "xq": semester},
    )
    print("请求时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    dic: dict[str, dict[str, dict[str, str]]] = json.loads(response.text)
    res: list[tuple[str, str, str, str]] = []
    for i in dic["d"].values():
        if i["kccj"] != "":
            res.append((i["kcmc"], i["kccj"], i["xf"], i["kclx"]))
    return res


class TableWindow(QMainWindow):
    def __init__(self, data: list[tuple[str, str, str, str]]) -> None:
        super().__init__()

        self.setWindowTitle("成绩查询")
        self.setGeometry(0, 0, 600, 600)

        self.table = QTableWidget()
        self.setupTable(data)
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            for i in range(1, 4):
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

        title = QLabel("当前已出：")

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.setAlignment(title, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(self.table, Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(30, 30, 30, 30)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def setupTable(self, data: list[tuple[str, str, str, str]]) -> None:
        self.table.setRowCount(len(data))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["课程", "成绩", "学分", "课程类型"])  # type: ignore
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(value))


def show_table(data: list[tuple[str, str, str, str]]) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Breeze")
    window = TableWindow(data)
    window.show()
    app.exec()


with open("config.yaml", encoding="utf-8") as f:
    raw_cfg = yaml.safe_load(f)
config = load_config_from_dict(raw_cfg)
pre = 0
while True:
    try:
        raw = get_score(config.year, config.semester)
        print("已出科目数：", len(raw))
        if pre < len(raw):
            show_table(raw)
        pre = len(raw)
    except requests.exceptions.RequestException as e:
        print("网络错误：", e)
    interval = config.interval.min + random.random() * (
        config.interval.max - config.interval.min
    )
    print(f"冷却时间：{interval} s")
    time.sleep(interval)
