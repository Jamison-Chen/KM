# Containerization

Containerization（容器化）指的是「==將應用程式運行時所需的 OS、runtime、code、dependencies 打包==」的動作，目的是讓應用程式可以快速地在各式各樣的機器上被建置並開始運行。

### 優點

- 可以快速建置環境，有利於縮短 dev(elopment) 與 op(eration) 兩個角色間的距離
- 可以將多個不同的應用程式各自打包並運行在同一台機器上，這些應用程式的環境相互獨立，不會影響彼此

Docker 是一個提供 containerization 相關服務的平台，Docker 所制定的關於 containerization 的規則已經成為目前的通用標準。開發者透過撰寫 **[Dockerfile](</Tools/Docker/2 - How to Write a Dockerfile?.md>)** 來設定要建置什麼樣的環境；用 **Docker engine** 來建置與運行環境；並且可以將建置好的環境上傳到雲端 (**[DockerHub](</Tools/Docker/4 - DockerHub.md>)**)。

# Image & Container

### Image

Image 就像是一個應用程式環境的 snapshot，這個 snapshot 記錄了某個時刻下有哪些已安裝的套件、環境變數、file system，用來建立一個具有該環境的 container。

- Image 是根據 Dockerfile 來建立 (build) 的，所以使用者透過撰寫 Dockerfile 來設定要建立什麼樣的 image
- Image is ==readonly==, so when an image is built, it does not change.

### Container

Container 是一個根據 image 建立出來的環境，一個 host 上可以運行多個 containers，containers 之間互不干擾。

### Bundle

要在 host 上運行一個 container 所需要用到的所有檔案會被打包成一個 directory 放在 host OS 中，這個 directory 就是一個 bundle。

# Container vs. Virtual Machine

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/container-vs-virtual-machine.png>)

#TODO 

>[!Note]
>Container 與 VM 可以同時並存，換句話說，一個機器上可以有多個 VMs，一個 VM 中可以運行多個 containers。

# Multi-Container Application

一個完整的應用程式通常會包括 application code、database、reverse-proxy server 等多個 components（詳見[這篇](</System Design/Backend Web Architecture.md>)），其中一種做法是只建立一個 container 然後把所有東西都放在裡面，但這樣做的話會有一些缺點：

- 無法針對單一 component 進行 scaling，只能整個應用程式一起 scaling
- 無法針對單一 component 進行 rebuild image
    - 依照 Docker 的運作方式，rebuild image 時，偵測到須要 rebuild 的第一行後，後續所有步驟都須要 rebuild

因此，比較好的做法是將不同 component 拆成獨立的 container，比如一個專門運行 application code 的 container、一個 database 專用的 container、一個 reverse-proxy 專用的 container 等，然後再用 **Docker Compose** 或 **Kubernetes** 這類 orchestration tool 來管理這些 containers。

- **Docker Compose** is a tool for defining and running multi-container applications ==on a single host==.
- **Kubernetes** can manage containers deployed ==across multiple nodes (hosts)==.

# The Architecture of Docker

在 Docker 平台中，從最接近使用者的表層介面應用程式到靠近 OS 的底層程式，分別有 Docker engine、containerd 與 runc 這些元件來實現容器化：

### Docker Engine

使用者透過 [[Docker CLI]] 來操控 Docker engine，進行 "build images"、"run containers" 等動作。

### containerd

是 Docker engine 的核心、用來管理 images 與 containers 的背景程式 (daemon)。

### runc

是實際運行 container 時所用的 runtime，負責直接與 host 的 OS 溝通。containerd 透過 shim 與 runc 溝通。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/docker-architecture.png>)

# 參考資料

- <https://www.docker.com/resources/what-container/>
- <https://accenture.github.io/blog/2021/03/18/docker-components-and-oci.html>
