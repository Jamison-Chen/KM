# Containerization

Containerization（容器化）指的是「==將應用程式運行時所需的 OS、runtime、code、dependencies 打包==」的動作，目的是讓應用程式可以快速地在各式各樣的機器上被建置並開始運行。

### 優點

- 可以快速建置環境，有利於縮短 dev(elopment) 與 op(eration) 兩個角色間的距離
- 可以將多個不同的應用程式各自打包並運行在同一台機器上，這些應用程式的環境相互獨立，不會影響彼此

Docker 是一個提供 containerization 相關服務的平台，Docker 所制定的關於 containerization 的規則已經成為目前的通用標準。開發者透過撰寫 **[Dockerfile](</Tools/Docker/2 - How to Write a Dockerfile?.md>)** 來設定要建置什麼樣的環境；用 **Docker engine** 來建置與運行環境；並且可以將建置好的環境上傳到雲端 (**[DockerHub](</Tools/Docker/3 - DockerHub.md>)**)。

# Image & Container

#TODO 

# Container vs. Virtual Machine

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/container-vs-virtual-machine.png>)

>[!Note]
>Container 與 VM 可以同時並存，換個話說，一個機器上可以有多個 VMs，一個 VM 中可以運行多個 containers。

# Docker Engine、containerd 與 runc 的關係
