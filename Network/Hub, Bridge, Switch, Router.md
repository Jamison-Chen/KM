# Hub

一個 hub 會有多個 ports，一個 port 供一個 host 使用，當有其中一個 host 發出訊號時，hub 會將這個訊號 ==broadcast 給其他所有 ports 上的 hosts==。

Hub 是屬於 physical layer 的裝置，所以它不會拆開 data-link layer 的 data frame（不會看裡面的 MAC address）。

>[!FAQ] Hub 自己有 MAC address 嗎？
>待查證... #TODO 

### Hub 的缺點

- Broadcast 讓資訊隱蔽性變低
- Broadcast 造成不必要的頻寬浪費
- Hub 通常是 **half-duplex**（一個時間只能有一個裝置在收／發訊息），而 broadcast 使得很容易發生 data collision

# Bridge

一個 bridge 通常只有左右兩個 ports，其最主要的功能是牽起左右兩邊的 **segments**，它可以知道某個 MAC address 是位在左邊或右邊的 port。此外，bridge 通常為 **full-duplex**（一個時間可以有很多裝置在收／發訊息）。

Bridge 是屬於 data-link layer 的裝置，所以它會看 data frame 中的 MAC address。

>[!FAQ] Bridge 自己有 MAC address 嗎？
> #TODO

# Switch

Switch 結合了 hub 和 bridge 的優點：有很多 ports、會用 MAC address 決定 port、full-duplex，也因此現在 hub 與 bridge 幾乎都已被 switch 取代。

Switch 也屬於 data-link layer 的裝置，所以它也會看 data frame 中的 MAC address，其實你可以把 switch 想成「擁有多個 port 的 bridge」。

>[!FAQ] Hub 自己有 MAC address 嗎？
> #TODO

---

上述的 hub、bridge、switch 皆是在一個 Autonomous System (AS) 中工作，接下來要介紹的 router 則可以做到跨 AS 的 routing。

# Router

Router 屬於 network layer 的裝置，所以它不會看 data frame 中的 MAC address

一個 router 會有很多 MAC address

#TODO 

### NAT Router

NAT 是 Network Address Traslation 的縮寫，

#TODO 

**Public IP**

**Local IP**

**Subnet Mask**

# 參考資料

- <https://www.section.io/engineering-education/switch-vs-router-vs-hub/>
- <https://www.youtube.com/watch?v=p6mqb5FCO0g>
