#Command 

# Inode (Index Node)

- Inode 是 Linux OS 用來儲存檔案 metadata 的資料結構
- Inode 所存放的 metadata 包括：
    - 存放檔案內容的 disk block 位置
    - 檔案類型
    - 最後修改時間
    - owner
    - 存取權限… 等
- 所有 inodes 約佔整個 file system 1% 的空間
- 一個 inode 存放一個檔案的 metadata，所以：
    - 每個檔案都有一個 inode number，可以用指令 `ls -i` 查看
    - 一個 file system 能儲存的檔案數量取決於 inode 數量
- Inode 不會紀錄檔名，是檔名指向 inode
    - 指向 inode 的東西被稱為該 inode 的 [[#Hard Links]]，所以檔名是一個 hard link

# 建立檔案的流程

```mermaid
flowchart TD
    id0("在當前目錄（父目錄）建立一個條目，命名為要新增的檔案名稱")
    id1("分配一個 inode，將要新增的檔案名稱指向這個 inode")
    id2("分配一塊儲存檔案內容的 disk block，將 block address 紀錄於 inode")
    id0 --> id1
    id1 --> id2
```

# Links

![[hard-link-and-soft-link.png]]

### Hard Links

- Hard link 是一個指向「檔案的 inode」的檔名／別名，所以指向同一個 inode 的所有 hard links 的 inode number 是相同的
- 其實原檔案本身的檔名也只是一個 hard link
- 指向同一個 inode 的 hard links A, B，由於控制的是同一份檔案內容，所以透過 A 打開檔案、修改內容並儲存後，再打開 B 就會看到修改過的內容
- 只有當指向同一個 inode 的所有 hard links 都被刪除時，該 inode 與其對應的 disk 儲存空間才會被釋出，所以一個 hard link 不會因為另一個 hard link 被刪除而失效

### Soft (Symbolic) Links

- Soft link 是一個指向原檔案的檔案
- 原檔案被刪除後，soft link 即失效
- Soft link 有自己的 inode，與原檔案的 inode 不同
- 開啟 soft link 時，實際上會開啟的是原檔案

### 建立連結

```sh
ln [-s] <SRC> <DEST>
```

若有 `-s` option，則建立的是 soft (symbolic) link，否則為 hard link。

# Directories

> Directory（目錄）也是一種檔案，打開目錄就是在讀取該目錄檔案。

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


### 列出目錄內容 - `ls`

```sh
ls [<OPTIONS>] [<PATH>]
```

- `ls -F`：根據檔案的類型在檔案名稱的結尾加上不同符號

    這裡的「檔案類型」就是 inode 中所記錄的檔案類型。

    Example output:

    ```plaintext
    Applications/  Volumes/  etc@      sbin/
    Library/       bin/      home@     tmp@
    System/        cores/    opt/      usr/
    Users/         dev/      private/  var@
    ```

    |符號|檔案類型|
    |:-:|:-:|
    |`/`|Directory|
    |`*`|執行檔|
    |`@`|[[#Soft (Symbolic) Links]]|
    |沒有符號|一般檔案|

- `ls -R`：Recursively 列出所有子目錄與檔案
- `ls -a`：把隱藏（檔名以 `.` 開頭）的檔案也列出來
- `ls -l`：顯示目錄底下每個檔案的詳細資訊，包括[[檔案存取權限]]、ower… 等
- `ls -i`：顯示目錄底下每個檔案的 inode number

若在 `ls` 後加上 `<PATH>`，則只會列出該 path 所指到的檔案資訊，舉例來說：

```bash
ls -l /usr/bin/vim
# -rwxr-xr-x  1 root  wheel  5320720 Sep  2 15:35 /usr/bin/vim
```

### 取得目前目錄位置 - `pwd`

pwd 是 print working directory 的縮寫，會印出目前所在目錄的絕對路徑。

```bash
pwd
```

### 切換目錄 - `cd`

cd 是 change directory 的縮寫。

```sh
cd <PATH>
```

- Path 間使用 `/` 前往下一層 directory
- `.` 代表目前的 directory
- `cd ..`：前往目前 directory 的上一層 directory
- `cd ~`：前往目前 user 的 home directory
- `cd /`：前往整台機器的 root directory
- `cd -`：回到上一個所在的 directory

### 建立新目錄

```sh
mkdir [-p] <PATH> [<PATH> ...]
```

- `<PATH>` 可以有多層

    比如 `mkdir test/test-sub`，但當有多層時，預設的行為是只有最後一層的 directory 會被建立，換句話說，path 中間的 directories 必須本來就存在，否則會報錯；若想要達到「若 path 中間的 directory 不存在，則一併建立」的效果，則須加上 `-p` option。

- `<PATH>` 可以有多個

    以空格分隔各個 `<PATH>`，效果是一次建立多個 directories，比如 `mkdir test01 test02` 就會一次建立 `test01` 與 `test02` 兩個 directories。

# Files & Directories

### 移動 - `mv`

- **「移動 directory」或「重新命名 directory」**

    ```sh
    mv <PATH_TO_DIR1> <PATH_TO_DIR2>
    ```

    - 若 `<PATH_TO_DIR1>` 指定的 directory 不存在，則會報錯
    - 若 `<PATH_TO_DIR2>` 指定的 directory 存在，則將 `<PATH_TO_DIR1>` 指定的 directory（及其底下所有東西）移到 `<PATH_TO_DIR2>` 底下
    - 若 `<PATH_TO_DIR2>` 指定的 directory 不存在，則將 `<PATH_TO_DIR1>` 指定的 directory（及其底下所有東西）移到 `<PATH_TO_DIR2>` 指定的 path，並重新命名為`<PATH_TO_DIR2>` 指定的 directory name
    - 若 `<PATH_TO_DIR2>` 指定的 directory 存在，但是是一個 file 而非 directory，則會報錯
    - `<PATH_TO_DIR1>` 與 `<PATH_TO_DIR2>` 都可以是相對或絕對路徑

- **移動 file 「並」重新命名**

    ```sh
    mv <PATH_TO_FILE1> <PATH_TO_FILE2>
    ```

    - 將 `<PATH_TO_FILE1>` 指定的 file 移到 `<PATH_TO_FILE2>` 指定的 path 底下，並將該檔案重新命名為 `<PATH_TO_FILE2>` 指定的 file name，若 `<PATH_TO_FILE1>` 與 `<PATH_TO_FILE2>` 指定的 path 一樣，則效果等同於原地重新命名檔案
    - 若 `<PATH_TO_FILE1>` 指定的 file 不存在，則會報錯
    - 若 `<PATH_TO_FILE2>` 指定的 file 已經存在，則會報錯
    - `<PATH_TO_FILE1>` 與 `<PATH_TO_FILE2>` 都可以是相對或絕對路徑

- **移動 file**

    ```sh
    mv <PATH_TO_FILE> <PATH_TO_DIR>
    ```

    - 若 `<PATH_TO_FILE>` 指定的 file 不存在，則會報錯
    - 若 `<PATH_TO_DIR>` 指定的 directory 不存在，則會報錯

### 複製 - `cp`

將指定檔案或目錄複製到指定位置。

```sh
cp [<OPTIONS>] <SRC> <DEST>
```

###### 常用 Options

- `-r` 只有在複製目錄時會用到，代表 "recursively"，也就是所有目錄裡的東西都複製
- `-f` 只有在複製檔案時會用到，代表 "force"，當指定的 `<DEST>` 檔案無法開啟時，就直接將其刪除並把 `<SRC>` 複製過去

### 刪除 - `rm`

```sh
rm [<OPTIONS>] <FILE | DIR>
```

#TODO 

# Files

### 建立檔案 - `touch`

```sh
touch <FILE>
```

若檔案已存在，則==不會==新增新的檔案把舊的檔案覆蓋掉，只會更新該檔案的 "last modified"。

### 顯示檔案內容

###### 顯示檔案所有內容 - `cat`

```sh
cat <FILE> [<FILE> ...]
```

將檔案內容放到 stdout，若有多個 `<FILE>`，則會依序 stdout。

###### 合併檔案內容 - `cat`

搭配 `>` 就可以用來將多個檔案合併並寫入一個檔案中：

```sh
cat <FILE_1> <FILE_2> [<FILE_3> ...] > <NEW_FILE>
```

###### 顯示檔案內容，但一次只顯示一頁 - `more`

```sh
more <FILE>
```

###### 顯示檔案的開頭若干行內容 - `head`

```sh
head [-n <LINE_NUM>] <FILE>
```

###### 顯示檔案的結尾若干行內容 - `tail`

```sh
tail [-n <LINE_NUM>] <FILE>
```

# 參考資料

- <https://www.mropengate.com/2018/01/linuxunix-cheat-sheet-for-linuxunix.html>
- <https://zh.wikipedia.org/zh-tw/Inode>
