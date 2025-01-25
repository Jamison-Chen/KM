# Variables

Shell 就像大多程式語言一樣，可以設定變數，比如：

```bash
db=postgres
```

此時就有一個名稱為 `db` 的變數，其值為字串 "postgres"。

我們可以將變數放進任何指令中作為引數，比如使用 `echo` 印出變數的值：

```bash
echo $db
# or
echo ${db}
# or
echo "$db"
# or
echo "${db}"
```

- 上面四種寫法中，變數前方都有一個 `$`，其中 `${VAR}`、`"$VAR"`、`"${VAR}"` 是為了避免變數名稱與字串合在一起，比如若寫 `${hello}world` 則 `${hello}` 是變數、`world` 是字串；但若寫 `$helloworld` 則整個都是變數。
- 若使用 `"$VAR"`、`"${VAR}"` 這兩種寫法，則一定要寫雙引號 (`"`)，不能寫單引號 (`'`)。
- 變數名稱大小寫不拘。
- ==`=` 的左右兩側不能有空格==，因為寫 `a = b` 會被視為 `a`、`=`、`b` 三個分開的參數。
- 變數建立後，只有在當前的 Shell session 中有效，在 [subshell](</Operating System/Shell/1 - Introduction.md#Subshell>) 或離開 Shell session 後變數便不具意義了。
- 若希望某些變數在每次進入 Shell 時都被自動設定，則可以將那些變數寫在 [Shell 設定檔](</Operating System/Shell/1 - Introduction.md#Shell 設定檔>)中。
- 某些名稱的變數具有特殊意義，比如 `PATH`、`HOME`、`USER`、`SHELL`… 等，這些具有特殊意義的變數是[系統層級的環境變數](</Operating System/Shell/1 - Introduction.md#系統層級的環境變數>)。

### Environment Variables

Environment variable（環境變數）與一般變數（又叫 local variable）的差別在於：

- **定義的方式**

    定義環境變數時須在前方加上 `export`，例如：

    ```bash
    export PGDATABASE=postgres
    ```

- **變數的 scope**

    環境變數在當前的 Shell session 以及 [subshell](</Operating System/Shell/1 - Introduction.md#Subshell>) 都有意義；一般變數在 subshell 不具意義。

### 列出目前 Session 中的所有 Variables

```bash
# list all variables in the current session
declare

# list all functions in the current session
declare -f
```

### 列出目前 Session 中的所有 Environment Variables

```bash
printenv
```

### 變數的串接

e.g.

```bash
VAR=hello
VAR=world$VAR

echo $VAR  # worldhello
```

### 字串中的變數

普通的字串可以使用 `''` 或 `""` 包起來，但若要將變數塞在字串中，則一定要使用 `""`，否則無法解析變數：

```bash
VAR=hello

echo "$VAR world"  # hello world
echo '$VAR world'  # $VAR world
```

### 具有特殊意義的變數名稱

具有特殊意義的變數名稱都會以 `$` 開頭：

|Variable|Description|
|:-:|---|
|`$_`|上一個指令的最後一個參數值|
|`$?`|上一個指令的 exit code|
|`$@`|執行目前的 Shell script file 時所給的所有參數<br/>（看起來是一個 space-separated string，但其實是一個 array）|
|`$#`|執行目前的 Shell script file 時所給的參數的數量|
|`$$`|執行目前的 Shell script file 的 process ID|

### 將指令的輸出存成變數

e.g.

```bash
foo=$(pwd)

echo foo  # /Users/bob
echo "I'm now in $(pwd)"  # I'm now in /Users/bob
```

>[!Note] 延伸
>也可以使用 `<()` 將一個指令的輸出存進 virtual file，如果須要把某個指令的輸出餵給「只接收 file 作為 argument」的指令時，這個指令可以派上用場，比如：
>
>```bash
>cat <(echo hello)  # hello
>```

# Control Flow

```bash
if [ {CONDITION} ]; then
    {ACTION}
else
    {ACTION}
fi
```

常用的判斷式：

- `-n {STR}`: 字串 `{STR}` 的長度是否不為 0
- `-z {STR}`: 字串 `{STR}` 的長度是否為 0
- `{STR} -ge {NUM}`: 字串 `{STR}` 的長度是否大於等於數字 `{NUM}`

# Functions

#TODO

# Hashbang

一個 Shell script file 中的第一行會有一個類似註解但又不完全是註解的存在，這一行會長得像這樣：

```bash
#! /bin/bash
```

由於開頭是 `#!`，所以被稱為 hashbang。

Hashbang 的功能是提示 Shell 要使用哪個 interpreter 執行這個檔案。以上面的例子來說就是要使用 /bin 底下的 bash 來執行這份檔案。

>[!Note]
>之所以會需要用 hashbang 來提示 Shell 要使用哪個 interpreter 執行這個檔案，是因為執行[執行檔](</Operating System/File System.md#一般檔案 vs 執行檔>)的時候並不會在指令的開頭寫要使用哪個程式執行。

`#! /bin/bash` 這個寫法的 portability 其實還不夠好，因為萬一某台電腦的 bash 程式不是放在 /bin/bash 這個 path，就無法直接執行這個檔案。所以更好的寫法應該是「指定要用來執行此檔案的 program name，讓電腦自己從[環境變數 PATH](</Operating System/Shell/1 - Introduction.md#`PATH`>) 中搜尋這個程式放在哪裡」：

```bash
#! /usr/bin/env bash
```

/usr/bin/env 這個程式接收一個 argument，這個 argument 須為一個指令的名稱，/usr/bin/env 的功能就是去環境變數 `PATH` 中尋找以這個 argument 為名的執行檔。

>[!Note]
>應該比較少有電腦的 bash 的位置不是 /bin/bash，不過如果是其它 interpreter program 像是 python 就不好說了。

# 註解

使用 `#` 開頭的行會被視為註解。

# 換行

若覺得某一行太長，或是想要增加可讀性，可以使用 `\` 將 script 分行：

e.g.

```bash
# Without line break
docker run --rm -it -v $(pwd):/app -w /app --env-file local.env --entrypoint /bin/bash api-server:latest

# With line break
docker run --rm -it \
    -v $(pwd):/app \
    -w /app \
    --env-file .env \
    --entrypoint /bin/bash api-server:latest
```

# 參考資料

- <https://www.youtube.com/watch?v=kgII-YWo3Zw&list=PLyzOVJj3bHQuloKGG59rS43e29ro7I57J&index=3>
- <https://github.com/denysdovhan/bash-handbook/blob/master/README.md>
