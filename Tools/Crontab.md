# 常用指令

### 查看

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

### 全部刪除

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
