# buaa-get-score

BUAA 自动查分

# Usage

更改 `config.yaml` 中的配置，运行 `getScore.py` 即可。

```yaml
year: "2024-2025" # 学年
semester: "2"     # 学期，"1" | "2" | "3" 对应秋、春、夏
cookie: ""        # 访问 https://app.buaa.edu.cn/buaascore/wap/default/index，控制台中查询 Cookie
interval:
  min: 60         # 最小冷却时间（秒）
  max: 300        # 最大冷却时间（秒）
```

相邻查询时间间隔秒数在配置的时间间隔内随机生成，出现新出科目则弹窗。

# Warning

**查询结果与是否评教无关，请做好心理准备。**
