#SSH 

### [[2 - 安裝與設定|Step 1: 確認 Client 上有安裝 Git]]

### [Step2: Client 新增 SSH Key](</Network/SSH 常用指令.md#產生 SSH Key>)

### Step3: 將 SSH Key 加到 GitHub

- Step3-1: 複製 .pub 檔（即 public key）中的內容
- Step3-2: 登入 GitHub，到 Settings > SSH and GPG keys 點選 `New SSH key`

### Step4: [SSH Agent](</Network/SSH/SSH 基本概念.md#SSH Agent>) 攜帶 SSH Key

e.g.

```bash
ssh-add ~/.ssh/id_rsa
```

若採用這個方法，則每次重開機時都要重新執行一次這個指令，因為重開機後 SSH agent 會被重啟。若想要一勞永逸，則須將下方設定檔寫進 ~/.ssh/config 中：

```plaintext
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa
```

### Step5: Client Side 測試

在 client 輸入以下指令：

```bash
ssh -T git@github.com
```

如果看到類似下面這樣的訊息，代表已成功新增 SSH client 至 GitHub：

```plaintext
Hi! You've successfully authenticated, but GitHub does not provide shell access.
```
