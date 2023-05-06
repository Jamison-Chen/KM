#SSH 

> [!Info]
> 閱讀本文前，我們預期你已經了解 [[SSH 基本概念]]。

---

SSH Tunneling 又叫做 SSH Port Forwarding，其中又可分為「順向」與「反向」，以下將分別解釋：

# Local Port Forwarding (順向 Tunnel)

Local Port Forwarding 指的是 Client 將自己的某個 port ($P_c$) 映射到 Server 的某個 port ($P_s$)，使得對 `<client-ip>:`$P_c$ 發起的 request 會直接被導向至 `<server-ip>:`$P_s$。

### Pattern

```bash
ssh -L [localhost:]<SSH_CLIENT_PORT>:<DESTINATION_HOST>:<DESTINATION_PORT> <USERNAME>@<SSH_SERVER_HOST>
```

請注意兩件事情：

1. `<DESTINATION_HOST>` 的 "DESTINATION" 指的是實際提供服務的 server；`SSH_SERVER_HOST` 的 "SSH_SERVER" 指的則是 client 使用 SSH 連上的 server，==他們可能是同一台機器，也可能是不同台==

2. `<DESTINATION_HOST>` 應是「對於 SSH Server 而言的位置」，所以當提供主要服務的 server 與 SSH server 是同一台機器時，`DESTINATION_HOST` 應為 `localhost`；而若是兩台不同機器，但都在 NAT 底下，則 `DESTINATION_HOST` 應為 Local IP 而非 Public IP

以下分別用兩張圖來表示提供主要服務的 server 與 SSH server 同一台機器與不同台機器的狀況：

### 一台機器同時是 SSH Server 也是主要服務的 Server

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/ssh-tunnels-1.png>)

---

### SSH Server 只是入口，真正提供服務的 Server 在 NAT 後面

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/ssh-tunnels-2.png>)

# Remote Port Forwarding (反向 Tunnel)

Remote Port Forwarding 指的是 Client 將 Server 的某個 port ($P_s$) 映射到自己的某個 port ($P_c$)，使得對 `<server-ip>:`$P_s$ 發起的 request 會直接被導向至 `<client-ip>:`$P_c$。當 SSH Client 希望由自己做為提供主要服務的 server 並==將服務公開到外部網路==時，就可以透過一個在外部網路的 Gateway server 將流量導向給自己。

> [!Note]
> Gateway Server 之所以叫 Gateway 是因為它的 `/etc/ssh/sshd_config` 設定檔有特別加上 `GatewatPorts yes` 這條設定，若沒有這條設定，則即使反向 Tunnel 被打通，也只有 Gateway Server 自己打 localhost 時的流量會被導向至 SSH Client；有了 `GatewatPorts yes` 才能使其他 clients 打 Gateway Server 的 IP 時，流量也會被導向 SSH Client。

### Pattern

```bash
ssh -R [0.0.0.0:]<SSH_SERVER_PORT>:<DESTINATION_HOST>:<DESTINATION_PORT> <USERNAME>@<SSH_SERVER_HOST>
```

同樣有幾點要注意：

- `<SSH_SERVER_HOST>` 與 `<SSH_SERVER_PORT>` 分別就是 Gateway Server 的 IP 與 port
- "DESTINATION" 指的仍然是實際提供服務的 server
- `<DESTINATION_HOST>` 應是「對於 ==SSH Client== 而言的位置」，所以當提供主要服務的 server 與 SSH client 是同一台機器時，`DESTINATION_HOST` 應為 `localhost`；而若是兩台不同機器，但都在 NAT 底下，則 `DESTINATION_HOST` 應為 Local IP 而非 Public IP

依照 SSH Client 與提供主要服務的 server 是否是同一台機器，Remote Port Forwarding 同樣也可以細分為兩種：

### 一台機器同時是 SSH Client 也是主要服務的 Server

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/ssh-tunnels-3.png>)

### SSH Client 只是入口，真正提供服務的 Server 在 NAT 後面

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/ssh-tunnels-4.png>)

在知道有 Remote Port Forwarding 這招後，你也應該更能體會為什麼 SSH Server 不能隨意給 unauthorized 的 client 連線了，因為如果陌生人可以連上原本提供主要服務的 server，並把 requests 導向自己這裡，那他就可以回覆任何不在 client 預期內的 responses，包括電腦病毒。

# 其它常見操作

### 列出所有正在運做的 SSH Tunnel

```bash
lsof -i -n | egrep '\<ssh\>'
```

### 建立 SSH Tunnel 並在背景運行

```bash
ssh -fNL <PORT>:<HOST>:<PORT> <USER>@<HOST>
```

上面的指令中，`-N` 代表此次的 SSH 連線不會輸入任何 command 到 SSH Server，`-f` 代表將 SSH 連線丟到背景去運作（潛規則：`-f` 一定要搭配 `-N` 一起使用）。

### 停止 SSH Tunnel

如果沒有使用 `-f` 將 SSH 丟到背景運作，那使用鍵盤的 `Ctrl` + `C` 即可停止；但若要關閉在背景運作的 SSH Tunnel，則必須先找出運行 SSH Tunnel 的 Process 的 pid，然後使用 `kill` 指令將其終止：

- Step1: 列出所有 SSH 相關的 Processes

    ```bash
    ps aux | grep ssh
    ```

    這個指令的 output 會因作業系統而有所不同，但一定會有 pid，此時我們要做的就是把要終止的 process 的 pid 複製起來，然後進到 Step2

- Step2: `kill <pid>`

# 同場加映：Dynamic Port Forwarding

#TODO 

# 參考資料

- <https://iximiuz.com/en/posts/ssh-tunnels/>
- <https://johnliu55.tw/ssh-tunnel.html>