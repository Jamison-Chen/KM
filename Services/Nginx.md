Nginx 是一個讓電腦可以成為 [[Backend Web Architecture#Web Server|web server]] 的軟體，與它類似的其他軟體還有 Apache。

# 設定檔

Nginx 預設設定檔名為 nginx.conf，其所在的路徑為 /etc/nginx/。

Nginx 設定檔的功能是聲明這個 web server 會處理哪些 URL，以及會如何處理這些 URL 背後的 HTTP requests。

設定 HTTP 的部分主要分三層：`http`、`server`，以及 `location`。http 只會有一個，底下會有一到多個 virtual "servers"，多個 virtual servers 可以讓一台機器 serve 不同的 directory 給不同的 URL；一個 virtual server 底下會有一到多個 "locations"，用來設定哪些位置的檔案要被 serve。

下面是一個 nginx.conf 的範例：

```plaintext
```

#TODO 

### 模組化

Nginx 設定檔中可以使用 `include` 來引入另一個設定檔，因此建議可以把性質相近的設定寫在一個檔案，再由一個最終的設定檔來將各個片段 include 進來。

# 指令

### 啟動 Nginx Server

```bash
systemctl start nginx
# or
service nginx start
```

### 查看 Nginx Server 的狀態

```bash
systemctl status nginx
# or
service nginx status
```

### 測試設定檔

通常如果有改設定檔，為避免設定檔有誤，不會直接 reload server，會先使用這個指令測試設定檔是否無誤：

```bash
nginx -t
```

### Reload Nginx Server

```bash
## On Linux
systemctl restart nginx.service

## On Debian/Ubuntu/RHEL/CentOS Linux
service nginx reload
# or
service nginx restart

## On Alpine Linux
/etc/init.d/nginx restart
```

>[!Note]
>Reload 與 restart 不同，reload 是 "gracefully restart after config change"，restart 則是直接 restart。

### 關閉 Nginx Server

```bash
systemctl stop nginx
# or
service nginx stop
```

### 查看目前 Nginx 版本

```bash
nginx -v
```

# 參考資料

- <https://docs.nginx.com/nginx/admin-guide/web-server/web-server/>
- <https://www.cyberciti.biz/faq/nginx-linux-restart/>
