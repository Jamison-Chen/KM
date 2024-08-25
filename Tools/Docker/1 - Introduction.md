### 📄 [官方文件](https://docs.docker.com/guides/)

# Containerization

Containerization（容器化）指的是「將應用程式運行時所需的 OS、runtime、code、dependencies 打包」的動作，目的是讓應用程式可以快速地在各式各樣的機器上被建置並開始運行。

### 容器化的優點

- 可以快速建置環境，有利於拉近 dev(elopment) 與 op(eration) 兩個角色間的距離
- 可以將多個不同的應用程式分別容器化並運行在同一台 host 上，這些應用程式的環境相互獨立，不會影響彼此

Docker 是一個提供 containerization 相關服務的平台，Docker 所制定的關於 containerization 的規則已經成為目前的通用標準。開發者透過撰寫 **[Dockerfile](</Tools/Docker/4 - Dockerfile.md>)** 來設定要建置什麼樣的環境；用 **Docker engine** 來建置與運行環境；並且可以將建置好的環境上傳到雲端 (**[Docker Hub](</Tools/Docker/5 - Docker Hub.md>)**)。

# Image & Container

>[!Info]
>關於 image 與 container 的完整介紹，請看[這篇](</Tools/Docker/3 - Image & Container.md>)。

```mermaid
flowchart LR
Dockerfile --build--> Image
Image --build--> Container
```

### Image

Image 又叫做 container image，就像是一個應用程式環境的 snapshot，這個 snapshot 記錄了某個時刻下有哪些已安裝的套件、環境變數與 file system 等，是根據 Dockerfile 建立 (build) 出來的。

### Container

Container 是一個根據 image 建立 (build) 出來的環境，一個 host 上可以運行多個 containers，containers 之間互不干擾。

# Container vs. Virtual Machine

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/container-vs-virtual-machine.png>)

一個 host 上所有 containers 都共用 host 的硬體資源與 [OS kernel](</Operating System/Kernel.md>)，所以即使 container 內可以有自己的 OS，但那也只包含讓應用程式可以正常運行的基本 libraries，不是完整的 OS；virtual machine (VM) 則裝有完整的 OS，所以不同 VMs 間只會共用 host 的硬體資源。

Docker 使用 host's OS kernel 的好處是這讓 container 變得相對輕量，也縮短了啟動 container 所需的時間。

Container 與 VM 可以並存，換句話說，一個機器上可以有多個 VMs，一個 VM 中可以運行多個 containers。

# Multi-Container Application

一個完整的應用程式通常會包括 application code、database、reverse-proxy server 等多個 components（詳見[這篇](</System Design/Backend Web Architecture.md>)），其中一種做法是只建立一個 container 然後把所有東西都放在裡面，但這樣做的話會有一些缺點：

- 無法針對單一 component 進行 scaling，只能整個應用程式一起
- 無法針對單一 component 的 image 進行 rebuild

因此，比較好的做法是將不同 components 拆成獨立的 containers，比如一個專門運行 application code 的 container、一個 database 專用的 container、一個 reverse-proxy 專用的 container 等，然後再用 **Docker Compose** 或 **Kubernetes** 這類 orchestration tool 來管理這些 containers。

- **Docker Compose** is a tool for defining and running multi-container applications ==on a single host==.
- **Kubernetes** can manage containers deployed ==across multiple nodes (hosts)==.

# The Architecture of Docker

整個 Docker 平台主要可以分為 **client**、**Docker host** 與 **registry** 三個 components。使用者透過 client 操控 Docker host；Docker host 必要時會到 registry 下載 image。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/docker-architecture.png>)

### Client

使用者可以透過 [Docker CLI](</Tools/Docker/2 - Docker CLI.md>) 或 REST API 操控 host。

以「列出在 local 運行中的 containers」為例：

- Docker CLI

    ```bash
    docker ps
    ```

- REST API

    ```plaintext
    curl --unix-socket /var/run/docker.sock http://localhost/containers/json
    ```

### Docker Host

Docker host 包括 Docker daemon（ Doker 的核心程式，程式名為 `dockerd`），以及存放 images 與 containers 的 local 空間。

Docker daemon 是 Doker 的核心程式（程式名為 `dockerd`）其負責的工作包括 "pull images"、"build images"、"collect logs" 等，但 ==Docker daemon 不負責運行 container==，它會把有關 container management 的工作交給 `containerd` 來完成。

### Registry

Registry 通常在遠端，主要功能是用來存放 images，分為 [public (Docker Hub)](</Tools/Docker/5 - Docker Hub.md>) 與 private (self-hosted) 兩種。使用者可以把 local 的 images 推上 registry，也可以從 registry 中 pull images 到 local。

>[!Note] Docker Engine
>Client 與 Docker host 會被包成一個叫 Docker engine 的應用程式。

>[!Note] Docker Desktop
>在 macOS 與 Windows 作業系統中，Docker engine 又被額外包了一層皮，叫 [Docker Desktop](https://www.docker.com/products/docker-desktop/)。Docker Desktop 主要是將 Docker engine 與 Dokcer Compose、Kubernetes 等工具整合，並提供 GUI 方便使用者操作。

# OCI

- OCI 是 [Open Container Initiative](https://opencontainers.org/) 這個組織的縮寫
- OCI 致力於打造 open-source 的容器化開發生態
- OCI 也致力於制定容器化開發的通用標準，目前已經有關於 container runtime 的規格書以及 container image 的規格書

# 參考資料

- <https://www.docker.com/resources/what-container/>
- <https://accenture.github.io/blog/2021/03/18/docker-components-and-oci.html>
