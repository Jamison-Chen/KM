### 步驟一：取得目標 Container 的 ID

列出所有 containers，找到目標的 id

```bash
docker ps
```

### 步驟二：找到目標 Container 的 Log 檔存放位置

其實這個步驟可以省略，因為在步驟三會直接使用這個指令當作取得路徑的方式。

```sh
docker inspect --format='{{.LogPath}}' <CONTAINER_ID>
```

Output 會長得像這樣：

```plaintext
/var/lib/docker/containers/57ef5c1...-json.log
```

這個路徑是實體機器的檔案路徑，不是 container 內的路徑。

### 步驟三：將該檔案的內容清空

這裡我們使用 `echo` 指令：

```bash
sudo sh -c 'echo "" > $(docker inspect --format="{{.LogPath}}" CONTAINER_ID>)'
```

Done!

# 參考資料

- <https://www.howtogeek.com/devops/how-to-clear-logs-of-running-docker-containers/>
