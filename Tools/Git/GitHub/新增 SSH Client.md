#SSH 

### Step 1: 確認 Client 上有安裝 Git

[[L2 - Git 安裝與設定|教學]]

### Step2: 新增 SSH Key

[[SSH 常用指令#產生 SSH Key|教學]]

### Step3: 將 SSH Key 加到 GitHub

- Step3-1: 複製 `<key_name>`.pub 檔中的內容（即 public key）
- Step3-2: 登入 GitHub，到 Settings > SSH and GPG keys 點選 New SSH key

### Step4: 測試你的 Key

```bash
ssh -T git@github.com
```

如果你看到類似下面這樣的訊息，代表你已成功新增 SSH client 至 GitHub：

```plaintext
Hi! You've successfully authenticated, but GitHub does not provide shell access.
```

Done!
