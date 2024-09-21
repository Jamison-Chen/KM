#SSH

SSH 為 Secure Socket Shell 的縮寫，是一種網路通訊協定，主要功能是：

>在 A、B 兩裝置都開幾且連上網的情況下，讓使用者可以透過 A 裝置 (SSH client) 遠端登入／存取／操縱 B 裝置 (SSH server)。

- SSH server 與 client 預設皆使用 ==port 22== (TCP port)。
- SSH 會將 client 與 server 間傳遞的訊息加密，因此即使 client 與 server 連上的網路不安全，兩個裝置也可以安全地溝通，這點是其他類似工具（如 Telnet 與 rlogin）所欠缺的。

# 從建立連線到結束連線

```mermaid
flowchart TD
    start((Start))
    id0{Client 是否<br/>認識 Server}
    id1{是否信任}
    id2{是否成功}
    id3{是否通過}
    id4((End))
    start --> HandShake
    HandShake --> id0
    id0 --True--> KeyExchange
    id0 --False--> HumanCheck
    HumanCheck --> id1
    id1 --yes--> KeyExchange
    id1 --no--> id4
    KeyExchange --> id2
    id2 --True--> Authentication
    id2 --False--> id4
    Authentication --> id3
    id3 --True--> ChannelOpened
    id3 --False--> id4
    ChannelOpened --> id4
```

# Hand Shake

這是 client 向 server 發出連線請求時的第一個環節，在這個環節中，server 會將自己的 public key (host key) 傳給 client。

Client 會希望自己準備連上的 server 是值得信任的，因此 client 會有一個白名單 (~/.ssh/known_hosts)，這個白名單會記錄信任（連線過）的 server 的 IP 與 host key。

當 client 使用 terminal 嘗試連線一個不存在於 ~/.ssh/known_hosts 的 server 時，terminal 會跳出以下訊息：

```plaintext
The authenticity of host '<ip>' can't be established.
ECDSA key fingerprint is <key>.
Are you sure you want to continue connecting (yes/no)?
```

若輸入 `yes`， 則 client 會新增一筆 IP 與 host key 於 ~/.ssh/known_hosts，這樣下次連線同一台 server 時就不會跳出相同的提示了。

Server 的 host key 通常會在 install SSH server 時自動產生，且不同演算法的版本都各有一份，會存在 /etc/ssh/ 底下，可以重新生成，只是當 SSH server 換 key 時，client 須重新決定是否信任這個 host key。

# Key Exchange

```mermaid
sequenceDiagram
    autonumber
    Client->>Server: 提供自己支援的 SSH 協定版本有哪些
    Server->>Client: 回傳一個可接受的協定版本、產生 session id 並傳送
    Client->>Server: 提供自己偏好的對稱式加密演算法與雜湊演算法
    Server->>Client: 回傳一個可接受的對稱式加密演算法與雜湊演算法
    Server->>Server: 使用 session id 與其他共同<br/>的資訊產生 Shared Secret Key
    Client->>Client: 使用 session id 與其他共同<br/>的資訊產生 Shared Secret Key
```

上方流程圖中，產生 shared secret key 的演算法叫做 [[Diffie-Hellman Key Exchange Algorithm.draft|Diffie-Hellman Key Exchange Algorithm]]，client 與 server 不用將 secret key 傳給對方就可以得到一模一樣的 secret key。

由於每次的 SSH session 都有唯一的 session id，因此每一次的 SSH session 都會產生出不同的 shared secret key。

# SSH 為什麼安全？

SSH 幾乎把所有可以使用的加密機制都用了一輪，包括 asymmetric encryption、symmetric encryption 以及 hashing，以下將分別介紹他們的使用場景：

- Asymmetric encryption 主要用在 key exchange

- 當雙方產生 shared secret key 後，往後的溝通都使用 symmetric encryption

- Hashing

    雙方通訊時的每則訊息除了會被對稱加密以外，還會額外對訊息計算出一個 hash value（hash value 不會被加密），收到訊息的一方將解密完的訊息丟進相同的 hash function 計算出的 hash value 應該要與送來的 hash value 相同，這可以用來確保資訊沒有被篡改。

# 各種 SSH Authentication 的方法

SSH client 連線到 SSH server 時都須要登入 server，登入的方式有很多，也可以疊加使用，以下將逐一介紹（設定方式請見 [#sshd_config 中的常用設定](</./Network/SSH 基本概念.md#sshd_config 中的常用設定>)）：

### Password Authentication

當 client 要求連線時，要求其輸入欲連線的 user password，就和直接在 server 登入做的事一樣。

### Host-Based Authentication

在 server 上設定允許連線的 IP address 與 hostname 白名單（寫在 /etc/ssh/sshd_config 中），可以使用 wildcard，只有透過被允許的 IP address 或 hostname 要求的連線才會被允許。

### Public-Key Authentication

這個方法比前面兩者來的安全，主要分為以下兩個環節：

1. SSH client 讓自己被記錄於 SSH server 的白名單（~/.ssh/authorized_keys）中

    ```mermaid
    sequenceDiagram
        autonumber
        Client->>Client: 產生 public-private key pair
        Client->>Server: 使用各種管道將 public key 交給 server
        Server->>Server: 將 client 的 public key 寫進白名單中<br/>(~/.ssh/authorized_keys)
    ```

2. SSH client 向 SSH server 請求連線

    ```mermaid
    sequenceDiagram
        autonumber
        Client->>Server: 拿著 public key 發送 Connection Request
        Server->>Server: 隨機產生一段訊息<br/>並用 client 的 public key 加密
        Server->>Client: "Challenge" the client
        Client->>Client: 使用對應的 private key 解密
        Client->>Client: 將解密的結果結尾加上 session id<br/>然後用一個雙方約定好的 hash<br/>function 計算出一個 hash value
        Client->>Server: 回傳 hash value
        Server->>Server: 將原本的隨機訊息結尾也加上<br/>session id，然後也用雙方約定好的<br/>hash function 計算出 hash value
        Server->>Client: 若結果相符則允許連線，否則拒絕連線
    ```

Client 在產生 key 時可以額外設定一個 passphrase，往後重新連線至 server 時，除了要有 private key，還會被要求輸入 passphrase，這可以進一步提高安全性，比如當別人使用你做為 client 的電腦時，就會因為不知道 passphrase 而無法連線至 server。

### Certificate-Based Authentication

Certificate-Based Authentication 是 Public-Key Authentication 的變體，因為有公正第三方（Certificate Authority, CA）認證所以更安全，但設定起來也比較麻煩，主要可分為以下三個環節：

1. SSH server 向信任的 CA 索取 public key

    ```mermaid
    sequenceDiagram
        autonumber
        Server->>CA: 要求 CA public key
        CA->>Server: 回傳 public key
        Server->>Server: 將 CA public key<br/>寫進 SSH server 設定檔中
    ```

2. SSH client 要求相同的 CA 核發並簽署憑證

    ```mermaid
    sequenceDiagram
        autonumber
        Client->>Client: 產生 public-private key pair
        Client->>CA: 發送 Certificate Signing Request (CSR)<br>須提供 public key, client name, email 等
        CA->>CA: 檢查拿到的 client 資訊<br/>沒問題就核發憑證<br/>並使用 CA private key 簽署
        CA->>Client: 回傳簽署後的憑證（通常是 .pem 檔）
    ```

3. SSH client 向 SSHsServer 請求連線

    ```mermaid
    sequenceDiagram
        autonumber
        Client->>Server: 提供經簽署的憑證（.pem）
        Server->>Server: 嘗試使用 CA public key 解密<br/>若可以解密則代表 client<br/>有經信任的 CA 認證過<br/>解密後可以得到 client 的 public key<br/>
        Server->>Server: 隨機產生一段訊息<br/>並用 client 的 public key 加密
        Server->>Client: Challenge the client
        Client->>Client: 使用 private key 解密
        Client->>Client: 將解密的結果結尾加上 session id<br/>然後用一個雙方約定好的 hash<br/>function 計算出一個 hash value
        Client->>Server: 回傳 hash value
        Server->>Server: 將原本的隨機訊息結尾也加上<br/>session id，然後也用雙方約定好的<br/>hash function 計算出 hash value
        Server->>Client: 若結果相符則允許連線，否則拒絕連線
    ```

    這個方法透過「第三方認證」取代 Public-Key Authentication 中「將 Client 的 Public Key 手動加入 Server 的白名單中」這個動作。

還有其它較少見的認證方式，比如 Keyboard-Interactive Authentication 與 GSSAPI Authentication，此處不詳述。

# 如何成為 SSH Server？

### Linux

- Step1: 安裝 openssh-server

    ```bash
    sudo apt-get install openssh-server
    ```

- Step2: 調整設定檔（/etc/ssh/sshd_config）

    ```bash
    # 開啟設定檔
    sudo nano /etc/ssh/sshd_config
    
    # 將 `#Port 22` 這行取消註解，以允許 SSH connection
    
    # 可以順便改其他設定，比如是否允許 Password Authentication
    ```

- Step3: 重啟 openssh-server

    ```bash
    sudo systemctl restart sshd
    ```

>[!Note]
>在 /etc/ssh/ 中，除了 sshd_config 外，還有另一個長得很像的檔案叫 ssh_config，前者是用來設定 SSH server，後者則是用來設定 SSH client。

### MacOS

只須至 System Settings > General > Sharing，然後將 Remote Login 選項開啟，client 即可連線，如下圖所示：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/mac-os-open-remote-login.png>)

> [!Note]
> MacOS 也是使用 sshd_config 來設定 SSH server，只是不需要額外將 `#Port 22` 取消註解就可以提供連線。

---

### `sshd_config` 中的常用設定

- 防止 SSH client 透過「輸入密碼」的方式登入

    ```plaintext
    PasswordAuthentication no
    KbdInteractiveAuthentication no
    ```

- 設定 certificate authority 的 public key

    ```plaintext
    TrustedUserCAKeys /etc/ssh/ca.pub
    ```

### 重啟 SSH Server

當有更動到 sshd_config 的內容時，就必須重啟 SSH server：

- Linux

    ```bash
    sudo systemctl restart sshd
    ```

- MacOS

    ```bash
    sudo launchctl unload /System/Library/LaunchDaemons/ssh.plist
    sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plis
    ```

# 如何成為 SSH Client？

MacOS 與 Linux 無須額外安裝程式即可扮演 SSH client，Windows 則必須至 Settings > Apps & Features > Manage optional features 找到 SSH client 並將其安裝。

### SSH Agent

SSH agent 是運行在 client side 的背景程式，其功能包括：

1. 攜帶 private key（暫存在 RAM）
2. 檢查準備連線的 host 是否是信任的 host

SSH agent 還有一個功能，就是如果 client 的 private key 需要輸入 passphrase，則只須在「指定攜帶該 key (`ssh-add`) 的時候」輸入 passphrase，後續 SSH agent 就會記住這個 passphrase（一樣是存在 RAM）並在需要用到 private key 的時候自動幫你輸入 passphrase。

啟動 SSH agent 的指令為：`ssh-agent`（Linux OS 中通常開機時會自動開啟）；可以用 `echo "$SSH_AUTH_SOCK"` 來確認 SSH agent 是否為開啟狀態。

### SSH Client 設定檔

在 SSH client 端可以建立一個叫做 config 的設定檔在 ~/.ssh/ 底下，這樣可以免去每次執行連線 SSH server 時都要加上一堆 options 與 arguments，示範如下：

```plaintext
Host myserver
    Host 192.168.50.88
    User jamison
    Port 2345
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa

Host <NICKNAME>
    <OPTION> <VALUE>
    ...
```

有了這個 config file，只要執行 `ssh myserver` 就等同於執行了以下動作：

```bash
ssh-add ~/.ssh/id_rsa
ssh jamison@192.168.50.88 -p 2345
```

> [!Info]
> 可以在 `<NICKNAME>` 的部分使用 wildcard (`*`)，將某些設定套用到所有 hosts。

# 其它進階概念

- [SSH Agent Forwarding](</Network/SSH Agent Forwarding.md>)
- [SSH Tunneling](</Network/SSH Tunneling.md>)
- [SCP 檔案傳輸](</Network/檔案傳輸.md#SCP>)

# 參考資料

- <https://www.youtube.com/watch?v=qWKK_PNHnnA>
- <https://www.hostinger.com/tutorials/ssh-tutorial-how-does-ssh-work>
- <https://www.ssh.com/academy>
