# Piping - `|`

>[!Note]
>在了解 piping 之前，你會須要先了解 [[Operating System/Shell/Introduction#STDIN, STDOUT & STDERR|stdin, stdout & stderr]]。

`|` 稱為 pipe，用來連接兩個指令。會先執行左側指令，並將左側指令的 stdout 作為右側指令的 stdin，然後執行右側指令。

e.g.

```bash
echo "hello world" | grep "h"
# hello world
```

# Output Redirection - `>`

`>` 的左側會是完整的 command，右側則必須是一個 file，`>` 會將左側 command 的 stdout 導向（寫入）右側的 file。

e.g.

```bash
echo hello > myfile.txt
```

以上例而言，若直接執行 `echo hello`，shell 會將 hello 印在 terminal 上；加上 `>` 後，hello 會被導向並寫入 myfile.txt 這個檔案，所以此時 terminal 不會印出文字。

### Append Mode

若 redirect output 時不想要將檔案內容覆蓋，而是想將 stdout 加在原檔案內容的後面，則應使用 `>>` 取代 `>`：

```bash
touch myfile.txt

echo hello > myfile.txt
echo world >> myfile.txt

cat myfile.txt
# hello
# world
```

### 將 stdout 導向 stderr

使用 `>&` 搭配 [[Operating System/Shell/Introduction#File Descriptors (FD)|file descriptor]] 可以將 stdout 導向 stderr，比如：

```bash
echo hello 1>&2
```

也可以反過來將 stderr 導向 stdout，比如：

```bash
cat non-existing-file 2>&1 | tee -a test.txt
```

在上例中，如果只寫 `cat non-existing-file | tee -a test.txt`，在「`cat` 因找不到 non-existing-file 而 stderr」後，就不會繼續執行後面 `| tee -a test.txt` 的部分了。但若有 `2>&1`，shell 就會將 `cat` 的 stderr (`cat: non-existing-file: No such file or directory`) 寫入 test.txt 中。

### 將 stderr 導向黑洞

```sh
<COMMAND> 2> /dev/null
```

- /dev/null 是一個檔案，任何寫入這個檔案的東西都會直接消失
- `2> /dev/null` 的意思是只將 stderr 導向 /dev/null，stdout 仍然會印在 terminal 上

# Input Redirection - `<`

`<` 的左側會是完整的 command，右側則必須是一個 file，`<` 會把右側 file 的內容讀入 stdin，並把 stdin 導向左側的 command。

e.g.

```bash
pbcopy < myfile.txt
```

`COMMAND < FILE` 的效果與 `cat FILE | COMMAND` 是一樣的，唯一的差別是後者多一個尋找並執行 `cat` 執行檔的時間。

# 把指令丟到背景執行 - `&`

如果一個指令在執行時會佔用 process 一段時間，但你不想因此連 terminal 都被佔用，可以在指令後方加上 `&` 來把指令丟到背景執行：

```bash
sh myscript.sh &
```

# Chaining Commands

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
# some other scripts
echo "world"
```

### 有條件地接連執行指令 - `||`

一樣是用來將若干個指令串連，但與 `&&` 的不同處在於：只有前面的指令執行失敗時（產生一個非 0 的 [[Operating System/Shell/Introduction#Exit Codes|exit code]]），才會執行後面的指令。

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

# 參考資料

- <https://thoughtbot.com/blog/input-output-redirection-in-the-shell>
