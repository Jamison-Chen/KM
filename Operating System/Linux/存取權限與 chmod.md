# 使用 `ls -l` 查看權限

使用 `ls -l` 可以查看當前 directory 中的所有 files 以及 subdirectory 的詳細資訊，其中就包含權限：

Example Output:

```plaintext
drwxrwxr-x  26 root  admin   832 Apr  3 22:38 Applications
drwxr-xr-x  67 root  wheel  2144 Mar 20 17:24 Library
drwxr-xr-x@ 10 root  wheel   320 Feb  9 17:39 System
drwxr-xr-x   5 root  admin   160 Mar 14 16:23 Users
dr-xr-xr-x   4 root  wheel  4804 Mar 15 11:27 dev
lrwxr-xr-x@  1 root  wheel    11 Feb  9 17:39 etc -> private/etc
.
.
.
```

其中每一行的結構如下：

![[Screenshot 2023-04-05 at 12.39.38 PM.png]]

### 常見的 Entry Types

- `-` $\to$ 一般檔案
- `d` $\to$ directory
- `l` $\to$ symbolic (soft) link（捷徑）
- `b` $\to$ 外接儲存裝置（如 USB）
- ...

# Permissions

針對任何一個 file 或 subdirectory，Linux 皆用九碼的 permission code 來表示所有人對它的存取權限，示意圖如下：

![[Screenshot 2023-04-05 at 2.45.04 PM.png]]

如上圖所示，九碼 permission code 又可以被切分為三個區段，三個區段分別代表三種不同身份，每個區段的三個 codes 分別代表該身份是否有讀、寫、執行某檔案的權限，若有，則會顯示英文字母 `r`/`w`/`x`，若沒有則會顯示 `-`。

舉例來說，如果某檔案的 permission code 為 `rwxr-xr-x`，就代表目前使用者有讀、寫、執行的權限；使用者所屬群組以及其他人則只有讀與執行的權限。

### 數字表示法

除了九碼 permission code，我們也常常使用 3 個數字來表示存取權限，3 個數字分別描述三本九碼 permission code 的三個區段（也就是三種身份的使用者）所擁有的檔案存取權限。換句話說，我們可以將每三個英文字母改用一個數字來表示，比如 `777`、`644` 等，以下介紹要如何轉換：

**Step1: 將 Permission Code 轉為二進制表示法**

我們先把目光聚焦在前三個英文字母（第一區段），已知三個區段不是出現固定的英文字母，就是出現 `-`，因此其實我們可以暫時改用 0/1 來取代它們，如果該位置出現字母就寫 1，出現 `-` 就寫 0，比如 `r-x`  就可以寫成 `101`，完整的範例如 `rwxr-xr-x` 就可以寫成 `111101101`。

**Step2: 將二進制轉為時進制**

由於每個區段長度為三，三位二進制可以表示十進制的 0~7，經過轉換後可以得到下面這張表：

|Permi. Code|`---`|`--x`|`-w-`|`-wx`|`r--`|`r-x`|`rw-`|`rwx`|
|-|-|-|-|-|-|-|-|-|
|數字|0|1|2|3|4|5|6|7|

# 更改權限

### `chmod` 設定權限

- **用數值設定：**

    `chmod <三位數值> <FILE/DIR>`

    e.g. `chmod 644 test.txt`

- **用 Permission Code：**

    `chmod <ROLE><OPERATOR><PERMI_CODE> <FILE/DIR>`

    - Role

        |`u`|`g`|`o`|`a`|
        |---|---|---|---|
        |使用者|群組|其他人|所有人（也可以什麼都不寫）|

    - Operator

        |`+`|`-`|`=`|
        |---|---|---|
        |增加權限|減少權限|重新定義權限|

    e.g. `chmod u-rx test.txt`、`chmod +x test.txt`

### `chown`、`chgrp` 變更擁有者及擁有群組

- **Pattern 1:** `chown <USER>[:<GROUP>] <FILE> [<FILE2> ...]`

- **Pattern 2:** `chown :<GROUP> <FILE>`

    這個 pattern 適用於只想變更所有群組時，其效果等同於 `chgrp <GROUP> <FILE>`。

- 搭配 `-R` option，可以變更 directory 及其底下的所有檔案及 sub-directories 的擁有者：

    ```bash
    chown -R <USER>[:<GROUP>] <DIR> [<DIR2 ...>]
    ```
