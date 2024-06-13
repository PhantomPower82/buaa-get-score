# buaa-get-score

BUAA 自动查分

# Usage

更改 `getScore.py` 中以下三个变量，运行即可。

```py3
year: str = "2023-2024"
semester: str = "1"     # "1" | "2" | "3" 对应秋、春、夏
cookie: str = ""        # 访问 https://app.buaa.edu.cn/buaascore/wap/default/index，控制台中查询 Cookie
```

相邻查询时间间隔秒数在 $[60, 360)$ 内，出现新出科目则弹窗。

# Warning

**查询结果与是否评教无关，请做好心理准备。**
