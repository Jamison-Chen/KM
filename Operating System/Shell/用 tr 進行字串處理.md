tr 代表 translate，這個指令專門用來將進行「字串處理」，主要擅長處理「尋找並刪除」、「尋找並替換」、「尋找並壓縮」三種任務。

# Input of `tr`

`tr` 指令須有 stdin，可以透過 [piping](</Operating System/Shell/3 - Operators.md#Piping - ``>) 或 [input redirection](</Operating System/Shell/3 - Operators.md#Input Redirection - `<`>) 兩種方式提供：

### Piping

Input 放 `tr` 前面。

e.g.

```bash
echo "hello world" | {TR_COMMAND}

cat test.txt | {TR_COMMAND}
```

### 使用 `<` 或 `<<<` Operator

- Input 放 `tr` 後面
- 若要直接以字串作為 stdin，須使用 `<<<`（請注意不是 `<<`）
- 若是要讀取某個檔案的內容作為 stdin，須使用 `<`

e.g.

```bash
{TR_COMMAND} < text.txt

{TR_COMMAND} <<< "hello world"
```

# 將 `tr` 的 stdout 寫入檔案

可以用 `>` 或 `>>` 對 `tr` 指令的 stdout 進行 [output redirection](</Operating System/Shell/3 - Operators.md#Output Redirection - `>`>)，比如：

```bash
{TR_COMMAND} <<< "hello world" > test.txt
```

# 刪除、替換、壓縮

### 尋找並刪除

```bash
tr -d {STR}
```

將所有出現在 input 中的 `{STR}` 刪除。

e.g. 消除 input 中的所有 "l"

```bash
tr -d l <<< "hello world"

# heo word
```

### 尋找並替換

```bash
tr {STR_1} {STR_2}
```

e.g. 將 input 中的所有 "l" 換成 "L"

```bash
tr l L <<< "hello world"

# heLLo worLd
```

### 尋找並壓縮

```bash
tr -s {STR}
```

e.g. 壓縮 input 中所有重複出現的空格

```bash
tr -s " " <<< "What   is   your        name?"

# What is your name?
```

# Set (集合)

上面關於 `tr` 的使用範例都是一次針對一個文字做刪除／替換／壓縮，不過其實一次可以針對屬於某個 set 內的所有 strings 做刪除／替換／壓縮。

當 argument 以 `":{CLASS}:"` 的形式表示時，該 argument 就是一個 set。

e.g. 將所有小寫的英文字母轉為大寫

```bash
tr "[:lower:]" "[:upper:]" <<< "hello world"

# HELLO WORLD
```

常用的 set 包括：

- `"[:alnum:]"`: 英文字母與數字
- `"[:alpha:]"`: 英文字母
- `"[:blank:]"`: 空格（包括 `" "` 與 `"\t"`）
- `"[:cntrl:]"`: [ASCII control characters](https://www.ascii-code.com/)
- `"[:digit:]"`: 數字
- `"[:lower:]"`: 小寫英文字母
- `"[:print:]"`: [ASCII printable characters](https://www.ascii-code.com/)
- `"[:space:]"`: 空格（包括 `" "` 與 `"\t"`）與換行（包括 `\n` 與 `"\r"`）
- `"[:upper:]"`: 大寫英文字母

# 參考資料

- <https://www.geeksforgeeks.org/tr-command-in-unix-linux-with-examples/>
