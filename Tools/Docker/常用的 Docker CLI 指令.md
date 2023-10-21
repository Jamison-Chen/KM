#Command 

### 啟動 Docker Daemon

###### On Linux

```bash
systemctl start docker
```

###### On MacOS

- 最簡單的方法就是打開 Docker Desktop
- 其它方法請參考[本文](<https://apple.stackexchange.com/questions/373888/how-do-i-start-the-docker-daemon-on-macos>)

---

### 顯示 Docker Daemon 的資訊

###### 只顯示版本資訊

```bash
docker version
# or
docker --version  # less info
```

###### 顯示完整資訊

```bash
docker info
```

---

### 從 Docker Hub 中搜尋 Images

```sh
docker search <KEYWORD>
```

e.g.

```bash
docker search redis
```

---

### 從 Docker Hub 下載指定 Image 至 Local

```sh
docker pull <IMAGE_NAME>[:<IMAGE_VERSION>]
```

e.g.

```bash
docker pull ubuntu:14.04
```

如果不指定 image 版本則預設為 latest。

---

### 列出 Local 的所有 Images

```bash
docker images
# or
docker image ls
```

---

### 列出 Local 的所有 Containers

```bash
# 只列出 status 為 UP 的
docker ps

# 列出所有
docker ps -a
# or
docker ps --all
```
