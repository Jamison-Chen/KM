### `HEAD` 與檔案 HEAD

`HEAD` 是一個指向「目前所在的 commit」的 pointer，以檔案的型態存在於 .git 中，檔名就叫 HEAD，這個檔案的內容會長得像這樣：

```plaintext
ref: refs/heads/main
```

其中 `refs/heads/main` 是 .git 中另一個檔案的路徑，實際找到 .git/refs/heads/main 後，可以看到它的內容是一個 40 個 16 進制字元的 hash value，形如：

```plaintext
676b452bece6f5e83f50ce271d0cf96ba2781513
```

- 這個 hash value 其實就是目前所在的 commit 的編號
- 檔案路徑 refs/heads/main 中的 main 是目前所在的分支的名字

`HEAD` 會自動指向目前所在的[[Branch - Basic|分支]]的「最近一個 commit」，所以：

- 切換分支時 `HEAD` 會變

    比如從 `main` 切到 `dev` 時，.git/HEAD 的內容會從 `ref: refs/heads/main` 變成 `ref: refs/heads/dev`。

- 新增 commit 時 `HEAD` 也會變

    但此時變的不是 .git/HEAD 的內容，而是 .git/ref/heads/main 內的 hash value（假設是在 `main` 分支上新增 commit）。

### Detached `HEAD`

#TODO 

### `FETCH_HEAD`

#TODO 

### `ORIG_HEAD`

#TODO 
