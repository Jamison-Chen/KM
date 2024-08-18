#TODO 

# 常用指令

#Command 

### 顯示 Docker Engine 的資訊

```bash
docker version
# or
docker info  # full info
# or
docker --version  # one-line info
```

### Image

##### 根據 Dockerfile 建立 Image

```sh
docker build [<OPTIONS>] <PATH_TO_DOCKERFILE>|<URL>
```

|Options|Short|Description|
|:-:|:-:|:-:|
|`--tag`|`-t`|爲 image 取名，可以只有名字或是 `<NAME>:<TAG>` 的形式。|

e.g.

```bash
docker build --tag my_image .
```

- 注意這個指令的最後有一個 `.`

##### 列出 Local 的所有 Images

```bash
docker images
# or
docker image ls
```

### Container

##### 列出 Local 的所有 Containers

```bash
# 只列出 status 為 UP 的
docker ps

# 列出所有
docker ps -a
# or
docker ps --all
```

##### 根據 Image 建立並啟動 Container

```sh
docker run [<OPTIONS>] <IMAGE_NAME> [<COMMANDS>]
```

>[!Note]
>若本機找不到指定的 image 則會嘗試從 DockerHub 下載 image。

|Options|Short|Description|
|--|--|--|
|`--detach`|`-d`|在背景執行 container，並印出 container ID。|
|`--interactive`|`-i`|在背景執行的狀態下，維持 STDIN 開啟，須搭配 `-t` 使用。|
|`--name`||爲 container 取名。|
|`--publish`|`-p`|將 container 的 port 映射到 host。</br>使用方式: `-p <PORT_OF_CONTAINER>:<PORT_OF_HOST>`|
|`--tty`|`-t`|配置一個終端機。|

##### 示範

- 根據 my_image 建立一個名為 my_container 的 container，並配置一個終端機：

    ```bash
    docker run --name my_container -it my_image
    ```

### DockerHub

##### 從 DockerHub 中搜尋 Images

```sh
docker search <KEYWORD>
```

e.g.

```bash
docker search redis
```

##### 從 DockerHub 下載指定 Image 至 Local

```sh
docker pull <IMAGE_NAME>[:<IMAGE_VERSION>]
```

e.g.

```bash
docker pull ubuntu:14.04
```

如果不指定 image 版本則預設為 latest。

##### 將 Local 的 Image 推到 DockerHub

```sh
docker push <IMAGE_NAME>[:<TAG>]
```

# 參考資料

- <https://docs.docker.com/engine/reference/commandline/docker/>
