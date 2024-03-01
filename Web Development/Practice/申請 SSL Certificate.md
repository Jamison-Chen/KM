# 手動申請

https://medium.com/@clu1022/903834f1ac5f

#TODO 

# 使用 Python 套件自動申請

這裡會使用到 Let's Encrypt (CA) 進行免費簽署。

### Step1: 安裝必要套件

```bash
sudo apt-get update
sudo apt-get install certbot
sudo apt-get install python3-certbot-nginx
```

### Step2: 申請 SSL/TLS 憑證

假設我要為 my-domain.com 以及 www.mydomain.com 兩個網域申請憑證：

```bash
sudo certbot --nginx -d my-domain.com
```

若想要一次申請多個網域，則可以寫多個 `-d`。

回答一些問題後，就會出現以下訊息：

```plaintext
Account registered.
Requesting a certificate for my-domain.com

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/my-domain.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/my-domain.com/privkey.pem
This certificate expires on 2024-05-25.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

Deploying certificate
Successfully deployed certificate for my-domain.com to /etc/nginx/sites-enabled/default
Congratulations! You have successfully enabled HTTPS on https://my-domain.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

現在會在 /etc/nginx/sites-available/ 底下的 server block config file 中看到多出了一些關於 port 443 還有憑證位置的內容。

### Step4: Test config files & Reload Nginx

```bash
sudo nginx -t && sudo nginx -s reload
```

這樣就大功告成了，現在你的網站已經可以透過 https 來取得連線了！

>[!Note]
>由 Let's Encrypt 簽署的憑證會在 90 天後到期，但 certbot 有幫我們在背景設定一個定時 renew 憑證的 process。

>[!Note]
>向 Let's Encrypt 申請 SSL 憑證是有 rate limit 的。

### 參考資料

- <https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/>
