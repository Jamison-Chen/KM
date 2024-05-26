# 學習資源

- [官方文件](https://git-scm.com/docs)
- <https://www.youtube.com/watch?v=Uszj_k0DGsg>

# Git 常用術語

|Terms|Description|
|---|---|
|repository (repo)|Git 所管理的對象的最大單位，是一個叫做 .git 的 folder，.git 所在的 directory 即被管理的單位的 root directory，repo 中可以有 sub-repo。|
|commit|「提交」檔案的最新狀態給 Git，也可以用作名詞，指的是一個「提交紀錄」，每個 commit 都是一個專案的「版本」。|
|HEAD|一個指標，用來記錄「目前」在哪個 commit 上。|
|working directory|檔案「目前」實際的狀態，又叫做 working tree。|
|staging area|存放「準備」被 commit 的檔案的地方，又叫做 index。|
|branch|分支。可以想成在 commit 上多貼一個標籤代表其所屬的 branch（一個 commit 可以有多個標籤）所有具有相同標籤的 commits 串連成一個 branch。|
|checkout|「切換」目前所在的 branch。|
|reset|「切換」目前所在的 commit。|
|merge|合併 branches。將某個 branch 的狀態合併進另一個 branch。|
|conflict|(檔案內容的) 衝突，一個檔案在兩個 branches 中的內容不一致。若要 merge 的兩個 branches 間有 conflict 就要解。|
|difference (diff)|(檔案內容的) 差異，一個檔案在兩個 commits 間的內容不一致，勿與 conflict 搞混。|
|cherry pick|把別的 branch 併進來時，只挑選部分 commits 合併，其餘採用自己的版本。|
|local|地端。也就是 repo 擁有者的電腦。|
|remote|遠端。大家可以在 local 向 remote 複製 (clone) repo，以及索取 (fetch) 或推送 (push) 最新的 repo 狀態。|
|push|將 repo 從 local 推送到 remote。|
|fetch|向 remote 索取 repo 的最新狀態至 local。|
|clone|將 repo 從 remote 複製一份到 local。|

# Version Control Systems

Git 是一個 Version Control Systems (VCSs, 版本控制系統)，VCSs 可以分為集中式 (centralized) 與分散式 (distributed)：

### Centralized VCSs (CVCSs)

所謂的 centralized，就是把檔案的所有版本存放在單一 server 的資料庫裡統一管理，clients (developers) 向這台 server 索取或存放特定的版本：

```mermaid
flowchart TD
    id1(Shared repository)
    id2(Developer1)
    id3(Developer2)
    id4(Developer3)
    id2 --> id1
    id3 --> id1
    id4 --> id1
```

其中一個有名的 CVCS 叫做 Subversion (SVN)。

CVCSs 的缺點：SPOF (single point of failure)。

### Distributed VCSs (DVCSs)

DVCSs 重點在於「所有 clients 都可以擁有完整的檔案歷史」，換句話說，每個 clients 的 local 都有一個記錄所有歷史的資料庫：

```mermaid
flowchart TD
    subgraph id1 [Server]
        id11(Version1)
        id12(Version2)
        id13(Version3)
        id11---id12
        id12---id13
    end
    subgraph id2 [Developer1]
        id21(Version1)
        id22(Version2)
        id23(Version3)
        id21---id22
        id22---id23
    end
    subgraph id3 [Developer2]
        id31(Version1)
        id32(Version2)
        id33(Version3)
        id31---id32
        id32---id33
    end
    subgraph id4 [Developer3]
        id41(Version1)
        id42(Version2)
        id43(Version3)
        id41---id42
        id42---id43
    end
    id2<-->id1
    id3<-->id1
    id4<-->id1
```

Git 即屬於 DVCS。

##### DVCSs 的優點

- 由於每個參與者的 local 都可以有完整的歷史，因此有越多人參與，檔案歷史被有心人士「完全」篡改的難度就越高
- 由於每個參與者的 local 都可以有完整的歷史，因此不用連上網就可以進行幾乎所有版本管理的操作

# Git

### Git 與 Linux Kernel

Git 的發明者同時也是 Linux kernal 的發明者：Linus Torvalds。Git 本來只是 Linus 在開發 Linux kernal 時，因為覺得當時既有的 VCS 太難用而開發的替代品（聽說他只花了 10 天…），後來逐漸被社群所接納。

### Git 與其他 VCS 最大的不同

多數 VCSs 通常是透過紀錄「每次的檔案變動 (differences)」來管理一個檔案的不同版本，但 Git 是透過「快照 (snapshot)」的方式來紀錄一個檔案每次被變更並提交 (commit) 後的樣子。

### .git Folder

每一個使用 Git 做版本控制的專案的 root directory 都會有一個名為 .git 的 folder，==.git folder 就是所謂的 repo==，所有與版本控制相關的資訊皆存放在 .git 裡，包括所有的 commits、branches… 等，所以==如果 .git 被刪了，所有歷史紀錄就都消失了==。

>[!Note]
>關於 .git folder 的更多細節，請見 [[The .git Folder]]。

### 一個 Commit 就是一個版本，Commits 間有順序

```mermaid
%%{init: { 'logLevel': 'debug', 'theme': 'base' } }%%
gitGraph
    commit
    commit
    commit tag: "HEAD"
```

### Git 如何確保 Data Integrity?

Git 每次儲存一個版本時，都會使用 SHA-1 演算法為這個版本計算出一個 hash value（動作稱為 **checksum**），計算的對象是這個版本的 repo 中「所有檔案的內容」，這個 hash value 是由 40 個 16 進制字元組成的字串，形如：

```plaintext
24b9da6552252987aa493b52f8696cd6d3b00373
```

這個 hash value 同時也是 commit 的編號。

只要任何檔案的內容有任何改動，checksum 的結果幾乎都會不一樣，發生 collision（不同檔案內容計算出相同 hash value）的機率極低（幾乎等於 0）。

### 📌 Working Directory, Staging Area & Repo

下圖為 working directory、staging area、local repo 與 remote repo 之間的關係：

```mermaid
sequenceDiagram
    Working Directory ->> Working Directory: modify
    Working Directory ->> Staging Area: fix stage
    Staging Area ->> Local Repo: commit
    Local Repo ->> Remote Repo: push
    Remote Repo ->> Local Repo: fetch
    Local Repo ->> Working Directory: checkout or merge
    Remote Repo ->> Working Directory: pull
```

>[!Question] 為什麼需要 Staging Area？
>由於我們並不會每次都想將「所有」本次對檔案的變動都 commit 為下一個版本，大多時候我們希望分批做 commit，staging area 就是用來分批的地方，每次 commit 都只會將 staging area 的內容 commit。

### 📌 檔案在 Git 裡的狀態

##### Untracked

一個檔案若存在於一個有用 Git 做版控的 working directory 中，但沒有被納入版控，則該檔案的狀態為 Untracked。「新增」與「在導入 Git 前就存在」的檔案，其狀態會是 untracked。

##### Modified

一個檔案在 working directory 的內容與 repo 裡最近一次的 commit 中的==內容不一致==，也==還沒被放進 staging area==。

##### Staged

一個檔案在 working directory 的內容與 repo 裡最近一次的 commit 中的==內容不一致==，但==已經被放進 staging area==，準備被 commit 為最新版本。

一個本來 **Untracked** 的檔案被加進 staging area 時，這個檔案會被額外標記為 **NewFile**。

##### Committed/Unmodified

檔案在 working directory 的內容與 repo 裡最近一次的 commit 中的==內容完全一致==。

##### Deleted

以下兩種狀態都算是 deleted：

1. **Deleted - Unstaged**

    檔案在最近一次的 commit 中存在，但卻不存在於現在的 working directory，且這個「消失」狀態還沒放進 staging area。

2. **Deleted - Staged**

    Staging area 顯示某檔案即將「脫離 Git 管控」，時機有以下兩種：

    - *1.* 所說的「消失」狀態被放進 staging area 後
    - 檔案沒有被實際刪除，而是使用者試圖讓某個本來被 Git 管理的檔案[脫離 Git 管控](</Tools/Git/L4 - Ignore.md>)，但還沒 commit，==這個狀態下的檔案同時會是 untracked==

##### Ignored

我們可以叫 Git 不要管專案中的某些檔案（或某子目錄下的所有檔案），不要管它們內容有沒有改變、也不要紀錄它們的變動歷史。==只有本來為 untracked 的檔案可以被 ignore==。

---

下面這張 FSM diagram 描繪了檔案狀態間的變換方式：

```mermaid
stateDiagram-v2
    c: Committed/Unmodified
    du: Deleted - Unstaged
    ds: Deleted - Staged
    dsu: Deleted - Staged, and Untracked
    [*] --> Untracked: Create a file
    Untracked --> Ignored
    Ignored --> Untracked
    Untracked --> Staged
    Modified --> Staged
    Staged --> c
    c --> Modified: Modify a file
    c --> dsu
    dsu --> Untracked
    c --> du: Delete a file
    du --> ds
    ds --> [*]
```

### 使用 Git 的基本工作流程

現在假設已經有一個使用 Git 的 repo，那麼一個基本的 workflow 會像是這樣：

```mermaid
flowchart TD
    id1(在 working directory 對一些檔案做修改)
    id2("將被修改的檔案加入 staging area")
    id3("將 staging area 的檔案狀態 commit 至 repo")
    id1-->id2
    id2-->id3
```

# GitHub

別把 Git 與 GitHub 搞混了，Git 是一個 VCS，而 GitHub 是一個網站，GitHub 主要提供的服務是一個雲端 Git server，也就是前面在[[#常用術語]]提到的 **remote** 的一種（其它提供類似服務的網站，包括 GitLab, Bitbucket, GitKraken… 等）。
