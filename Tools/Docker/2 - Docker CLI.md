#Command

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

# 初始化

```bash
docker init
```

在專案中建立所有 Docker 所須用到的檔案，包括 Dockerfile、.dockerignore、compose.yml 與 README.Docker.md。

>[!Note]
>也可以不使用這個指令，直接手動建立檔案。

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
|`--quiet`|`-q`|只顯示 image id，不顯示其它資訊。|

### 根據 Dockerfile 建立 Image

```bash
docker [image] build [{OPTIONS}] {PATH_TO_DOCKERFILE}|{URL}
```

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--tag`|`-t`|爲 image 取名，可以只有名字或是 `<NAME>:<TAG>` 的形式。|
|`--no-cache`| |從頭開始重新 build，不使用過去的 cache。|

e.g.

```bash
docker build -t my_image .
```

- 注意：這個指令的最後有一個 `.`，意思是使用目前下指令的這層目錄的 Dockerfile

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
|`--quiet`|`-q`|只顯示 container id，不顯示其它資訊。|

### 根據 Image 建立並啟動 Container

```bash
docker run [{OPTIONS}] {IMAGE_NAME} [{COMMAND}]
```

- `{COMMAND}` 是啟動 container 後要在 container 內執行的指令，可以不提供，若提供的話，會==覆蓋掉==原本寫在 Dockerfile 的 `CMD` 的指令。
- `docker run` 可以拆解為 `docker create` 與 `docker start` 兩個步驟。

>[!Note]
>若在 local 找不到名為 `{IMAGE_NAME}` 的 image，則會嘗試從 Docker Hub 下載 image。

**常用的 Options**

|Option|Short|Description|
|---|:-:|---|
|`--detach`|`-d`|在背景執行 container，所以不會看到 command output，但會印出 container ID。|
|`--tty`|`-t`|配置一個終端機。|
|`--interactive`|`-i`|在背景執行的狀態下，維持 STDIN 開啟，須搭配 `-t` 使用。|
|`--name`||爲 container 取名。</br>不取名的話，Docker daemon 會隨機幫 container 取名。|
|`--publish`|`-p`|將 container 的 port 映射到 host 的 port。</br>使用方式: `-p <PORT_OF_CONTAINER>:<PORT_OF_HOST>`|

e.g. 根據 my_image 建立一個名為 my_container 的 container，並配置一個終端機，然後在 container 內執行 `echo hello`：

```bash
docker run --name my_container -it my_image echo hello
```

### 根據 Image 建立 Container

```bash
docker [container] create [{OPTIONS}] {IMAGE_NAME} [{COMMAND}]
```

Options 幾乎與 `docker run` 相同，只差沒有 `--detach`。

### 啟動 Created/Stopped Container

```bash
docker [container] start {CONTAINER_ID} [{CONTAINER_ID} ...]
```

啟動後，container 的狀態會變為 "UP"。

### 終止 Running Container

```bash
docker [container] stop [{OPTIONS}] {CONTAINER_ID} [{CONTAINER_ID} ...]
```

**常用的 Options**

|Option|Short|Description|
|---|:-:|---|
|`--singal`|`-s`|用來終止 container 的 [[Unix Signal & IPC\|Unix signal]]，預設為 `SIGTERM` (15)，參數值可以使用 signal 的名字或代號，比如 `-s SIGKILL` 或 `-s 9`。|
|`--time`|`-t`|強制關閉前所等待的時間 (grace period)。在送出 Unix signal 後，若 container 超過指定時間還沒有停止，則送出 `SIGKILL`。|

- 若 container 是 Linux container，則強制關閉前所等待的時間 default 為 10 秒；Windows container 的 default 為 30 秒。
- 在 create container 時，可以透過 `--stop-signal` 與 `--stop-timeout` 來設定該 container 的預設值。
- 若啟動 container 時有配置終端機，那也可以在該終端機前景使用 `Ctrl` + `C` 終止 container。
- 終止後，container 的狀態會變為 "EXITED"。

### 立即強制終止 Running Container

```bash
docker [container] kill {CONTAINER_ID} [{CONTAINER_ID} ...]
```

`docker kill` 的效果等價於 `docker stop -s 9`，兩者都不會有 grace period。

>[!Note]
>關於 container 的各種狀態間如何切換，請看[[3 - Image & Container.draft#Container 的狀態|這篇]]。

### 重新啟動 Container

```bash
docker [container] restart [{OPTIONS}] {CONTAINER_ID} [{CONTAINER_ID} ...]
```

### 在 Container 中執行指令

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
>後綴為 "alpine" 的 Docker image 沒有 `bash`，只有 `sh`。

### 查看 Container 的 Log

```bash
docker [container] logs [{OPTIONS}] {CONTAINER_ID}
```

**常用的 Options**

|Option|Short|Description|
|:--|:-:|---|
|`--follow`|`-f`|持續監控 logs，不結束指令。|

### 動態監控 Container 的資源使用狀況

```bash
docker [container] stats [{CONTAINER_ID} ...]
```

若沒有提供任何 `{CONTAINER_ID}`，則預設是監控所有 running containers。

### 刪除 Container

##### 刪除指定 Container

```bash
docker [container] rm [{OPTIONS}] {CONTAINER_ID} [{CONTAINER_ID} ...]
```

**常用的 Options**

|Option|Short|Description|
|---|:-:|---|
|`--force`|`-f`|使用 `SIGKILL` 立即強制刪除 container，即使它正在運行。|
|`--volumes`|`-v`|連同 container 的 volumes 一起刪除，但不會刪有名字的 volume。|

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

### 刪除 Volume

```bash
docker volume rm {VOLUME_NAME} [{VOLUME_NAME} ...]
```

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--force`|`-f`|強制刪除。|

Running container 的 volume 須要額外使用 `-f` option 才能被刪除，此時 container 不會被刪除，但可能會因為無法存取 volume 而出現 error。

# 與 Docker Compose 相關的指令

>[!Note]
>在過去，Docker compose 有自己的 CLI，指令名稱為 `docker-compose`，但後來 Docker CLI 把它們整合在一起，因此 `docker-compose` 指令已經 deprecated 了。

### 查看 Docker Compose 的版本

```bash
docker compose version
```

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--short`| |只顯示版本號碼。|

### 建立並啟動 Containers

```bash
docker compose [--file {PATH_TO_FILE}] up [{OPTIONS}] [{SERVICE_NAME} ...]
```

- `--file` (`-f`) 用來指定 docker-compose.yml 的路徑，若未提供，則預設是當前目錄中的 docker-compose.yml。
    - 請注意：這個 option 是放在 `compose` 與 `up` 之間。
- 若沒有提供 `{SERVICE_NAME}`，預設是啟動 docker-compose.yml 中的所有 services。

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--build`| |若發現有 image 還沒 build，則先 build image。|
|`--detach`|`-d`|在背景運行 containers，所以不會看到 command output。|
|`--watch`|`-w`|監控 Dockerfile、docker-compose.yml 與所有 containers 內的檔案，若有改動則馬上 rebuild/refresh containers。|

### 停止並刪除 Containers

```bash
docker compose [--file {PATH_TO_FILE}] down [{OPTIONS}] [{SERVICE_NAME} ...]
```

- `--file` (`-f`) 用來指定 docker-compose.yml 的路徑，若未提供，則預設是當前目錄。
- 若沒有提供 `{SERVICE_NAME}`，預設是停止並刪除 docker-compose.yml 中的所有 services（包括 containers 與 networks）。

**常用的 Options**

|Option|Short|Description|
|:-:|:-:|---|
|`--rmi`| |連同相關的 images 一起刪除。|
|`--volumes`|`-v`|連同相關的 volumes 一起刪除。|

### 啟動／停止 Containers

```bash
# 啟動
docker compose [--file {PATH_TO_FILE}] start [{SERVICE_NAME} ...]

# 停止
docker compose [--file {PATH_TO_FILE}] stop [{SERVICE_NAME} ...]
```

- `--file` (`-f`) 用來指定 docker-compose.yml 的路徑，若未提供，則預設是當前目錄。
- 若沒有提供 `{SERVICE_NAME}`，預設是啟動／停止 docker-compose.yml 中的所有 services。

### 在 Container 中執行指令

```bash
docker compose exec [{OPTIONS}] {SERVICE_NAME} {COMMAND}
```

這個指令的效果等同於 `docker exec {CONTAINER_ID} {COMMAND}`，差別在這裡是用 docker-compose.yml 的 service name 來指定 container。

**常用的 Options**

|Option|Short|Description|
|:--|:-:|---|
|`--detach`|`-d`|在背景執行指令，所以不會看到指令的輸出。|
|`--env {KEY}={VALUE}`|`-e`|設定環境變數。|
|`--user {USER}`|`-u`|以指定的 user 身份執行指令。|
|`--workdir {PATH}`|`-w`|在指定路徑下執行指令。|

### 查看 Container 的 Log

```bash
docker compose logs [{OPTIONS}] {CONTAINER_ID}
```

**常用的 Options**

|Option|Short|Description|
|:--|:-:|---|
|`--follow`|`-f`|持續監控 logs，不結束指令。|

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

# 與 Remote Registry 相關的指令

>[!Note]
>Docker 官方有提供 remote registry 的服務，叫做 [[5 - Docker Hub.draft|Docker Hub]]，但我們也可以自己 host remote registry。
### 從 Remote Registry 搜尋 Images

```bash
docker search {KEYWORD}
```

e.g.

```bash
docker search redis
```

### 從 Remote Registry 下載指定 Image 至 Local

```bash
docker [image] pull {IMAGE_NAME}[:{IMAGE_VERSION}]
```

- 如果不指定 `{IMAGE_VERSION}` 則預設為 `latest`。

e.g.

```bash
docker pull ubuntu:14.04
```

### 將 Image 上傳到 Remote Registry

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

# 組合技

```bash
# 刪除所有 images
docker rmi $(docker images -aq)

# 強制停止所有 containers
docker stop -f $(docker ps -aq)
```

# 查詢指令的使用方式

```bash
docker {SUB_COMMAND} --help
```

e.g.

```bash
docker push --help
```
