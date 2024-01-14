import json
import random
import requests
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractScrollArea,
    QApplication,
    QLabel,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

year: str = "2023-2024"
semester: str = "1"  # "1" | "2" | "3" 对应秋、春、夏
cookies: str = "" # 访问 https://app.buaa.edu.cn/buaascore/wap/default/index，复制 Cookie 并替换


def get_score(year: str, semester: str):
    response = requests.post(
        "https://app.buaa.edu.cn/buaascore/wap/default/index",
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "19",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": cookies,
            "Host": "app.buaa.edu.cn",
            "Origin": "https://app.buaa.edu.cn",
            "Referer": "https://app.buaa.edu.cn/buaascore/wap/default/index",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
        },
        data={"year": year, "xq": semester},
    )
    print("请求时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    dic: dict[str, dict] = json.loads(response.text)
    res = []
    for i in dic["d"].values():
        if i["xf"] is not None:
            res.append(
                {"km": i["kcmc"], "cj": i["kccj"], "xf": i["xf"], "lx": i["kclx"]}
            )
    return res


class TableWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("成绩查询")
        self.setGeometry(0, 0, 600, 600)

        self.table = QTableWidget()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setupTable(data)

        title = QLabel("当前已出：")

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.setAlignment(title, Qt.AlignHCenter)
        layout.setAlignment(self.table, Qt.AlignHCenter)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def setupTable(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["课程", "成绩", "学分", "课程类型"])
        for row, i in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(i["km"]))
            self.table.setItem(row, 1, QTableWidgetItem(i["cj"]))
            self.table.setItem(row, 2, QTableWidgetItem(i["xf"]))
            self.table.setItem(row, 3, QTableWidgetItem(i["lx"]))


def show_table(data):
    app = QApplication(sys.argv)
    window = TableWindow(data)
    window.show()
    app.exec()


while True:
    try:
        raw = get_score(year, semester)
    except:
        raw = []
    show_table(raw)
    interval = 60 + random.random() * 300
    print(interval)
    time.sleep(interval)
