# 什麼是分支？

- 可以想成在 commit 上多貼一個「標籤」代表其所屬的 branch
- 一個 commit 可以同時屬於多個 branches（一個 commit 可以貼上多個標籤）
- 所有具有相同標籤的 commits 串連起來就是一個 branch
- 一個 repo 至少要有一個 branch
- 多個 branches 可以 [merge](</Tools/Git/merge.md>)（合併）成一個 branch

### Default Branch

一個 repo 至少要有一個 branch，初始化一個 repo 時會有一個預設的 branch 叫做 `main`（較舊的版本則叫 `master`），在 global 設定檔可以設定「初始化 repo 時預設 branch 的名稱」：

```bash
git config --global init.defaultBranch {BRANCH_NAME}
```

或者也可以直接在 global 設定檔 (.gitconfig) 加入下面設定：

```properties
[init]
defaultBranch = main
```

請注意這個設定不會影響到已建立的 repo。

# 為什麼需要分支？

### 原因一：方便多人協作

一個 commit 就代表一種專案的狀態，多人協作同一個專案時，經常會同時有多個人需要基於同一個狀態（基於同一個 commit）進行開發，若大家都在 `main` branch 上，當某個人率先在原 commit 後面新增 commits 並 [push](</Tools/Git/push、fetch、pull.md#`git push`>) 後，其他人的 local `main` branch 就會因爲 outdated（缺乏第一個人新加的 commits）而無法 push。

有了 branch，大家就可以各自基於 `main` 另開自己的 branch，這樣自己新增的 commits 就會被貼上自己 branch 的標籤，也可以將這個 branch 的 commits push 至 remote repo，其他人也可以 push 他們的 commits 到他們的 branches。

### 原因二：確保產品穩定

就算是一人專案，一個持續有新功能的產品在增加新功能的中途難免會出現 bug，若 production code 與 development code 在同一個 branch，產品就會很不穩定，多人協作時，development code 更容易因為大家同時在加功能而出現「單獨看都很好但合起來就壞掉」的狀況。

如果可以將 production code 與 development code 區分成兩個 branches（假設叫 `main` 與 `dev`），新功能開發完畢後先 push 上 `dev`，並針對 `dev` 做好測試，確定沒問題後再將 `dev` [merge](</Tools/Git/merge.md>) 進 `main`，這樣可以大幅增加 `main` 的穩定性。

# 常用指令

### 列出所有分支

```bash
# 只列出 local branches
git branch

# 只列出有 fetch 至 local 的 remote branches
git branch -r

# 將上面兩種皆列出
git branch -a
```

Example output:

```plantext
  bar
  foo
* master
```

- 有 `*` 的是目前所在的分支

### 新增分支

```bash
git branch {NEW_BRANCH} [{FROM_BRANCH}]
```

- 「新增一個 branch」就是在指定的 commit 上多貼一個標籤
- 如果沒有特別寫 `{FROM_BRANCH}`，那就是基於「現在所在的 branch」新增一個 branch；或者說是在「現在所在的 branch 的最後一個 commit」上多貼一個叫 `{NEW_BRANCH}` 的標籤
- Branch 新增成功後，會停留在原本的 branch

### 切換分支

```bash
git checkout {BRANCH}
```

- 若指定的 branch name 不存在，則 Git 會報錯
- 切換 branch 時，在原 branch 上對 working directory 的變動會被保留（不須要「push to [stash](</Tools/Git/stash.md>) → checkout to new branch → pop from stash」）

##### 新增 Branch 後直接切過去

```bash
git checkout -b {NEW_BRANCH} [{FROM_BRANCH}]
```

- 如果沒有特別寫 `{FROM_BRANCH}`，那就是基於「現在所在的 branch」新增一個 branch

>[!Note]
>`git checkout` 的其它用法請見[本文](</Tools/Git/checkout、switch、restore.canvas>)。

### 重新命名分支

```bash
git branch -m {OLD_NAME} {NEW_NAME}
```

### 刪除分支

```bash
git branch -d {BRANCH}
```

- 不能刪除目前所在的分支
- 如果欲刪除的分支有一些目前所在的分支沒有的 commits，則 git 會提示：

    ```plaintext
    error: The branch foo is not fully merged.
    If you are sure you want to delete it, run 'git branch -D foo'.
    ```

    - 使用 `-D` option 就可以強制刪除
    - 若 merge 時使用 squash merge，則因為 squash merge 是一個全新的 commit，所以還是會出現上面的錯誤提示（`foo` squash merge `bar` 後，`foo` 上還是找不到 `bar` 上多出來的 commits）

# 其它

### 新增一個「沒有 Parent」的 Branch

```bash
git checkout --orphan {NEW_BRANCH}
```

實務上須要這個指令的時機比如要新增一個 branch 給 [GitHub Page](</Tools/Git/GitHub/GitHub Page.md>)。
