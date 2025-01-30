Cron 是 Linux OS 內建的排程系統，其運作方式是使用者將 **cron expression** 與要定時執行的指令寫入 Cron 的設定檔，Cron 就會根據 cron expression 定時執行指令。

# Cron Expression

Cron expression 由 `分`、`時`、`日`、`月`、`星期幾` 五個部分組成。

有以下幾種特殊字元可使用：

- `*`：表示所有值
- `,`：用來分隔一個欄位中的多個數字，e.g. `0,2,5`
- `-`：表示 range，e.g. `1-5`
- `/`：表示間隔值，e.g. `*/2`、`1-50/5`

Example:

```cron
* 9-14 * * MON-FRI 
```
### [Tool](https://crontab.guru/)

# 常用指令

### 查看所有 Jobs

```bash
crontab -l
```

### 匯出

```bash
crontab -l > /PATH/TO/TARGET/FILE
```


### 匯入

```bash
crontab /PATH/TO/SOURCE/FILE
```

### 匯入至某個 User 的 Crontab

```bash
crontab -u USERNAME /PATH/TO/FILE
```

### 編輯

```bash
crontab -e
```

### 刪除所有 Jobs

```bash
crontab -r
```

### Gracefully Restart Cron

```bash
sudo systemctl reload cron
```

### Hard Restart Cron

```bash
sudo systemctl restart cron
```

### 查看與 Cron 相關的 System log

```bash
sudo grep cron /var/log/syslog
```

# 其它類似工具

### [Airflow](</Services/Airflow.canvas>)

Airflow 是一款免費且 open source 的工具，最初由 Airbnb 公司開發，後來轉賣給 Apache。在 Airflow 中，可以設定流程（任務間的先後順序），且有 GUI 將流程與任務的執行狀況視覺化。
