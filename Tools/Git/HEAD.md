# `HEAD` 與 HEAD File

`HEAD` 是一個指向「repo 目前所在的 commit」的 pointer，以檔案的型態存在於 .git 中，檔名就叫 HEAD，這個檔案的內容會長得像這樣：

```plaintext
ref: refs/heads/main
```

其中 `refs/heads/main` 是 .git 中另一個檔案的路徑，實際找到 .git/refs/heads/main 後，可以看到它的內容是一個 40 個 16 進制字元的 hash value，形如：

```plaintext
676b452bece6f5e83f50ce271d0cf96ba2781513
```

- 這個 hash value 其實就是 repo 目前所在的 commit 的編號
- 檔案路徑 refs/heads/main 中的 main 是目前所在的分支的名字

`HEAD` 會自動指向目前所在的 [branch](</Tools/Git/Branch.md>) 的「最後一個 commit」，所以：

- 切換 branch 時，`HEAD` 會變

    比如從 `main` 切到 `dev` 時，.git/HEAD 的內容會從 `ref: refs/heads/main` 變成 `ref: refs/heads/dev`。

- 新增 commit 時 `HEAD` 也會變

    但此時變的不是 .git/HEAD 的內容，而是 .git/ref/heads/`BRANCH_NAME` 內的 hash value。

`HEAD` 在指令中也可以用 `@` 代替之。

# 利用相對位置指定 Commit

在執行 `git reset`、`git revert` 等指令時，會需要指定 commit，此時除了可以使用前面提到的 40 碼 hash value 指定外（其實只要前 7 碼，因為發生碰撞的機率太低了），也可以使用「以 `HEAD` 為出發點的相對位置」來指定 commit。

相對位置的寫法有兩種：

- `^`：一個 `^` 就是指「前一個」commit，所以 `HEAD^^^` 就是指 `HEAD` 的前 3 個 commit

    ```mermaid
    %%{init: { 'logLevel': 'debug', 'theme': 'base' } }%%
    gitGraph
        commit tag: "HEAD"
        commit tag: "HEAD^"
        commit tag: "HEAD^^"
    ```

- `~n`：前 n 個 commit，`HEAD~7` 就是指 `HEAD` 的前 7 個 commit

    ```mermaid
    %%{init: { 'logLevel': 'debug', 'theme': 'base' } }%%
    gitGraph
        commit tag: "HEAD"
        commit tag: "HEAD~1"
        commit tag: "HEAD~2"
    ```

# Detached `HEAD`

當 `HEAD` 不在一個 branch 的最後一個 commit 時，就是 detached 的狀態（其實「不在一個 branch 的最後一個 commit」就等同於「不在 branch 上」）所以換句話說，detached HEAD 就是 HEAD 不知道自己在哪個 branch 上。

關於如何進入與離開 detached HEAD 狀態，請見 [checkout](</Tools/Git/checkout、switch、restore.canvas#Detached HEAD>)。

# 其它種類的 `HEAD`

### `FETCH_HEAD`

#TODO 

### `ORIG_HEAD`

#TODO 
