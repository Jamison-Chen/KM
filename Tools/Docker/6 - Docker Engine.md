#TODO 

### containerd

負責 "pull/download image from a registry"、"manage containers' lifecycle"。實際上 "run container" 的工作也不是由 `containerd` 負責，而是透過更底層的 `runc`，`containerd` 透過 `shim` 與 `runc` 溝通。

### runc

`runc` 是實際運行 container 時所用的 runtime，負責直接與 host 的 OS 溝通。

```mermaid
flowchart TD
id0(Docker Desktop)
id1(Docker Engine)
id2(containerd)
id3(shim)
id4(shim)
id5(shim)
id6(runc)
id7(runc)
id8(runc)
id9{{container}}
id10{{container}}
id11{{container}}
id0 <--> id1
id1 <--> id2
id2 <--> id3
id2 <--> id4
id2 <--> id5
id3 --> id6
id4 --> id7
id5 --> id8
id6 --> id9
id7 --> id10
id8 --> id11
```

>[!Info]
>runc 是 OCI 的第一個 open source project。
