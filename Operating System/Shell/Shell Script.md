# 變數

Shell 就像大多程式語言一樣，可以設定變數，比如：

```bash
db=postgres
```

此時就有一個名稱為 `db` 的變數，其值為字串 "postgres"。

若要印出變數的值，可以使用 `echo`，並且須在變數前方加一個 `$`，比如：

```bash
echo $db
```

- 變數名稱可以是大寫或小寫
- `=` 的左右兩側不能有空格，因為寫 `a = b` 會被視為 `a`、`=`、`b` 三個分開的參數
- 變數建立後，只有在當前的 shell session 有效，在 [[Operating System/Shell/Introduction#Sub-Shell|sub-shell]] 或離開 shell session 後變數便不具意義
- 若希望某些變數在每次進入 shell 時都被自動設定，則可以將那些變數寫在 [[Operating System/Shell/Introduction#Shell 設定檔|shell 設定檔]]中
- 某些名稱的變數具有特殊意義，比如 `PATH`, `HOME`, `USER`, `SHELL`… 等，這些具有特殊意義的變數是[[Operating System/Shell/Introduction#系統層級的環境變數|系統層級的環境變數]]

### Environment Variable

Environment variable（環境變數）與一般變數（又叫 local variable）的差別在於：

- **定義的方式**

    定義環境變數時須在前方加上 `export`，例如：

    ```bash
    export PGDATABASE=postgres
    ```

- **變數的 scope**

    環境變數在當前的 shell session 以及 [[Operating System/Shell/Introduction#Sub-Shell|sub-shell]] 都有意義；一般變數在 sub-shell 不具意義。

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

|變數|意義|
|:-:|:-:|
|`$_`|上一個指令的最後一個參數值|
|`$?`|上一個指令的 error code|
|`$@`|執行目前的 shell script file 時所給的所有參數<br/>（看起來是一個 space-separated string，但其實是一個 array）|
|`$#`|執行目前的 shell script file 時所給的參數的數量|
|`$$`|執行目前的 shell script file 的 process ID|

### 將指令的 Output 存成變數

e.g.

```bash
foo=$(pwd)

echo foo  # /Users/jamison
echo "I'm now in $(pwd)"  # I'm now in /Users/jamison
```

>[!Note] 延伸
>也可以使用 `<()` 將一個指令的 output 存成 virtual file，如果須要把某個指令的 output 餵給「只接收 file 作為 argument」的指令時，這個指令可以派上用場，比如：
>```bash
>cat <(echo hello)  # hello
>```

# Operators

### Piping - `|`

>[!Note]
>在了解 piping 之前，你會須要先了解 [[Operating System/Shell/Introduction#STDIN, STDOUT & STDERR|stdin, stdout & stderr]]。

`|` 稱為 pipe，用來連接兩個指令。會先執行左側指令，並將左側指令的 stdout 作為右側指令的 stdin，然後執行右側指令。

e.g.

```bash
echo "hello world" | grep "h"
# hello world
```

---

### Output Redirection - `>`

`>` 的左側會是完整的 command，右側則必須是一個 file，`>` 會將左側 command 的 stdout 導向（寫入）右側的 file。

e.g.

```bash
echo hello > myfile.txt
```

以上例而言，若直接執行 `echo hello`，shell 會將 hello 印在 terminal 上；加上 `>` 後，hello 會被導向並寫入 myfile.txt 這個檔案，所以此時 terminal 不會印出文字。

###### Append Mode

若 redirect output 時不想要將檔案內容覆蓋，而是想將 stdout 加在原檔案內容的後面，則應使用 `>>` 取代 `>`，例如：

```bash
echo hello > myfile.txt
echo world >> myfile.txt

cat myfile.txt
# hello
# world
```

###### 將 stdout 導向 stderr

使用 `>&` 搭配 [[Operating System/Shell/Introduction#File Descriptors (FD)|file descriptor]] 可以將 stdout 導向 stderr，也可以反過來將 stderr 導向 stdout，比如：

```bash
# redirect stdout to stderr
echo hello 1>&2

# redirect stderr to std out
cat non-existing-file 2>&1 | tee test.txt
```

在 `cat non-existing-file 2>&1 | tee test.txt` 這個例子中，如果只寫 `cat non-existing-file | tee test.txt`，在「`cat` 因找不到 non-existing-file 而 stderr」後，就不會繼續執行後面 `| tee test.txt` 的部分了；反之若有 `2>&1`，shell 就會將 `cat` 的 stderr (`cat: non-existing-file: No such file or directory`) 寫入 test.txt 中。

###### 將 stderr 導向黑洞

```sh
<COMMAND> 2> /dev/null
```

- `2>` 的意思是只將 stderr 導向右方的檔案，stdout 仍然會印在 terminal 上
- /dev/null 是一個檔案，任何寫入這個檔案的東西都會直接消失

---

### Input Redirection - `<`

`<` 的左側會是完整的 command，右側則必須是一個 file，`<` 會把右側 file 的內容讀入 stdin，並把 stdin 導向左側的 command。

e.g.

```bash
pbcopy < myfile.txt
```

`COMMAND < FILE` 的效果與 `cat FILE | COMMAND` 是一樣的，唯一的差別是後者多一個尋找並執行 `cat` 的時間。

---

### 將程式丟到背景執行 - `&`

如果一個指令在執行時會佔用 process 一段時間，但你不想因此連 terminal 都被佔用，可以在指令後方加上 `&` 來把指令丟到背景執行。

e.g.

```bash
sh myscript.sh &
```

---

### 有條件地接連執行指令 - `&&`

若將若干個指令用 `&&` 串連，則這些指令會「一個接著一個」被執行，只有前面的指令成功執行完畢才會執行後面的，否則就中斷。

```bash
echo "hello" && echo "world"
# hello
# world
```

這麼做的效果等同於在 shell script 中使用 `set -e` 讓 script 在遇到錯誤時就終止：

```bash
set -e
echo "hello"
echo "world"
```

### 有條件地接連執行指令 - `||`

一樣是用來將若干個指令串連，但與 `&&` 的不同處在於：只有前面的指令執行失敗時（產生一個非 0 的 error code），才會執行後面的指令。

e.g.

```bash
echo "hello" || echo "world"
# hello
```

因為有成功執行 `echo "hello"`，所以就不執行 `echo "world"`。

### 無條件地接連執行指令 - `;`

無論前方的指令發生什麼事，都會從頭到尾執行所有 commands：

```bash
echo "hello" ; echo "world"
# hello
# world

false ; echo "hi"
# hi
```

其實使用 `;` 的效果就和「不在開頭寫 `set -e` 的前提下」一行一行寫是一樣的。

# 在 Shell 中執行 Shell Script File

執行 shell script file 的指令有 `sh` 與 `source` 兩種：

- `sh`

    ```sh
    sh <FILE>
    ```

    若使用 `sh` 執行 shell script file，則會在當前的 shell session 中==另開一個 sub-shell== 來執行，因此 script 對 shell 環境的更動不會影響到 parent shell。

- `source`

    ```sh
    source <FILE>
    ```

    若使用 `source` 執行 shell script file，則會在當前的 shell session 中直接執行，因此 file 中對於 shell 環境的更動會影響到當前的 shell。

    可以把 `source` 當成其它語言中的 `import`，可以在一個 shell script file 中 `source` 另一個 shell script file，藉此載入變數或 function。

# Arguments of a Shell Script File

### 傳入參數

假設今天輸入下面這個指令：

```bash
mycommand a b c d
```

指令中的 `mycommand` 是指令名稱，會是環境變數 `PATH` 中的某個 path 底下的一個名為 mycommand 的 shell script file，且該 file 是一個[[File System#一般檔案 vs 執行檔|執行檔]]；而後面的 `a b c d` 是要傳入 mycommand 的參數，參數由空格分割，所以這個例子共有四個參數，分別是字串 a, b, c 與 d。

### 讀取參數值

- 在 shell script file 中，可以用 `$1` 取得第一個參數的值、`$2` 取得第二個參數值… 依此類推
- `$0` 是 file 的名稱（也就是 command 的名稱）

# 註解

使用 `#` 開頭的行會被視為註解。

# Hashbang

一個 shell script file 中的第一行會有一個類似註解但又不完全是註解的存在，這一行會長得像：

```bash
#!/bin/bash
```

由於開頭是 `#!`，所以被稱為 hashbang。

Hashbang 的功能是提示 shell 要使用哪個 interpreter 執行這個檔案。以上面的例子來說就是要使用 /bin 底下的 bash 來執行這份檔案。

>[!Note]
>之所以會需要用 hashbang 來提示 shell 要使用哪個 interpreter 執行這個檔案，是因為執行[[File System#一般檔案 vs 執行檔|執行檔]]的時候並不會在指令的開頭寫要使用哪個程式執行。

`#!/bin/bash` 這個寫法的 portability 其實還不夠好，因為萬一某台電腦的 bash 程式不是放在 /bin/bash 這個 path，就無法直接執行這個檔案。所以更好的寫法應該是「指定要用來執行此檔案的 program name，讓電腦自己從[[Operating System/Shell/Introduction#`PATH`|環境變數 PATH]] 中搜尋這個程式放在哪裡」：

```bash
#!/usr/bin/env bash
```

/usr/bin/env 這個程式接收一個 argument，這個 argument 須為一個指令的名稱，/usr/bin/env 的功能就是去環境變數 `PATH` 中尋找以這個 argument 為名的執行檔。

>[!Note]
>應該比較少有電腦的 bash 的位置不是 /bin/bash，不過如果是其他 interpreter program 像是 python 就不好說了。

# Exit Code

#TODO 

# 參考資料

- <https://www.youtube.com/watch?v=kgII-YWo3Zw&list=PLyzOVJj3bHQuloKGG59rS43e29ro7I57J&index=3>
- <https://thoughtbot.com/blog/input-output-redirection-in-the-shell>
- <https://github.com/denysdovhan/bash-handbook/blob/master/README.md>
