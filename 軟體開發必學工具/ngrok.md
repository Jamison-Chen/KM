一般來說，如果我們要將自己家裡的電腦當做 server 提供外網使用者連線，必須要在家裡的 router 設定 [[Port Forwarding]]，然後調整電腦的防火牆設定以允許外部連線。

而 ngrok 是一個讓你可以不用進行上述動作就將 local server 暴露到外網的服務。

![[how-ngrok-works.png]]

### 安裝

[5 分鐘完成 ngrok 設定](https://medium.com/life-after-hello-world/6cedab20bc21)

### 啟動

```bash
ngrok http <LOCAL_PORT>
```

# 官方資源

- [GitHub](https://github.com/inconshreveable/ngrok)
- <https://ngrok.com/>
