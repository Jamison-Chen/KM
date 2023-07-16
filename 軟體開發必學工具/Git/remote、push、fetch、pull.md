# `git push`

>將地端 (local) repository 已 commit 的版本推送至雲端 (remote) repository。

### 首次將地端的專案推送至雲端

- **Step1: 在 GitHub 上建立一個新的 repository，取得此 repo 的 URL**

- **Step2: 在 local 使用 terminal 切換至專案根目錄**

    ```bash
    cd <project-name>
    ```

- **Step3: 將 origin 設定為 step1 取得的 URL**

    ```bash
    git remote add origin <REMOTE-REPO-URL>
    ```

    此步驟的目的為「用一個叫做 `origin` 的變數儲存 remote repo 的 URL」，這樣以後 push 時，就不用把 remote repo 的 URL 一字不漏地寫出來，只須以 `origin` 作為 alias 即可。（[詳見此文](https://www.git-tower.com/learn/git/glossary/origin)）

- **Step4: 將目前所在的 local branch 推送至 remote repo 中的指定 branch**

    ```bash
    git push -u origin <REMOTE-BRANCH-NAME>
    ```

    若 remote repo 不存在指定名稱的 branch，會長出一個新的。

    加上 `-u` 或 `--set-upstream` option 可以讓 git 順便記住現在所在的這個 local branch name 與 `<REMOTE-BRANCH-NAME>` 之間的對應關係，這個 option 只須在「local 有新的 branch 第一次要推上 remote」時加。這樣日後 push 或 pull 這個 branch 時，就可以直接執行 `git push` 或 `git pull`，不用聲明 remote branch name，git 會自動根據你現在所在的 local branch 決定對應的 remote branch。

---

### 直接 Push 到指定 Remote Repo

若要直接 push 到指定的 remote repo，則無須 step3 與 step4，直接執行以下指令即可：

```bash
git push <remote-repo-url>
```

這個做法適合在要推送到平常不常推送的 remote repo 時使用，因為沒有建立變數儲存 remote repo 的 url，因此執行 `git branch -r` 時也不會有紀錄。

### 推送所有 Local Branches 至 Remote Repo

```bash
git push --all origin
```

### push 的原則

- 每次從 local push 到 remote 時，git 都會將所有「上次成功 push 或 pull 的 commit」之後的所有 commit(s) 都 push 過去。
- 若 local 的「上次成功 push 或 pull 的 commit」與 remote 目前的 HEAD 不是同一個 commit，則 push 會失敗並出現 conflict 提示。通常造成此現象的原因是有其他人在對 remote repo 做事，比如 push 新的 commit 到你現在要 push 的 remote branch 上。

### `git push -f`

強制 push 目前 local 的狀態到 remote，無視前面說的 [[#push 的原則]]。

-   可以理解為把 remote 的 `.git` folder 整包刪除，以目前要 push 上去的 `.git` folder 取代之，或者理解為 push 一個全新的專案取代掉原本的
-   可以在 GitHub 設定某 repo 的某 branch 要拒絕 force push，藉此[[保護 Branch]]

### 移除 `origin` 與 `<remote-repo-url>` 的對應關係

```bash
git remote remove origin
```

### 列出所有地端有的 Remote-Tracking References

```bash
git branch -r
```

Output 會像這樣：

```plaintext
remote/origin/master
remote/origin/dev
```

每一個 remote-tracking references 都用來代表一個 remote branch。

### 在 Local 刪除 Remote-Tracking References

```bash
git branch -rd origin/<remote-branch-name>
```

這個指令只是刪除 local 的 reference 而已，並不會刪到 remote 的 brach 本人。

### 刪除 Remote Branch (from Local)

>[!Danger]
>這個指令會實際刪除 remote 的 branch，也就是說你的 GitHub 上的 branch 會因為這樣就消失了。

```bash
git push origin -d <remote-branch-name>
```

指令中不用寫 `remotes/origin` 這個 prefix。

# `git fetch`

>將 remote repo 的最新狀態下載至 local。

```bash
# fetch 指定的 remote branch
git fetch origin <remote-brance-name>

# fetch 所有 remote branch
git fetch origin

# 也可以不寫 orign，效果與 git fetch origin 相同
git fetch
```

fetch 至 local 的 remote branch，git 會用形如 `origin/<remote-branch-name>` 的 remote-tracking reference 標記之，使用 `git branch -r` 可以查看。

### `git fetch --prune`

fetch 前會先檢查所有 local 的 remote-tracking reference，若有 reference 其指向的 remote branch 已經不存在，則將該 reference 刪除，完成上述動作後才進行 fetch。

### 把 Local 原本沒有的 Branch 從 Remote 拉過來

- **Step1: `git fetch origin <BRANCH_NAME>`**
- **Step2: `git checkout -b <BRANCH_NAME> FETCH_HEAD`**

# `git pull`

>將 remote repo 的最新狀態下載至 local，並將 local 的狀態更新為與 remote 一致。

`git pull` 其實就是 `git fetch` + `git merge`。

```bash
# fetch 指定的 remote branch 並 merge 至目前所在的 local branch
git pull origin <remote-branch-name>

# fetch 所有 remote branches 並 merge remote HEAD 所在的那個 branch 至目前所在的 local branch
git pull origin

# 也可以不寫 origin，效果與 git pull origin 相同
git pull
```

### Branch 間出現 Diverge

```plaintext
      A---B---C remote master
     /
D---E---F---G local master
    ^
    origin/master
```

若目前所在的 local branch 與準備 pull 的 remote branch 有 diverge 時（也就是 local 的 `origin/<remote-branch-name>` 與 remote 的 `<remote-branch-name>` 的 HEAD 不是同一個 commit），pull 會失敗，並且會出現警告。

要想 pull 這個 remote branch，必須這麼做：

- **Step1: 加上 option 來聲明要維持用 merge 的方式來合併，還是改用 rebase**

    ```bash
    # 維持用 merge 的方式來合併 remote branch
    git pull origin <remote-branch-name> --no-rebase
    
    # 改用 rebase
    git pull origin <remote-branch-name> --rebase
    ```

- **Step2: 手動解兩個 branch 間的 conflicts**

- **Step3: push merge/rebase 完的結果至 remote**

    - 採用 merge 的結果：

        ```plaintext
           A---B---C remote master|origin/master
          /         \
        D---E---F---G---H local master
        ```

        須要將 H push 至 remote。

        push 後：

        ```plaintext
           A---B---C
          /         \
        D---E---F---G---H local master|remote master|origin/master
        ```

    - 採用 rebase 的結果：

        ```plaintext
            remote master|origin/master
            ˇ
        D---E---A---B---C---F'---G'---H' local master
        ```

        須要將 F', G', H' push 至 remote。

        push 後：

        ```plaintext
        D---E---A---B---C---F'---G'---H' local master|remote master|origin/master
        ```

### 以 Remote Branch 的狀態為主

遇到 divergence 時，我們已知如果要以 local 的 branch 狀態為主，可以執行 `git push -f`，那如果要以 remote 的 branch 狀態為主呢？

**簡單版**

```bash
# Step1: Fetch the remote branch.
git fetch origin <remote-branch-name>

# Step2: Reset the local branch to the fetched branch.
git reset --hard origin/<remote-branch-name>
```

**複雜版**

```bash
# Step1: Fetch the remote branch.
git fetch origin <remote-branch-name>

# Step3: Re-create the local branch.
git checkout origin/<remote-branch-name>
git branch -D <local-branch-name>
git checkout -b <local-branch-name>

# Step4: Fast-forward merge the remote branch to this new local branch.
git merge origin/<remote-branch-name>
```
