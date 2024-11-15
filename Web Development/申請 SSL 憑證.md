#WebDevPractice

# 有哪些解決方案？

- 手動申請
- 自動申請
    - 使用 certbot
    - 使用 acme.sh
- 使用 Caddy
- 使用 CloudFlare

接下來將逐一介紹這些解決方案的實行方法。

# 手動申請

#TODO

# 使用 certbot 自動申請

[certbot](https://certbot.eff.org/) 是一款可以幫我們申請 SSL 憑證與定期更新憑證的套件，它會向 Let's Encrypt（其中一個 certificate authority）請求免費簽署。

### Step1: 安裝必要套件 (On Linux Ubuntu)

```bash
sudo apt-get update
sudo apt-get install certbot
sudo apt-get install python3-certbot-nginx
```

### Step2: 取得並安裝憑證

假設我要為 my-domain.com 申請憑證，且使用的 web server 為 nginx：

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

看到這個訊息就帶表申請到憑證了，certbot 總共幫我們做了兩件事：

- 幫你申請到 SSL 憑證
- 在 /etc/nginx/sites-available/ 底下的 server block config file 中，幫你加上 port 443（https 用的 port）的 config，並填入憑證位置、private key 的位置等

### Step4: Test config files & Reload Nginx

```bash
sudo nginx -t && sudo nginx -s reload
```

Done!

>[!Note] 自動更新憑證
>由 Let's Encrypt 簽署的憑證會在 90 天後到期，但 certbot 有幫我們設定一個定時 auto renew 憑證的 cron job 或 systemd timer。
>
>如果你擔心 auto renew 會失敗，可以 dry run 看看 renew 的指令：
>
>```bash
>sudo certbot renew --dry-run
>```

>[!Warning] Rate Limit
>向 Let's Encrypt 申請 SSL 憑證是有 rate limit 的，所以不要短時間在同一台機器上頻繁地 renew 或重新申請憑證。

>[!Note]
>其它細節請見 [certbot 官方文件](https://certbot.eff.org/)。

# 使用 acme.sh 自動申請

[acme.sh](https://github.com/acmesh-official/acme.sh) 是一個與 certbot 類似，但更輕量的 shell script（甚至稱不上是套件），它也是向 Let's Encrypt 請求憑證。

### Step1: 安裝 acme.sh (On Linux Ubuntu)

```bash
curl https://get.acme.sh | sh -s email={YOUR_EMAIL_ADDRESS}
```

安裝的過程中會發生三件事：

- Create and copy `acme.sh` to your home directory: `~/.acme.sh/`.
    - 之後申請到的憑證都會放在這裡
- Create alias: `acme.sh=~/.acme.sh/acme.sh`.
- Create a daily cron job to check and renew the certs if needed.

### Step2: Reload the Shell

```bash
exec "$SHELL"
```

這個步驟的目的是讓剛剛設定的 alias 生效。

### Step3: 申請並安裝憑證

假設我要為 my-domain.com 申請憑證，且使用的 web server 為 nginx：

```bash
acme.sh --install-cert -d my-domain.com -w /var/www/html --reloadcmd "service nginx force-reload"

# or 

# only for root user
acme.sh --install-cert --nginx -d my-domain.com --reloadcmd "service nginx force-reload"
```

- 若想要一次申請多個網域，則可以寫多個 `-d`
- 執行此指令前，請先確保目前的 user 對 webroot (/var/www/html/) 有 [write 權限](</Operating System/Shell/7 - 與 Permission 相關的指令.md>)
    - acme.sh 不能搭配 `sudo` 使用，所以你必須直接切換成有權限的 user

Done!

>[!Note] 自動更新憑證
>acme.sh 也會幫我們設定一個定時 auto renew 憑證的 cron job。
>
>你也可以抖手動更新憑證：
>
>```bash
>acme.sh --renew -d my-domwin.com --force
>```

>[!Note]
>其它細節請見 [acme.sh 官方文件](https://github.com/acmesh-official/acme.sh)。

# 使用 Caddy

[Caddy](https://caddyserver.com/) 是一款會幫你處理好所有 SSL/TLS 憑證問題的 web server。

#TODO

# 使用 CloudFlare

CloudFlare 除了提供 CDN 服務外，也提供 SSL 加密服務。其提供加密服務的方式其實就是擋在 server 前面扮演 reverse proxy 的角色。

使用 CloudFlare 還有一個額外的好處是它內建了防禦 [DDoS attack](</Network/DDoS Attack.canvas>) 的機制。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cloudflare-ssl-service.png>)

# 參考資料

- [各種 SSL/TLS 解決方案](https://ithelp.ithome.com.tw/articles/10209276)
- [關於憑證的維運](https://medium.com/@clu1022/903834f1ac5f)
- [Using Free SSL/TLS Certificates from Let's Encrypt with Nginx](https://www.f5.com/company/blog/nginx/using-free-ssltls-certificates-from-lets-encrypt-with-nginx)
- [Certbot 官方網站](https://certbot.eff.org/)
- [Acme.sh 官方文件](https://github.com/acmesh-official/acme.sh)
- [Caddy 官方網站](https://caddyserver.com/)
- [CloudFlare 官網簡介](https://www.cloudflare.com/zh-tw/learning/what-is-cloudflare/)
