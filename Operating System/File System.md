>[!Info]
>本文旨在介紹作業系統中的 file system，但不包括相關指令，若要查看與 file system 相關的指令，請見[本文](</Operating System/Shell/9 - 與 File System 相關的指令.md>)。

# 基礎觀念

### 1. Everything is a File in Linux

包括一般檔案、links、directories、sockets、processes、硬體裝置... 這些東西在 Linux OS 中都是以檔案的形式存在。

### 2. File Names are Case-Sensitive in Linux

在 Linux 中，檔案名稱是 case-sensitive 的，也就是說 `test` 與 `Test` 對系統來說是兩個不同的檔名，可以同時存在在同一個 directory 底下；但在 MacOS 以及 Windows 中，檔案名稱是 case-insensitive 的，所以 `test` 及 `Test`、`TEST`… 等都會被視為相同的檔名，不能同時存在於同一個 directory 底下。

### 3. File System 分為 Data Blocks 與 Inodes 兩部分

Inode 存放檔案的 meta data；data block 則存放檔案內容。

# File System 的種類

依「儲存檔案的方式」可以將 file systems 分為以下幾類：

- [#Disk File Systems](</./Operating System/File System.md#Disk File Systems>)
- Flash file systems：使用 flash memory（快閃記憶體）儲存檔案的檔案系統
- Tape file systems：使用 tape（磁帶）儲存檔案的檔案系統
- Database file systems：使用 database（資料庫）儲存檔案的檔案系統（不要跟 [flat-file database](</Database/0 - Introduction.md#Flat-File Database>) 搞混了，flat-file database 是「用檔案當作資料庫」）
- [#Network File Systems](</./Operating System/File System.md#Network File Systems>)

### Disk File Systems

- 使用 disk（硬碟）儲存檔案的檔案系統。
- 在 Linux OS 中常見的 disk file systems 包括 XFS, ext4 等。

### Network File Systems

這種 file system 只是一個 interface/client，它和其它檔案系統一樣可以新增／編輯／刪除／移動檔案／目錄，但實際上是將這些檔案分散在網路中的各個 nodes (servers)，client 與 servers 再透過網路通訊完成以上操作。

其實這就是所謂的「分散式檔案系統」。

# Inode (Index Node)

- Inode 是 Linux OS 用來儲存檔案 metadata 的資料結構
- Inode 所存放的 metadata 包括：
    - 存放檔案內容的 disk block 位置
    - 檔案大小
    - 檔案類型
    - 建立時間、最後寫入時間、最後讀取時間
    - Owner
    - 存取權限
- 所有 inodes 約佔整個 file system 1% 的空間
- 每個檔案都有一個唯一的 inode number，這個編號是 ==system-wide== 的，可以用指令 `ls -i` 查看
- 一個 file system 能儲存的檔案數量取決於 inode 數量，在某些不能動態調整 inode 空間的 file system 中，有可能發生「disk 還有空間，卻無法新增檔案」的情況
- Inode 不會紀錄檔名，是檔名指向 inode
    - 指向 inode 的東西被稱為該 inode 的 [#Hard Links](</./Operating System/File System.md#Hard Links>)，所以檔名是一個 hard link
- 一個檔案在同一個 file system 內移動時，其 inode number 不變，但儲存檔案內容的 disk block「可能」會變

# File Descriptors (FD)

File descriptors 就是檔案、[socket](</Network/Socket & Port.md#Socket>)、input/output resource 的編號，與 inode number 不一樣的地方在於：inode number 是 system wide 的；FD 則是 ==per process== 的。換句話說，FD 只有對它所屬的 process 來說有意義，FD 出了 process 就沒意義了。

FD 會由小到大分配，每存取到一個檔案就必須分配一個 FD 給它，每個 process 一定都有最基本的三個 FD，分別是「輸入 (Standard Input)」、「輸出 (Standard Output)」與「錯誤 (Standard Error)」，根據 [POSIX standard](https://pubs.opengroup.org/onlinepubs/9699919799/functions/stdin.html) 的規定，`stdin`、`stdout`、`stderr` 的編號分別是 `0`、`1`、`2`。

一個 FD 只能指向一個檔案 (inode)，但同一個檔案即使在同一個 process 內也可以有多個 FDs 指向它；不同 processes 存取同一個檔案時，則是 processes 各自的 FDs 指向同一個 inode。但其實在 FD 與 inode 間還有一層叫 open file table 的東西：

### Open-File Descriptions

Open-file description 使用 ==system-wide 的 open-file table== 紀錄每個 process 正在存取哪些檔案，當 process 存取某個檔案時，會先在 open-file table 中建立一個 entry，裡面的資訊會包含檔案的 inode number，該 process 的 FD 則會記錄 open-file table entry 的 id。所以其實是 FD 指向 open-file description，open-file description 才指向 inode，如下圖：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/file-descriptor-open-file-description-inode.png>)

- Open-file table 中的 file offset 表示「從第幾個 ch開始存取這個檔案」
- 在一個 process 中可以複製 FD，此時不同的 FD 會指向同一個 open-file table entry
- 不同 processes 間也可以複製 FD，此時也是不同的 FD 會指向同一個 open-file table entry
- 不同 processes 間如果不是透過複製 FD，而是各自打開同一個檔案的話，則各自的 FD 就會指向不同的 open-file table entries，但這些 open-file table entries 會指向同一個 inode

# File

### 建立檔案的流程

```mermaid
flowchart TD
    id0("在當前目錄（父目錄）建立一個條目，命名為要新增的檔案名稱")
    id1("分配一個 inode，將要新增的檔案名稱指向這個 inode")
    id2("分配一塊儲存檔案內容的 disk block，將 block address 紀錄於 inode")
    id0 --> id1
    id1 --> id2
```

### 檔案的類型 (Entry Types)

這裡的「檔案類型」就是 inode 中所記錄的檔案類型，下方為 Linux 中的所有檔案類型，以及 `ls -l` 時對應的符號：

|符號|檔案類型|
|:-:|:-:|
|`-`|一般檔案或執行檔|
|`d`|Directory|
|`l`|Soft (Symbolic) Links|
|`b`|外接儲存裝置（如 USB）|
|`c`|Character 裝置|
|`p`|Pipe file|
|`s`|Socket file|

### 一般檔案 vs. 執行檔

若一個 user 對一個一般檔案有 [execute 的權限](</Operating System/Shell/7 - 與 Permission 相關的指令.md>)，則該檔案對該 user 來說就是一個執行檔。

User 可以直接在 [[Operating System/Shell/1 - Introduction|Shell]] 中輸入執行檔的檔名來執行該檔案，比如若要執行一個位在當前目錄的名為 myscript 的執行檔，則須輸入：

```bash
./myscript
```

>[!Note]
>即使執行檔位在當前目錄，也須要在檔名前面加上 `./`，因為若單純輸入檔名，會被 Shell 認為是一個 command，此時 Shell 只會從 [[Operating System/Shell/1 - Introduction#`PATH`|PATH]] 這個環境變數中所列的 paths 中尋找執行檔，反而不會找當前的目錄。

由於是透過 Shell 執行，所以==執行檔的內容通常都會用 Shell script 撰寫==，但若檔案內容的第一行有使用 [[2 - Shell Script Overview#Hashbang|hashbang]] 提示 Shell 要使用哪個 interpreter 執行這個檔案，則內容就可以是該 interpreter 所能解析的程式語言。

一個一般檔案在還沒有變成執行檔前，若使用 `open` 指令打開，OS 會使用文字編輯器打開這個檔案；但若這個檔案變成一個執行檔，則 `open` 指令會觸發 OS 使用 [[CLI vs. Terminal vs. Console vs. Shell#Terminal|terminal emulator]] + Shell 直接執行檔案中的 script。

新建一個檔案時，所有 users 對該檔案都不會有 execute 的權限（即使是建立它的 user 也只會有 read 跟 write 權限），所以該檔案對所有 users 來說都只是一個「一般檔案」，若要讓該檔案成為一個執行檔，則須使用 [chmod](</Operating System/Shell/7 - 與 Permission 相關的指令.md#用 Permission Code 設定>) 指令改變權限，比如：

```bash
chmod u+x myscript
```

# Link

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/hard-link-and-soft-link.png>)

### Hard Link

- Hard link 是一個指向「檔案的 inode」的檔名／別名，所以指向同一個 inode 的所有 hard links 的 inode number 是相同的
- 其實原檔案本身的檔名也只是一個 hard link
- 指向同一個 inode 的 hard links A, B，由於控制的是同一份檔案內容，所以透過 A 打開檔案、修改內容並儲存後，再打開 B 就會看到修改過的內容
- 只有當指向同一個 inode 的所有 hard links 都被刪除時，該 inode 與其對應的 disk 儲存空間才會被回收並釋出，所以一個 hard link 不會因為另一個 hard link 被刪除而失效
- 現代的 file system 大多禁止對 directory 建立 hard link
- Hard link 不能跨 file system（無法在一個 file system 中建立另一個 file system 中的檔案的 hard link）

### Soft (Symbolic) Link

- Soft link 是一個指向原檔案的檔案名稱的檔案
- 原檔案被刪除後，soft link 會因為找不到名為原檔案名稱的檔案而失效
- Soft link 有自己的 inode，與記錄原檔案的 inode 不同
- 可以對 directory 建立 soft link
- Soft link 可以跨 file system（可以在一個 file system 中建立另一個 file system 中的檔案的 soft link）
- 透過 soft link 開啟檔案的流程：

```mermaid
flowchart TD
    id0("找到該 soft link 所指向的原檔案名稱")
    id1("找到原檔案名稱所指向的 inode")
    id2("讀取該 inode 所指向的 disk block")
    id0 --> id1
    id1 --> id2
```

# Directory

Directory（目錄）也是一種檔案，打開目錄就是在讀取該目錄檔案。

### 建立目錄的流程

由於目錄也是一種檔案，所以建立目錄的流程與建立檔案的流程很像，只是多了最後一個步驟：

```mermaid
flowchart TD
    id0("在當前目錄（父目錄）建立一個條目，命名為要新增的目錄名稱")
    id1("分配一個 inode，將要新增的目錄名稱指向這個 inode")
    id2("分配一塊用來儲存新目錄底下的檔案與子目錄的 disk block，<br/>將 block address 紀錄於 inode")
    id3("在新目錄底下新增兩個子目錄條目，分別為 . 與 ..")
    id0 --> id1
    id1 --> id2
    id2 --> id3
```

### `.` 與 `..`

建立一個目錄時，OS 會在該目錄底下自動建立 `.` 與 `..` 兩個子目錄：

- `.` 的 inode number 就是目錄本人的 inode number，所以一個目錄底下的 `.` 就是目錄自己的其中一個 hard link
- `..` 的 inode number 是目錄的父目錄的 inode number，所以一個目錄底下的 `..` 就是目錄的父目錄的其中一個 hard link

>[!Note] 一個目錄的 hard links 數量 = 該目錄底下的子目錄數 (n) + 2
>- 目錄底下的每個子目錄會有 `..` 來指向目錄的 inode (n)
>- 目錄自己有 `.` 指向自己的 inode (1)
>- 目錄的父目錄底下會有一個條目（就是目錄的名字）指向目錄的 inode (1)

# 參考資料

- <https://en.wikipedia.org/wiki/File_system>
- <https://zh.wikipedia.org/zh-tw/Inode>
- <https://kkc.github.io/2020/08/22/file-descriptor/>
- <https://www.lenovo.com/us/en/glossary/file-descriptor/>
