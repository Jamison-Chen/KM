### 📄 [官方文件](https://docs.docker.com/guides/)

# Containerization

Containerization（容器化）指的是「將應用程式運行時所需的 OS、runtime、code、dependencies 打包」的動作，目的是讓應用程式可以快速地在各式各樣的機器上被建置並開始運行。

### 容器化的優點

- 可以快速建置環境，有利於拉近 dev(elopment) 與 op(eration) 兩個角色間的距離
- 可以將多個不同的應用程式分別容器化並運行在同一台 host 上，這些應用程式的環境相互獨立，不會影響彼此

# The Architecture of Docker

Docker 是一個提供 containerization 服務的平台，整個 Docker 平台主要可以分為 **client**、**Docker host** 與 **registry** 三個 components，使用者透過 client 操控 Docker host；Docker host 必要時會到 registry 下載 image。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/docker-architecture.png>)

### Client

使用者可以透過 [Docker CLI](</Tools/Docker/2 - Docker CLI.md>)（程式名稱為 `docker`）或 REST API 與 Docker host 溝通。

以「列出在 local 運行中的 containers」為例：

- Docker CLI

    ```bash
    docker ps
    ```

- REST API

    ```plaintext
    curl --unix-socket /var/run/docker.sock http://localhost/containers/json
    ```

    從這個指令可以發現，我們是透過 [[Socket & Port#Unix Domain Socket|Unix domain socket]] 與 Docker 溝通的。

### Docker Host

Docker host 包括 Docker daemon（ Doker 的核心程式，程式名為 `dockerd`），以及存放 images 與 containers 的 local 空間。

Docker daemon 是 Docker 的核心程式（程式名為 `dockerd`）。粗略地說，Docker daemon 負責管理 images、containers、Docker networks 與 Docker volumes，但其實 ==`dockerd` 本身不負責運行 container==，它會把有關 container management 的工作轉交給更底層的程式 (`containerd`) 來完成。

>[!Info]
>關於 Docker daemon 的完整介紹，請看[這篇](</Tools/Docker/6 - Docker Daemon.draft.md>)。

### Registry

Registry 通常在遠端，主要功能是用來存放 images，分為 [public (Docker Hub)](</Tools/Docker/5 - Docker Hub.draft.md>) 與 private (self-hosted) 兩種。使用者可以把 local 的 images 推上 registry，也可以從 registry 中 pull images 到 local。

>[!Note] Docker Engine
>Client 與 Docker host 會被包成一個叫 Docker engine 的應用程式。

>[!Note] Docker Desktop
>[Docker Desktop](https://www.docker.com/products/docker-desktop/) 將 Docker engine 與 Dokcer Compose、Kubernetes 等工具整合，且有 GUI，通常在 Windows 或 macOS 系統中都會裝 Docker desktop 而不會只裝 Docker engine。

# Image & Container

>[!Info]
>關於 image 與 container 的完整介紹，請看[這篇](</Tools/Docker/3 - Image & Container.draft.md>)。

開發者透過撰寫 [Dockerfile](</Tools/Docker/4 - Dockerfile.draft.md>) 來設定要建置什麼樣的環境；用 Docker engine 根據 Dockerfile 來堆疊出 image，最後再根據 image 建置 container 並運行之。

```mermaid
flowchart LR
Dockerfile --build--> Image
Image --build--> Container
```

### Image

- Image 就像是一個應用程式環境的 snapshot，這個 snapshot 記錄了某個時刻下有哪些已安裝的套件、環境變數與 file system 等
- Dockerfile 就像是食譜，它告訴 Docker daemon 要如何建立 (build) 出開發者想要的 image
- Image 以「層」為單位，多個 images 可以堆疊出另一個更大的 image

### Container

- Container 是一個根據 image 建立 (build) 出來的環境，你可以對它進行 "create"、"start"、"stop"、"delete" 等操作
- 一個 host 上可以運行多個 containers，containers 之間互不干擾，但你也可以建立一個網絡讓多個 containers 互聯
- 可以為 container 配置儲存空間 (volume)

# Container vs. Virtual Machine

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/container-vs-virtual-machine.png>)

一個 host 上所有 containers 都共用 host 的硬體資源與 [OS kernel](</Operating System/Kernel.draft.md>)，所以即使 container 內可以有自己的 OS，但那也只包含讓應用程式可以正常運行的基本 libraries，不是完整的 OS；virtual machine (VM) 則裝有完整的 OS，所以不同 VMs 間只會共用 host 的硬體資源。

Docker 使用 host's OS kernel 的好處是這讓 container 變得相對輕量，也縮短了啟動 container 所需的時間。

Container 與 VM 可以並存，換句話說，一個機器上可以有多個 VMs，一個 VM 中可以運行多個 containers。

# Multi-Container Application

一個完整的應用程式通常會包括 application code、database、reverse-proxy server 等多個 components（詳見[這篇](</System Design/Backend Web Architecture.md>)），其中一種做法是只建立一個 container 然後把所有東西都放在裡面，但這樣做的話會有一些缺點：

- 無法針對單一 component 進行 scaling，只能整個應用程式一起
- 無法針對單一 component 的 image 進行 rebuild

因此，比較好的做法是將不同 components 拆成獨立的 containers，比如一個專門運行 application code 的 container、一個 database 專用的 container、一個 reverse-proxy 專用的 container 等，然後再用 **Docker Compose** 或 **Kubernetes** 這類 orchestration tool 來管理這些 containers。

- **Docker Compose** is a tool for defining and running multi-container applications ==on a single host==.
- **Kubernetes** can manage containers deployed ==across multiple nodes (hosts)==.

# OCI

- OCI 是 [Open Container Initiative](https://opencontainers.org/) 這個組織的縮寫
- OCI 致力於打造 open-source 的容器化開發生態
- OCI 也致力於制定容器化開發的通用標準，目前已經有關於 container runtime 的規格書以及 container image 的規格書

# 其它

- Docker 的核心程式使用 Go 寫的
- Docker 之所以可以讓 containers 間互相獨立，主要是透過「為每個 container 建立專屬的 namespaces」來做到

# 參考資料

- <https://docs.docker.com/get-started/docker-overview/>
- <https://www.docker.com/resources/what-container/>
- <https://accenture.github.io/blog/2021/03/18/docker-components-and-oci.html>
