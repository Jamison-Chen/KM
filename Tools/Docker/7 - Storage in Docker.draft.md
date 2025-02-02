# Volume

- 綁定 container 的 volume 不會隨著 container 被刪除而消失（除非刪除 container 時有特別要求）所以我們說存在 volume 裡的資料具有持久性。
- 同一個 volume 可以讓不同 containers 存取，達到 containers 共享檔案的效果。
- Volume 通常被拿來放資料庫的資料，以及使用者生成的檔案。

# Bind Mount

- Bind mount 的功能是將 host 指定路徑的檔案「掛載」到 container 內，使得兩邊的資料同步更動。
- 如果希望編輯中的程式碼或 compiled binary 可以即時地反應到容器化的 development server，則須要將 codebase 或 compiled binary "bind mount" 到 container 中。
- Volumes 是一種由 Docker 控管的 bind mount。

### Named Volume vs. Bind Mount
  
| |Named Volumes|Bind Mounts|
|--|--|--|
|Host location|Docker chooses|You decide|
|Populates new volume with container contents|Yes|No|
|Supports Volume Drivers|Yes|No|

# 實際演練

### Step 1: Create Volume

```bash
docker volume create {VOLUME_NAME}
```

### Step 2: Volume Mount / Bind Mount

在 `docker run` 指令中可以用 `--volume` (`-v`) 或 `--mount` option 來進行 volume mount 與 bind mount：

##### 方法一：使用 `--volume` (`-v`)

```bash
# Named volume
docker run -v {VOLUME_NAME}:{CONTAINER_PATH} {IMAGE}

# or, bind mount
docker run -v {HOST_PATH}:{CONTAINER_PATH} {IMAGE}
```

##### 方法二：使用 `--mount`

```bash
# named volume
docker run --mount type=volume,src={VOLUME_NAME},target={CONTAINER_PATH} {IMAGE}

# or, bind mount
docker run --mount type=bind,src={HOST_PATH},target={CONTAINER_PATH} {IMAGE}
```

以下是 named volume 與 bind mount 的差異：

- Named volume: `type=volume,src={VOLUME_NAME},target={CONTAINER_PATH}`
- Bind mount: `type=bind,src={HOST_PATH},target={CONTAINER_PATH}`

官方推薦一律使用 `--mount`，因為 `--mount` 可以做到所有 `--volume` 做得到的事，且功能比 `--volume` 齊全。
