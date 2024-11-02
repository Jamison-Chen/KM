一般家庭用的網路都會使用 [NAT](</Network/IP & IP Address.md#NAT>)，以解決 IPv4 不夠用的問題，所以如果我們要將自己家裡的電腦當做 server 提供外網使用者連線，必須要在家裡的 router 設定 [[Port Forwarding]]，然後調整電腦的防火牆設定以允許外部連線。

而 ngrok 是一個讓你可以不用進行上述動作就將 local server 暴露到 Internet 的 application。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/how-ngrok-works.png>)

# 安裝

### On MacOS

```bash
# Step1: install ngrok
brew install ngrok/ngrok/ngrok

# Step2: add your authtoken to the default ngrok.yml
ngrok config add-authtoken {YOUR_AUTH_TOKEN}
```

- Ngrok 設定檔位置: ~/Library/Application Support/ngrok/ngrok.yml

# 啟動

```sh
ngrok http <LOCAL_PORT>
```

# 官方資源

- [GitHub](https://github.com/inconshreveable/ngrok)
- <https://ngrok.com/>
