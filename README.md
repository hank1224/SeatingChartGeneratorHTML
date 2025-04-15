# 台科 Moodle：生成考試座位表

給予一個有 `First name` 和 `ID number` 欄位的 CSV 檔案，就能產出隨機分配的考試座位表 HTML。

可自訂 座位排數、每排座位數量、考試科目名稱、考試日期、考試時間。

[座位表預覽](https://hank1224.github.io/SeatingChartGeneratorHTML/)

## 使用方法

### 需要 Pandas 套件
```bash
pip install pandas
```

### 取得學生名單：
可以直接用 **台科 Moodle 輸出學生名單**，丟進來就能直接產表。
1. 選課程
2. `Participants` > `Enrolled users`
3. Filter 出課堂學生後，把學生全選（打勾）
4. 最下面有 `With selected users...` 下拉選單選擇下載 csv。

其他csv也能跑，但檔案必須存在這兩欄：[csv檔案範例](./courseid_12345_participants.csv)
- `First name`：學生的姓名。
- `ID number`：學生的學號。


### 設定參數：
- `CSV_FILE_PATH`**: CSV 檔案的路徑。
- `NUM_ROWS`: 教室的座位排數。
- `NUM_COLS`: 每排座位的個數。
- `RANDOM_SEED`:  隨機種子，提供可重現性。
- `EXAM_SUBJECT`: 考試科目名稱。
- `CLASSROOM`: 教室名稱。
- `EXAM_DATE`: 考試日期 (範例: `"2025/4/16"` )。
- `EXAM_TIME`: 考試時間 (範例: `"10:20 - 12:00"` )。
- `LANGUAGE`:  座位表的語言。設定 `'zh'` 為中文， `'en'` 為英文。
