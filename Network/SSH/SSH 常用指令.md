#SSH

# 連線 Remote Server

```bash
ssh [OPTIONS] {USERNAME}@{HOSTNAME} [-p {PORT}]
```

其中 `{USERNAME}` 指的是一個已存在於 server 上的使用者的名稱；`{HOSTNAME}` 可以是 server 的 IP address 或 domain name，若 client 與 server 處在同一個 [NAT](</Network/IP & IP Address.md#NAT>) router 後面，則 `{HOSTNAME}` 應為 local IP address，否則應為 public IP address。

若要連線的不是預設的 port 22，則需要 `-p` option 來聲明。

若有找到指定 IP address 以及指定 user，則進入 Authentication 階段。

**常用的 Options**

- `-v`：將 client 與 server 溝通的過程 stdout
- `-J {JUMP_SERVER}`：當要連線的服務只能透過特定 server 做為窗口／跳板（又被稱為 bastion host 或 jump server）聯繫時，`-J` option 可以讓 client 直接跳到最終要連線的 server，省去在 jump server 上額外輸入 ssh 指令的動作

    ```bash
    ssh -J root@{JUMP_SERVER} root@{MAIN_SERVER}
    ```

- `-A`：使用 [SSH Agent Forwarding](</Network/SSH Agent Forwarding.md>)
- `-D`：使用 [Dynamic Port Forwarding](</Network/SSH Tunneling.md#Dynamic Port Forwarding>)

# 產生 SSH Key

```bash
ssh-keygen [-t {ALGO} [-b {BIT_LENGTH}]] [-f {PATH_TO_FILE}]
```

產生一對 public-private key pair，可以選擇不同的加密演算法，包括 rsa, dsa, ecdsa 與 ec25519。

`-t` option 用來選擇加密演算法，可選的選項包括 rsa, dsa, ecdsa 與 ed25519，預設為 rsa，但 rsa 與 dsa 現在已經普遍被認為不夠安全了。

若選擇使用 rsa 或 ecdsa 做為加密演算法，則可以另外使用 `-b` option 選擇 key 的長度，長度越長越安全，但並不是任何長度都可以，以下提供他們的長度選項（單位為 bit，故要除以 8 才是文字的長度）：

- **rsa**: 1024, 2048 *(recommended)*, 4096 *(better)*
- **ecdsa**: 256, 384, 521 *(recommended)*

`-f` option 用來聲明產生的 key 儲存為檔案後要叫做什麼名字，以及要存在哪裡。若不提供，則預設為存在 `~/.ssh`，預設檔名為 "`id_` + *演算法名稱*"（比如 `id_rsa`）。檔案名稱無須副檔名，此指令執行完畢後會產生兩個同名的檔案，分別是 public key 以及 private key，儲存 public key 的那個檔案會被加上 `.pub` 副檔名。

e.g.

```bash
ssh-keygen -t ecdsa -b 521 -f ~/Desktop/id_test
```

輸入指令後會被要求設定 passphrase，也可以不設定。passphrase 用途是防止 private key 被盜用，因為之後使用 private key 時都會被要求輸入 passphrase。

# 啟動 [SSH Agent](</Network/SSH 基本概念.md#SSH Agent>)

```bash
ssh-agent
```

# 攜帶／卸下 SSH Keys

可以用指令來控制 SSH agent 要攜帶哪些 keys，以及更改 SSH agent 要用哪個白名單來判斷一個 host 是否是信任的 host。

### 攜帶一個新 Key

```bash
ssh-add [{PATH_TO_FILE_OF_PRIVATE_KEY}]
```

若不給 `{PATH_TO_FILE_OF_PRIVATE_KEY}`，則預設加入 `~/.ssh/id_rsa`, `~/.ssh/id_ecdsa`, `~/.ssh/id_ecdsa_sk`, `~/.ssh/id_ed25519`, `~/.ssh/id_ed25519_sk`, `~/.ssh/id_dsa` 所有 keys。

### 列出所有已攜帶的 Keys

```bash
ssh-add -l
```

### 卸下的指定的 Key

```bash
ssh-add -d {PATH_TO_FILE_OF_PRIVATE_KEY}
```

### 卸下所有 Keys

```bash
ssh-add -D
```

### 設定要用哪個檔案作為信任的 Hosts 的白名單

```bash
ssh-add -H {PATH_TO_WHITELIST_FILE}
```
