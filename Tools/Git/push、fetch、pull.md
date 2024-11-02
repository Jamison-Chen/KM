# `git push`

>將地端 (local) repository 的 commit 推送至雲端 (remote) repository。

### 首次將地端的 Repo 推送至雲端

- Step1: 在 GitHub 上建立一個新的 remote repository，取得此 repo 的 URL

- Step2: 在 local repo 的根目錄將 origin 設定為 step1 取得的 URL

    ```bash
    git remote add origin {REMOTE_REPO_URL}
    ```

    此步驟的作用是「用一個叫做 `origin` 的變數儲存 remote repo 的 URL」，這樣以後 push 時，就不用把 remote repo 的 URL 一字不漏地寫出來，只須以 `origin` 作為 alias 即可。（[詳見此文](https://www.git-tower.com/learn/git/glossary/origin)）

    >[!Note]
    >有 `add` 當然就有 `remove`，請見[[#移除 `origin` 與 `{REMOTE_REPO_URL}` 的對應關係|此段]]。

- Step3: 將目前所在的 local branch 推送至 remote repo 中的指定 branch

    ```bash
    git push -u origin {REMOTE_BRANCH_NAME}
    ```

    若 remote repo 原本不存在指定名稱的 branch，push 後會自動長出來。

    加上 `-u` (`--set-upstream`) option 可以讓 Git 順便記住現在所在的這個 local branch name 與 `{REMOTE_BRANCH_NAME}` 之間的對應關係，這個 option 只須在「local 有新的 branch 第一次要推上 remote」時加。這樣日後 push 或 pull 這個 branch 時，就可以直接執行 `git push` 或 `git pull`，不用聲明 remote branch name，Git 會自動根據你現在所在的 local branch 決定對應的 remote branch。

---

### 直接 Push 到指定 Remote Repo

若要直接 push 到指定的 remote repo，則無須上面的 step2 與 step3，直接執行以下指令即可：

```bash
git push {REMOTE_REPO_URL}
```

這個做法適合在要推送到平常不常推送的 remote repo 時使用，因為沒有建立變數儲存 remote repo 的 url，因此執行 `git branch -r` 時也不會有紀錄。

### Push 所有 Local Branches 至 Remote Repo

```bash
git push --all origin
```

### Push 的原則

- 每次從 local push 到 remote 時，git 都會將所有「上次成功 push 或 pull 的 commit」之後的所有 commit(s) 都 push 過去。
- 若 local 的「上次成功 push 或 pull 的 commit」與 remote 目前的 HEAD 不是同一個 commit，則 push 會失敗並出現 conflict 提示。通常造成此現象的原因是有其他人在對 remote repo 做事，比如 push 新的 commit 到你現在要 push 的 remote branch 上。

### 強制 Push

```bash
git push -f origin {REMOTE_BRANCH_NAME}
```

- 強制 push 目前 local branch 的狀態到 remote branch，無視前面說的 push 的原則
- 可以在 GitHub 設定某 repo 的某 branch 要拒絕 force push，藉此[保護 Branch](</Tools/Git/GitHub/保護 Branch.md>)

>[!Danger]
>
>```bash
>git push -f --all origin
>```
>
>可以將上面這個指令理解為「把 remote 的 .git folder 整包刪除，以目前要 push 上去的 .git folder 取代之」，或者理解為「push 一個全新的專案取代掉原本的」。

### 移除 `origin` 與 `{REMOTE_REPO_URL}` 的對應關係

```bash
git remote remove origin
```

### 列出所有 Local 的 Remote-Tracking References

```bash
git branch -r
```

Example output：

```plaintext
remote/origin/master
remote/origin/dev
```

每一個 remote-tracking references 都用來代表一個 remote branch。

### 在 Local 刪除 Remote-Tracking References

```bash
git branch -rd origin/{REMOTE_BRANCH_NAME}
```

這個指令只是刪除 local 的 reference 而已，並不會刪到 remote 的 brach 本人。

### 刪除 Remote Branch (from Local)

>[!Danger] 注意
>這個指令會刪除 remote repo 的 branch。

```bash
git push origin -d {REMOTE_BRANCH_NAME}
```

>[!Note]
>雖然 `git branch -r` 時，remote branches 會有 prefix `remote/origin/`，但這個指令中不用寫 prefix。

# `git fetch`

>將 remote repo 的最新狀態下載至 local。

- Fetch 指定的 remote branch

    ```bash
    git fetch origin {REMOTE_BRANCH_NAME}
    ```

- Fetch 所有 remote branches

    ```bash
    git fetch origin
    ```

Git 會用形如 `origin/{REMOTE_BRANCH_NAME}` 的 **remote-tracking reference** 標記 fetch 至 local 的 remote branches，可以使用 `git branch -r` 查看。

### 將 Local 的所有「已不存在於 Remote」的 Remote-Tracking References 刪除

```bash
git remote prune origin
```

### 組和技：Fetch and then Prune

```bash
git fetch --prune origin
```

這個指令會先 fetch 所有的 remote 分支，再 prune 掉 local 的「已不存在於 remote」的 remote-tracking references。

所以可以說 `git fetch --prune origin` = `git fetch origin` + `git remote prune origin`。

### 🔥 把一個 Local 沒有的分支從 Remote 拉過來

```bash
# Step1
git fetch origin {BRANCH_NAME}

# Step2
git checkout -b {BRANCH_NAME} FETCH_HEAD
```

# `git pull`

`git pull` = `git fetch` + `git merge`

- Fetch 所有 remote branches，並 merge **remote HEAD** 所在的 branch 至目前的 local branch

    ```bash
    git pull origin
    ```

- Fetch 指定的 remote branch，並將它 merge 至目前的 local branch

    ```bash
    git pull origin {REMOTE_BRANCH_NAME}
    ```

# Local 與 Remote 出現分歧時怎麼辦？

```plaintext
      A---B---C remote master
     /
D---E---F---G local master
    ^
    origin/master
```

若目前所在的 local branch 與準備 pull 的 remote branch 有分歧時（也就是 local 的 `origin/{REMOTE_BRANCH_NAME}` 與 remote 的 `{REMOTE_BRANCH_NAME}` 的 HEAD 不是同一個 commit 時），pull 會失敗，並且會出現警告。

此時你有三種選項：

- 把兩個 branches 間的 conflicts 解決並 merge，以 merge 後的版本為最終版本
- 以 local branch 為最終版本
- 以 remote branch 為最終版本

### 解 Conflicts 並 Merge

- **Step1: 加上 option 來聲明要維持用 merge 的方式來合併，還是改用 rebase**

    ```bash
    # Option 1: 維持用 merge 的方式來合併 remote branch
    git pull origin {REMOTE_BRANCH_NAME} --no-rebase
    
    # Option 2: 改用 rebase
    git pull origin {REMOTE_BRANCH_NAME} --rebase
    ```

- **Step2: 手動解兩個 branches 間的 conflicts**

- **Step3: push merge/rebase 完的結果至 remote**

    - 若採用 merge：

        ```plaintext
           A---B---C remote master|origin/master
          /         \
        D---E---F---G---H local master
        ```

        須將 H push 至 remote。

        Push 後：

        ```plaintext
           A---B---C
          /         \
        D---E---F---G---H local master|remote master|origin/master
        ```

    - 若採用 rebase：

        ```plaintext
        remote master|origin/master
            ˇ
        D---E---A---B---C---F'---G'---H' local master
        ```

        須要將 F', G', H' push 至 remote。

        Push 後：

        ```plaintext
        D---E---A---B---C---F'---G'---H'
                                      ^
                    local master|remote master|origin/master
        ```

### 以 Local Branch 為最終版本

```bash
git push origin {REMOTE_BRANCH_NAME} -f
```

### 以 Remote Branch 為最終版本

**簡單版**

```bash
# Step1: Fetch the remote branch.
git fetch origin {REMOTE_BRANCH_NAME}

# Step2: Reset the local branch to the fetched branch.
git reset --hard origin/{REMOTE_BRANCH_NAME}
```

**複雜版**

```bash
# Step1: Fetch the remote branch.
git fetch origin {REMOTE_BRANCH_NAME}

# Step2: Re-create the local branch based on the fetched branch.
git checkout origin/{REMOTE_BRANCH_NAME}
git branch -D {LOCAL_BRANCH_NAME}
git checkout -b {LOCAL_BRANCH_NAME}

# Step3: Fast-forward merge the remote branch to this new local branch.
git merge origin/{REMOTE_BRANCH_NAME}
```
