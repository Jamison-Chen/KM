# MAC Address

一台能夠連上網路的裝置 (host) 的 IP address 會因為其所處的 [Subnet vs. Autonomous System](</Network/Subnet vs. Autonomous System.md>) 不同（白話文：連上不同的網路）而不同，比如你的筆電連上家裡網路時跟連上公司網路時的 IP address 就不一樣；而 MAC address 則是跟這台可連網裝置綁定、無論走到哪裡都不變，且也具有唯一性的一串編號。MAC 是 medium access control 的縮寫。

你可以想像 IP address 就像是你的通訊地址，如果你今天搬家了，通訊地址就會換；而 MAC address 就像是你的身分證字號，會跟著你一輩子。

### NIC

一個可連網裝置是因為具有 **NIC**（"network interface controller" or "network interface card"，中文叫「網卡」）才可以連網，而其實 ==MAC address 並不是跟著裝置本身，而是跟著 NIC==，所以如果有裝置擁有不只一個 NIC（比如 router）那它就會有不只一個 MAC address。

MAC address 是由 [IEEE](https://www.ieee.org/) 分配給 NIC 製造商，然後由製造商在製造過程中將其儲存在 NIC 的 ROM (read-only memory) 中，由於 MAC address 是跟著實體的 NIC 的，所以 MAC address 又叫 **physical address**。

早期的 NIC 都是外接在裝置外，但現在大多數可連網裝置都會把 NIC 直接焊接在 mainboard 上，於是 NIC 現在有時也被叫 **LoM** (LAN on mainboard)，而 MAC address 也多了 **burned-in address** 這個別稱。

### MAC Address 的表示方式

一個 MAC address 的長度為 48 bits，這意味著全世界總共可以有 $2^{48}$ 個 MAC addresses，通常會以 16 進制表示，比如 `1A:2B:3C:4D:5E:6F`。

### Address for Data-Link Layer

雖然 MAC address 具有唯一性且不變，可以透過它來精準地指定要溝通的對象，但在 network routing 的過程中，client/server 卻是使用 IP address 而非 MAC address 來指定溝通對象，這是因為 MAC address 是 data-link layer (L2) 所使用的資料，而 network routing 是在 network layer (L3) 進行，根據 [OSI Model](</Network/OSI Model.md>)，上層的裝置不會去看下層 protocol 所使用的資料，所以無法在 network routing 時使用 MAC address 找到要溝通的對象。

那 MAC address 的用途是什麼呢？

### Multiple Access Protocol

當一個要送給你的封包被送到離你最近的 router (first hop router) 後，整個 network layer 的旅程 (routing) 就走完了，接著「從 router 到你的裝置」這段路就是屬於 data-link layer 的工作範圍，而 MAC address 就是 router 用來找到你的根據。但其實嚴格說並不是 router 找到你，而是 router 將封包「廣播」給所有與它連上的裝置，所有收到封包的裝置再看封包上指名的 MAC address 是不是自己，是的話再拆開來看。 

使用這種廣播機制的 L2 protocol 又叫做 **multiple access protocol**，包括：

- 802.3 (Ethernet)
- 802.11 (Wi-Fi)
- 802.15 (Bluetooth)（不是 `router → 裝置`，而是 `裝置 → 裝置`）

而 MAC address 就是用來實現 multiple access protocol 的關鍵。

你可能會好奇：「Router 難道不能記住每個跟他連線的裝置的 MAC address，然後只把封包送給指定的裝置嗎？」

答案是「可以，但只有在特定條件下才可以。」首先如果是無線傳輸（如 802.11/Wi-Fi、802.15/Bluetooth），那絕對只能廣播；==只有在使用有線網路 (802.3/Ethernet) 且 [Network Topology](</Network/Network Topology.md>) 為 star topology 時，才可以由 [switch](</Network/Hub, Bridge, Switch, Router.md#Switch>) 直接根據 MAC address 決定要將封包往哪個 port 送==，其它 topology 都只能廣播。

# ARP

ARP 是一個介於 [network layer](</Network/OSI Model.md#Network Layer (Layer 3)>) 與 [data-link layer](</Network/OSI Model.md#Data-Link Layer (Layer 2)>) 之間的 protocol（到底是屬於哪一層目前有爭議）全名為 address resolution protocol。ARP 的核心即 ARP table，是一個可以透過 IP address 查詢到 MAC address 的表，在 host、[router](</Network/Hub, Bridge, Switch, Router.md#Router>)、[switch](</Network/Hub, Bridge, Switch, Router.md#Switch>) 上都可以看到。

### ARP 之於 DNS

ARP 是一個「可以透過 IP address 查詢到 MAC address 的協定」，就好比 [DNS](</Network/DNS.md>) 是一個「可以透過 domain name 查詢到 IP address 的系統」的概念，但這兩個名詞其實不一樣的地方更多，下面是它們的比較表：

| |DNS|ARP|
|:-:|:-:|:-:|
|Input|Domain name|IP address|
|Output|IP address|MAC address|
|作用範圍|整個 Internet|Local (一個 autonomous system 中)|
|架構|Hierarchical|Flat (一台機器紀錄所有東西)|
|儲存位置|Host、router、DNS server|ARP table (host、switch 與 router 上都有)|

### 查詢本機的 ARP Table

```bash
arp -a
```

Example output:

```plaintext
router.asus.com (192.168.50.1) at 24:4b:fe:35:13:7c on en0 ifscope [ethernet]
```

>[!Note]
>更多與網路相關的指令請見[本文](</Operating System/Shell/與網路相關的指令.md>)。

### ARP 中的特殊 MAC Addresses

##### Broadcast Address

#TODO 

# 參考資料

- <https://en.wikipedia.org/wiki/MAC_address>
- <https://en.wikipedia.org/wiki/Address_Resolution_Protocol>
