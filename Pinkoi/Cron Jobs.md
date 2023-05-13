### Step1: 建立 Python Script

這個 Script 就是要定期給 Cron Worker 執行的任務，建議放在 `/cron` 底下。

### Step2: 將 Cron Job 定義在 crontab 中

crontab 檔案路徑為 `/_misc/server_conf/crontab.py3`。

> [!Note]
> 建議不要將 cron job 設定在整點，因為已經有很多 jobs 在整點要執行了。