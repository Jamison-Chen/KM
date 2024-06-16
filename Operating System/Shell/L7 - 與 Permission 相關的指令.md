#Command 

# 查看檔案／目錄權限

```bash
ls -l
```

`ls -l` 用來查看當前目錄中的所有檔案與子目錄的詳細資訊，其中就包含權限。

Example output:

```plaintext
drwxrwxr-x  26 root  admin   832 Apr  3 22:38 Applications
drwxr-xr-x  67 root  wheel  2144 Mar 20 17:24 Library
drwxr-xr-x@ 10 root  wheel   320 Feb  9 17:39 System
drwxr-xr-x   5 root  admin   160 Mar 14 16:23 Users
dr-xr-xr-x   4 root  wheel  4804 Mar 15 11:27 dev
lrwxr-xr-x@  1 root  wheel    11 Feb  9 17:39 etc -> private/etc
```

其中每一行的結構如下：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/ls-l-output-structure.png>)

>[!Info]
>本文不會介紹 entry type，若想了解 entry type，請見 [File System](</Operating System/File System.md#檔案的類型 (Entry Type)>)。

# 權限的表示方式

針對任何一個檔案／子目錄，Linux OS 皆用九碼的 permission code 來表示所有人對它的存取權限，permission code 的結構如下：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/unix-permission-expression.png>)

如上圖所示，九碼 permission code 可以被切分為三個區段，三個區段分別代表「使用者」、「使用者群組」、「其他人」三種不同身份，每個區段的三個 codes 分別代表該身份是否有讀、寫、執行某檔案的權限：

- 顯示英文字母 `r` (read) /`w` (write) /`x` (execute) → 有權限
- 顯示 `-` → 沒有權限

舉例來說，如果某檔案的 permission code 為 `rwxr-xr-x`，就代表：

- 目前使用者有讀、寫、執行的權限
- 目前使用者所屬群組只有讀與執行的權限
- 其他人也只有讀與執行的權限

### 數字表示法

除了九碼 permission code，我們也常常使用 3 個數字來表示存取權限，3 個數字分別描述 permission code 的三個區段（也就是三種身份的使用者）所擁有的檔案存取權限。換句話說，我們可以將每三個英文字母改用一個數字來表示，比如 `777`、`644` 等。轉換方式如下：

##### Step1: 將 permission code 轉為二進制表示法

我們先把目光聚焦在前三個英文字母（第一區段），已知三個區段不是出現固定的英文字母，就是出現 `-`，因此其實我們可以暫時改用 0/1 來取代它們，如果該位置出現字母就寫 1，出現 `-` 就寫 0，比如 `r-x`  就可以寫成 `101`，完整的範例如 `rwxr-xr-x` 就可以寫成 `111101101`。

##### Step2: 將二進制轉為十進制

由於每個區段長度為三，三位二進制可以表示十進制的 0~7，經過轉換後可以得到下面這張表：

|Code|`---`|`--x`|`-w-`|`-wx`|`r--`|`r-x`|`rw-`|`rwx`|
|---|---|---|---|---|---|---|---|---|
|**Number**|0|1|2|3|4|5|6|7|

所以 `rwxr-xr-x` 就可以寫成 `755`。

### 什麼是對目錄的 read/write/execute 權限？

- User 必須對一個目錄有 read 的權限，才可以用 `ls` 查看該目錄底下有哪些檔案與子目錄
- User 必須對一個目錄有 write 的權限，才可以的對該目錄底下的檔案與子目錄進行 rename、delete，也可以新增檔案與子目錄

    >[!Note]
    >即使你擁有一個檔案的所有權限，只要你沒有該檔案所在目錄的 write 權限，你就無法刪除該檔案。

- User 必須對一個目錄有 execute 權限，才可以 `cd` 至該目錄，以及執行該目錄底下的檔案與子目錄

    >[!Note]
    >要想執行某個檔案，必須擁有該檔案的所有 ancestor directories 以及檔案本身的 execute 權限。

# 使用 `chmod` 設定權限

### 用數值設定

```sh
chmod <三位數值> <FILE_OR_DIR>
```

e.g.

```bash
chmod 644 test.txt
```

### 用 Permission Code 設定

```sh
chmod <ROLE><OPERATOR><PERMI_CODE> <FILE_OR_DIR>
```

`<ROLE>` 包括：

|`u`|`g`|`o`|`a`|
|---|---|---|---|
|使用者|群組|其他人|所有人（也可以什麼都不寫）|

`<OPERATOR>` 包括：

|`+`|`-`|`=`|
|---|---|---|
|增加權限|減少權限|重新定義權限|

e.g.

```bash
chmod u-rx test.txt

chmod +x test.txt
```

# 變更檔案／目錄擁有者及擁有群組

### 變更擁有者與擁有群組

```sh
chown <USER>[:<GROUP>] <FILE> [<FILE2> ...]
```

搭配 `-R` option，可以變更 directory 及其底下的所有檔案及 sub-directories 的擁有者：

```sh
chown -R <USER>[:<GROUP>] <DIR> [<DIR2 ...>]
```

### 只變更擁有群組

```sh
chown :<GROUP> <FILE> [<FILE2> ...]
```

效果等同於：

```sh
chgrp <GROUP> <FILE>
```
