Nginx 是一個讓電腦可以成為 [[Backend Web Architecture#Web Server|web server]] 的軟體，與它類似的其他軟體還有 Apache。

# 安裝

```bash
sudo apt-get update
sudo apt-get install nginx
```

# 設定檔

Nginx 設定檔：/etc/nginx/nginx.conf

Nginx 設定檔的功能是聲明這個 web server 會 listen 哪些 URLs，以及會如何處理打向這些 URL 的 HTTP(S) requests。

下面是 nginx.conf 的預設檔案內容：

```nginx
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
	worker_connections 768;
	# multi_accept on;
}

http {

	##
	# Basic Settings
	##

	sendfile on;
	tcp_nopush on;
	types_hash_max_size 2048;
	# server_tokens off;

	# server_names_hash_bucket_size 64;
	# server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	##
	# SSL Settings
	##

	ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;

	##
	# Logging Settings
	##

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	##
	# Gzip Settings
	##

	gzip on;

	# gzip_vary on;
	# gzip_proxied any;
	# gzip_comp_level 6;
	# gzip_buffers 16 8k;
	# gzip_http_version 1.1;
	# gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

	##
	# Virtual Host Configs
	##

	include /etc/nginx/conf.d/*.conf;
	include /etc/nginx/sites-enabled/*;
}


#mail {
#	# See sample authentication script at:
#	# http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
#
#	# auth_http localhost/auth.php;
#	# pop3_capabilities "TOP" "USER";
#	# imap_capabilities "IMAP4rev1" "UIDPLUS";
#
#	server {
#		listen     localhost:110;
#		protocol   pop3;
#		proxy      on;
#	}
#
#	server {
#		listen     localhost:143;
#		protocol   imap;
#		proxy      on;
#	}
#}
```

### 模組化

Nginx 設定檔中可以使用 `include` 來引入另一個設定檔，因此建議可以把性質相近的設定寫在一個檔案，再由一個最終的設定檔來將各個片段 include 進來。

### sites-available & sites-enable

Server block configuration files 會放在 /etc/nginx/sites-available/ 下面，但這些設定檔預設都是不啟用的，若要啟用某個設定檔，就必須在 /etc/nginx/sites-enable/ 放入要使用的設定檔的 link。

詳細步驟如下：

##### Step1: 建立 Server Block Configuration File 並放在 /etc/nginx/sites-available/ 底下

e.g.

```nginx
server {
   listen 80;
   server_name your_domain.com www.your_domain.com;
   location / {
       include proxy_params;
       proxy_pass http://127.0.0.1:8000; # Assuming Gunicorn is running on 127.0.0.1:8000
   }
}
```

##### Step2: 在 /etc/nginx/sites-enable/ 底下為要啟用的設定檔建立 Link

>[!Note]
>Remember to replace `your_app` with the actual file name.

```bash
sudo ln -s /etc/nginx/sites-available/your_app /etc/nginx/sites-enabled
```

### Nginx 作為 Static File Server

Nginx 作為 static file server 時，這些 static file 一定要放在 /var/www/html/`project_name`，否則 Nginx 會沒有權限 access，client side 就會拿到 403 或 500。

---

設定 HTTP 的部分主要分三層：`http`、`server` 及 `location`。`http` 只會有一個，底下會有一到多個 virtual "servers"，多個 virtual servers 可以讓一台機器 serve 不同的 directory 給不同的 URL；一個 virtual server 底下會有一到多個 "locations"，用來設定哪些位置的檔案要被 serve。

# 常用指令

>[!Note]
>執行下方指令時，若需要 superuser 權限，就在最前面加上 `sudo`。

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
# or
nginx -s reload

## On Alpine Linux
/etc/init.d/nginx restart
```

>[!Note]
>Reload 與 restart 不同，reload 是 "gracefully restart after config change"，restart 則是直接 restart。

### 關閉 Nginx Server

```bash
## On Linux
systemctl stop nginx

## On Debian/Ubuntu/RHEL/CentOS Linux
service nginx stop
```

### 查看目前 Nginx 版本

```bash
nginx -v
```

# 參考資料

- <https://docs.nginx.com/nginx/admin-guide/web-server/web-server/>
- <https://www.cyberciti.biz/faq/nginx-linux-restart/>
