#Command

# 查看 File System 目前所使用的硬碟空間

```bash
df [{OPTION}] [{FILE}]
```

### 常用的 Options

- `-h`/`--human-readable`：讓儲存空間的單位自動進位（本來是固定為 KB）
- `-T`/`--print-type`：讓輸出值多一欄 file system 的 type

# 查看某目錄或檔案所佔用的硬碟空間

```bash
du -sh {DIRECTORY_OR_FILE}
```

# 列出目錄內容

```bash
ls [{OPTIONS}] [{PATH}]
```

- `-F` option：根據[檔案的類型](</Operating System/File System.md#檔案的類型>)在檔案名稱的結尾加上不同符號

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
|`@`|Soft link|
|沒有符號|一般檔案|

- `-R` option：Recursively 列出所有子目錄與檔案
- `-a` option：把隱藏（檔名以 `.` 開頭）的檔案也列出來
- `-l` option：顯示目錄底下每個檔案的詳細資訊，包括[7 - 與 Permission 相關的指令](</Operating System/Shell/7 - 與 Permission 相關的指令.md>)、owner… 等
- `-i` option：顯示目錄底下每個檔案的 [inode](</Operating System/File System.md#Inode (Index Node)>) number
- `{PATH}` 預設為 `.`

>[!Note] Wildcard
>可以使用 wildcard (`*`) 搭配檔名的片段來篩選要列出的檔案。
>
>舉例來說，`ls *.py` 會列出當前目錄中所有檔名以 `.py` 結尾的檔案。

# 取得目前的絕對路徑

```bash
pwd
```

pwd 是 print working directory 的縮寫。

# 切換目錄

```bash
cd {PATH}
```

- cd 是 change directory 的縮寫
- Path 間使用 `/` 前往下一層 directory
- `cd ..`：前往目前 directory 的上一層 directory
- `cd ~`：前往目前 user 的 home directory
- `cd /`：前往整台機器的 root directory
- `cd -`：回到上一個所在的 directory

# 建立新目錄

```bash
mkdir [-p] {PATH} [{PATH} ...]
```

- `{PATH}` 可以有多層

    比如 `mkdir test/test-sub`，但當有多層時，預設的行為是只有最後一層的 directory 會被建立，換句話說，path 中間的 directories 必須本來就存在，否則會報錯；若想要達到「若 path 中間的 directory 不存在，則一併建立」的效果，則須加上 `-p` option。

- `{PATH}` 可以有多個

    以空格分隔各個 `{PATH}`，效果是一次建立多個 directories，比如 `mkdir test01 test02` 就會一次建立 `test01` 與 `test02` 兩個 directories。

# 移動

### 「移動 directory」或「重新命名 directory」

```bash
mv {OLD_PATH_TO_DIR} {NEW_PATH_TO_DIR}
```

- 若 `{OLD_PATH_TO_DIR}` 不存在，則會報錯
- 若 `{NEW_PATH_TO_DIR}` 已存在，則將 `{OLD_PATH_TO_DIR}` 末端的 directory（及其底下所有東西）移到 `{NEW_PATH_TO_DIR}` 末端的 directory 底下
- 若 `{NEW_PATH_TO_DIR}` 不存在，則會將缺少的 directories 建立起來，並將 `{OLD_PATH_TO_DIR}` 末端的 directory（及其底下所有東西）移到 `{NEW_PATH_TO_DIR}` 的倒數第二層，並將移過來的 directory 重新命名為`{NEW_PATH_TO_DIR}` 末端的 directory name
- 若 `{NEW_PATH_TO_DIR}` 已存在，但不是一個 directory，則會報錯
- `{OLD_PATH_TO_DIR}` 與 `{NEW_PATH_TO_DIR}` 都可以是相對或絕對路徑

### 移動 file「並」重新命名

```bash
mv {OLD_PATH_TO_FILE} {NEW_PATH_TO_FILE}
```

- 將 `{OLD_PATH_TO_FILE}` 指定的 file 移到 `{NEW_PATH_TO_FILE}` 指定的 path 底下，並將該檔案重新命名為 `{NEW_PATH_TO_FILE}` 指定的 file name，若 `{OLD_PATH_TO_FILE}` 與 `{NEW_PATH_TO_FILE}` 指定的 path 一樣，則效果等同於原地重新命名檔案
- 若 `{OLD_PATH_TO_FILE}` 指定的 file 不存在，則會報錯
- 若 `{NEW_PATH_TO_FILE}` 指定的 file 已經存在，則會報錯
- `{OLD_PATH_TO_FILE}` 與 `{NEW_PATH_TO_FILE}` 都可以是相對或絕對路徑

### 移動 file

```bash
mv {PATH_TO_FILE} {PATH_TO_DIR}
```

- 若 `{PATH_TO_FILE}` 指定的 file 不存在，則會報錯
- 若 `{PATH_TO_DIR}` 指定的 directory 不存在，則會報錯

# 複製

```bash
cp [{OPTIONS}] {SRC} {DEST}
```

- `-r` option 複製目錄，r 代表 "recursively"
    - `{DEST}` 要包含複製出來的目錄名稱，但若該名稱在目的地已經被其它目錄使用了，`{SRC}` 就會被複製到那個已存在的目錄底下，並以原本的名稱為名
        - 以 `cp -r ~/src/ ~/Desktop/copied/` 為例，若 `~/Desktop/` 底下本來沒有名為 `copied` 的目錄，則這個指令的效果就是把 `~/src/` 複製到 `~/Desktop/` 底下，並命名為 `copied`；但若 `~/Desktop/` 底下本來已經有一個名為 `copied` 的目錄，則這個指令的效果就是把 `~/src/` 複製到 `~/Desktop/copied/` 底下，並且目錄名字維持為 `src`
        - 那如果想要達到「若目的地已有同名目錄存在，則用新目錄將其取代」的效果，該怎麼做呢？此時須要搭配 `-T` option（只有 Linux 的 `cp` 指令有 `-T` option）
- `-f` option 強制覆蓋既有檔案，f 代表 "force"，當 `{DEST}` 檔案已存在時，就直接將其刪除並把 `{SRC}` 複製過去

# 刪除

```bash
rm [{OPTIONS}] {FILE | DIR}
```

- `-r` option 只有在刪除目錄時會用到且必須用到，代表 "recursively"，也就是將所有目錄裡的東西都刪除

#TODO

# 建立檔案

```bash
touch {FILE}
```

若檔案已存在，則==不會==新增新的檔案把舊的檔案覆蓋掉，只會更新該檔案的 "last modified"。

>[!Note] 使用 `{}` 一次產生多個檔案
>
>- `touch hello{1, 2, 3}` 可以一次生成 hello1, hello2, hello3 三個檔案
>- `touch hello{1..10}` 可以一次生成 hello1 ~ hello10 十個檔案

# 顯示檔案內容

- 顯示檔案所有內容 - `cat`

    ```bash
    cat {FILE} [{FILE} ...]
    ```

    將檔案內容放到 stdout，若有多個 `{FILE}`，則會依序 stdout。

- 合併檔案內容 - `cat`

    搭配 `>` 就可以用來將多個檔案合併並寫入一個檔案中：

    ```bash
    cat {FILE_1} {FILE_2} [{FILE_3} ...] > {NEW_FILE}
    ```

- 顯示檔案內容，但一次只顯示一頁 - `more`

    ```bash
    more {FILE}
    ```

- 進階版的分頁 - `less`

    比 `more` 更好操作，可以使用滑鼠的 scroll 來前進後退。

>Less is more.

- 顯示檔案的開頭若干行內容 - `head`

    ```bash
    head [-n {LINE_NUM}] {FILE}
    ```

- 顯示檔案的結尾若干行內容 - `tail`

    ```bash
    tail [-n {LINE_NUM}] {FILE}
    ```

# 開啟檔案

```bash
xdg-open {FILE}
```

OS 會使用最適合的應用程式來開啟檔案，使用者可以爲每個檔案類型自訂要以哪個應用程式開啟。

>[!Note]
>MacOS 中沒有 `xdg-open` 這個指令，取而代之的是 `open`。

# 建立 Link

```bash
ln [-s] {SRC} {DEST}
```

- 若有 `-s` option，則建立的是 [soft link](</Operating System/File System.md#Soft (Symbolic) Links>)，否則為 [hard link](</Operating System/File System.md#Hard Links>)

# 參考資料

- <https://www.mropengate.com/2018/01/linuxunix-cheat-sheet-for-linuxunix.html>
