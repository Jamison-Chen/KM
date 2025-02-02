>[!Info] 官方文件
><https://docs.docker.com/reference/cli/docker/>

Docker CLI (`docker`) 是使用者與 Docker daemon 互動的其中一個途徑，這裡節錄了一些常用的指令，想了解完整的指令請看官方文件。

# 顯示 Docker Engine 的資訊

```bash
docker version
# or
docker info  # full info
# or
docker --version  # one-line info
```

# 與 Image 相關的指令

### 列出所有 Images

```bash
docker images [{OPTIONS}]
# or
docker image ls [{OPTIONS}]
```

**常用的 Options**

|Option|Short|Description|
|---|:-:|---|
|`--all`|`-a`|顯示所有 images（預設不顯示 intermediate images）。|
|`--quiet`|`-q`|只顯示 image ID，不顯示其它資訊。|

---

### 根據 Dockerfile 建立 Image

```bash
docker [image] build [{OPTIONS}] {PATH_TO_DOCKERFILE}|{URL}
```

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--tag`|`-t`|爲 image 取名，格式為 `[{HOST}[:{PORT_NUMBER}]/]{PATH}[:{TAG}]`，其中 `{PATH}` 可以再拆解為 `[{NAMESPACE}/]{REPOSITORY}`。|
|`--target {STAGE}`| |要 build 的 stage（詳見 [multi-stage builds](</Tools/Docker/3 - Dockerfile, Image & Container.md#Multi-Stage Builds>)）。|
|`--platform={P1}[,{P2},...]`| |為一到多個指定平台 build 該平台可用的 image。|
|`--no-cache`| |從頭開始重新 build，不使用過去的 cache。|

- `--platform` 的參數值的格式為 `{OS}/{ARCH}/{VARIANT}`，其中 `{VARIANT}` 可以省略不寫，比如 `linux/amd64`、`linux/arm/v7`。

e.g.

```bash
docker build -t my_image --platform=linux/arm64,linux/amd64 .
```

請注意這個指令的最後有一個 `.`，意思是使用目前下指令的這層目錄的 Dockerfile

---

### 查看一個 Image 的每一層

```bash
docker image history [{OPTIONS}] {IMAGE_ID}
```

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--no-trunc`| |不截斷指令。|

---

### 刪除 Image

```bash
docker image rm [{OPTIONS}] {IMAGE_ID} [{IMAGE_ID} ...]
# or
docker rmi [{OPTIONS}] {IMAGE_ID} [{IMAGE_ID} ...]
```

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--force`|`-f`|強制刪除。|

Running container 的 image 須要額外使用 `-f` option 才能被刪除，此時 container 也會同時被終止並刪除。

# 與 Container 相關的指令

### 列出所有 Containers

```bash
docker [container] ps
# or
docker container ls
```

**常用的 Options**

|Option|Short|Description|
|---|:-:|---|
|`--all`|`-a`|顯示所有 containers（預設只顯示 running 的）。|
|`--quiet`|`-q`|只顯示 container ID，不顯示其它資訊。|

---

### 🔥 根據 Image 建立並啟動 Container

```bash
docker run [{OPTIONS}] {IMAGE_NAME} [{COMMAND}]
```

**常用的 Options**

|Option|Short|Description|
|---|:-:|---|
|`--detach`|`-d`|在背景執行 container，不佔用 host 的終端機。|
|`--env {KEY}={VALUE}`|`-e`|設定環境變數。（多個環境變數需要多個 `-e`）|
|`--env-file {PATH_TO_FILE}`| |透過檔案一次設定多個環境變數。|
|`--tty`|`-t`|將 host 的終端機連接上 container 的 I/O streams。|
|`--interactive`|`-i`|維持 container 的 STDIN 開啟，須搭配 `-t` 使用。|
|`--publish`|`-p`|將 container 的 port 映射到 host 的 port。</br>使用方式: `-p {HOST_PORT}:{CONTAINER_PORT}`|
|`--rm`| |離開 container 後，自動刪除 container，以及相關的 volumes。|
|`--volume`|`-v`|將 volume / host-directories 綁定 container。</br>使用方式: `-v {HOST_PATH}:{CONTAINER_PATH}`|
|`--mount`|`-m`|將 volume/host-directories/`tmpfs` 綁定 container。使用方式請見[這篇](</Tools/Docker/7 - Storage in Docker.draft.md>)。|

- `docker run` 可以拆解為 `docker create` 與 `docker start` 兩個步驟。
- 若在 host 找不到指定的 image，則會嘗試 pull image from Docker Hub。
- `-v` 與 `--mount` 的功能差不多，但 `--mount` 的功能更齊全，所以官方推薦一律使用 `--mount`。
- 若 `-e` 或 `--env-file` 中含有與 Dockerfile 中 `ENV` 所設定的環境變數同名的變數，則會覆蓋掉 Dockerfile 中的 `ENV` 所設定的值。
- `{COMMAND}` 是啟動 container 後要在 container 內執行的指令，可以不提供，若提供的話，會==覆蓋掉==原本寫在 Dockerfile 的 `CMD` 的指令。

e.g.

```bash
docker run --name my_container -it my_image echo hello
```

---

>[!Note]
>`docker run` 的 `{COMMAND}` 雖然看起來像 **Shell form**，但其實是 **exec form**。==exec form 不是使用 Shell 執行指令==，所以無法做到「讀取變數」、「使用 `&&` 串接多個指令」等 Shell script 獨有的操作，必須打開 Shell 然後在 Shell 裡面執行 Shell script 才可以：
>
>```bash
>docker run -it my_image sh -c "cd /app && echo $MY_VAR"
>```
>
>關於 Shell form 與 exec form 的詳細差別，請看[這篇](</Tools/Docker/3 - Dockerfile, Image & Container.md#RUN>)。

---

### 根據 Image 建立 Container

```bash
docker [container] create [{OPTIONS}] {IMAGE_NAME} [{COMMAND}]
```

Options 幾乎與 `docker run` 相同，只差沒有 `--detach`。

---

### 啟動 Created/Stopped Container

```bash
docker [container] start {CONTAINER_ID} [{CONTAINER_ID} ...]
```

啟動後，container 的狀態會變為 "UP"。

---

### 終止 Running Container

```bash
docker [container] stop [{OPTIONS}] {CONTAINER_ID} [{CONTAINER_ID} ...]
```

**常用的 Options**

|Option|Short|Description|
|---|:-:|---|
|`--singal`|`-s`|用來終止 container 的 [Unix signal](</Operating System/Unix Signal & IPC.md>)，預設為 `SIGTERM` (15)，參數值可以使用 signal 的名字或代號，比如 `-s SIGKILL` 或 `-s 9`。|
|`--time`|`-t`|強制關閉前所等待的時間 (grace period)。在送出 Unix signal 後，若 container 超過指定時間還沒有停止，則送出 `SIGKILL`。|

- 若 container 是 Linux container，則強制關閉前所等待的時間 default 為 10 秒；Windows container 的 default 為 30 秒。
- 在 create container 時，可以透過 `--stop-signal` 與 `--stop-timeout` 來設定該 container 的預設值。
- 若啟動 container 時有配置終端機，那也可以在該終端機前景使用 `Ctrl` + `C` 終止 container。
- 終止後，container 的狀態會變為 "Exited"。

---

### 立即強制終止 Running Container

```bash
docker [container] kill {CONTAINER_ID} [{CONTAINER_ID} ...]
```

`docker kill` 的效果等價於 `docker stop -s 9`，兩者都不會有 grace period。

>[!Note]
>關於 container 的各種狀態間如何切換，請看[這篇](</Tools/Docker/3 - Dockerfile, Image & Container.md#Container Status>)。

---

### 重新啟動 Container

```bash
docker [container] restart [{OPTIONS}] {CONTAINER_ID} [{CONTAINER_ID} ...]
```

將狀態為 "Running" 的 container 關掉重開。

---

### 在正在運行的 Container 中執行指令

```bash
docker [container] exec [{OPTIONS}] {CONTAINER_ID} {COMMAND}
```

`{COMMAND}` 的部分只能有一個指令，不能直接用 `&&` 將多個指令串接，因此若要執行多個指令，須要先開 subshell 再將指令傳入，比如：

```bash
# 正確寫法：
docker exec -it my_container sh -c "pwd && pwd"
# sh -c "pwd && pwd" 是在 container 內執行

# 以下為錯誤示範：
docker exec -it my_container pwd && pwd
# && 後面的 pwd 是直接在 host 上執行
```

**常用的 Options**

|Option|Short|Description|
|:--|:-:|---|
|`--detach`|`-d`|在背景執行指令，所以不會看到指令的輸出。|
|`--env {KEY}={VALUE}`|`-e`|設定環境變數。|
|`--env-file {PATH_TO_FILE}`| |透過檔案一次設定多個環境變數。|
|`--interactive`|`-i`|保持 STDIN 開啟。|
|`--tty`|`-t`|配置一個終端機，要搭配 `-i` 使用。|
|`--user {USER}`|`-u`|以指定的 user 身份執行指令。|
|`--workdir {PATH}`|`-w`|在指定路徑下執行指令。|

- 使用 `-e` 設定環境變數時，每個環境變數前面都須要一個 `-e`，如：`-e A=a -e B=b`。
- 使用 `-t` 時，須搭配 `-i` 使用，這樣 container 內的 TTY 才收得到使用者輸入的指令。

##### 🔥 開啟 Container 中的 Shell

```bash
docker exec -it my_container bash
```

>[!Note]
>若 base image 的後綴為 "alpine"，則沒有 `bash`，只有 `sh`。

---

### 查看 Container 的 Log

```bash
docker [container] logs [{OPTIONS}] {CONTAINER_ID}
```

**常用的 Options**

|Option|Short|Description|
|:--|:-:|---|
|`--follow`|`-f`|持續監控 logs，不結束指令。|

---

### 動態監控 Container 的資源使用狀況

```bash
docker [container] stats [{CONTAINER_ID} ...]
```

若沒有提供任何 `{CONTAINER_ID}`，則預設是監控所有 running containers。

---

### 刪除 Container

##### 刪除指定 Container

```bash
docker [container] rm [{OPTIONS}] {CONTAINER_ID} [{CONTAINER_ID} ...]
```

- 預設無法刪除狀態為 "Running" 的 containers，須加上 `-f` option。

**常用的 Options**

|Option|Short|Description|
|---|:-:|---|
|`--force`|`-f`|若 container 仍為 running 狀態，則先使用 `SIGKILL` 立即強制終止，再執行刪除。|
|`--volumes`|`-v`|連同 container 的 volumes 一起刪除，但不會刪有特別取名的 volume。|

##### 刪除所有 Stopped Containers

```bash
docker container prune [{OPTIONS}]
```

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--force`|`-f`|刪除前不顯示提示問句。|

# 與 Volume 相關的指令

### 列出所有 Volumes

```bash
docker volume ls
```

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--quiet`|`-q`|只顯示 volume name，不顯示其它資訊。|

---

### 刪除 Volume

```bash
docker volume rm {VOLUME_NAME} [{VOLUME_NAME} ...]
```

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--force`|`-f`|強制刪除。|

Running container 的 volume 須要額外使用 `-f` option 才能被刪除，此時 container 不會被刪除，但可能會因為無法存取 volume 而出現 error。

---

### 刪除所有沒用到的 Volumes

```bash
docker volume prune
```

# 與 Docker Compose 相關的指令

請見 [Docker Compose](</Tools/Docker/5 - Docker Compose.draft.md>)。

# 清理垃圾

```bash
docker system prune [{OPTIONS}]
```

這個指令預設會刪除所有 dangling images、stopped containers、unused networks 與 unused build cache。

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--all`|`-a`|連同 unused images 也刪除（預設只刪除 dangling 的）|
|`--force`|`-f`|刪除前不顯示提示問句。|
|`--volumes`| |刪除 anonymous volumes。|

# 與 Registry 相關的指令

### 從 Registry 搜尋 Images

```bash
docker search {KEYWORD}
```

e.g.

```bash
docker search redis
```

---

### 從 Registry 下載指定 Image 至 Local

```bash
docker [image] pull {IMAGE_NAME}[:{IMAGE_VERSION}]
```

- 如果不指定 `{IMAGE_VERSION}` 則預設為 `latest`。

e.g.

```bash
docker pull ubuntu:14.04
```

---

### 將 Image 上傳到 Registry

```bash
docker [image] push [{HOST}[:{PORT}]/]{PATH}[:{TAG}]
```

- `{HOST}` 預設是 Docker Hub 的 public registry (`registry-1.docker.io`)，若要上傳到 self-host registry 就須要額外寫
- `{PATH}` 可以再分解為 `[{NAMESPACE}/]{REPOSITORY}`
    - `{NAMESPACE}` 預設為 `library`，通常會寫公司或組織的名稱
    - `{REPOSITORY}` 沒有預設值，必填

e.g.

```bash
docker push registry.helloworld.io/my_server:latest
```

# 其它組合技

```bash
# 刪除所有 images
docker rmi $(docker images -aq)

# 強制停止所有 containers
docker stop -f $(docker ps -aq)
```

# 查詢使用方式

```bash
docker {SUB_COMMAND} --help
```

e.g.

```bash
docker push --help
```
