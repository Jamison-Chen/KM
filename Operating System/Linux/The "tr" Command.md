tr 代表 translate，這個指令專門用來將進行「字串處理」，主要擅長處理「尋找並刪除」、「尋找並替換」、「尋找並壓縮」三種任務。

由於這個 command 需要接收 input string 才知道要處理什麼，因此在介紹如何執行上述三種任務前，我們先來看看要如何輸入資料：

# Input Data

`tr` 與其他指令較不相同的地方是：一定要有 input。Input 可以透過以下兩種方式餵入：

### 一、使用 `|` operator，input 放 `tr` 前面

使用這種方法為入的 input 可以是 `echo` 指令的 output，也可以是 `cat` 指令讀入的檔案內容，舉例而言：

- `echo "hello world" | <TR_COMMAND>`
- `cat test.txt | <TR_COMMAND>`

### 二、使用 `<` 或 `<<<` operator，input 放 `tr` 後面

當要直接輸字串作為 input 時，必須搭配 `<<<` 使用；若是要讀取某個檔案的內容作為 input，則是搭配 `<` 使用，舉例而言：

- `<TR_COMMAND> < text.txt`
- `<TR_COMMAND> <<< "hello world"`

# 寫入檔案

與 `echo` 指令類似，`tr` 所 output 的結果不只能印在 terminal 上，也可以透過 `>` 與 `>>`
operators 寫入檔案，指令形如：

```bash
<TR_COMMAND> <<< "hello world" > test.txt
```

關於 `>` 與 `>>` 的用途與差異，詳見 [[常用指令#`echo <STR>`|echo]]。

# 刪除、替換、壓縮

### 尋找並刪除

**Pattern:** `tr -d <S1>`

將所有出現在 input 中的 `<S1>` 刪除。

e.g. 消除 input 中的所有 "l"

```bash
tr -d l <<< "hello world"
```

Output

```plaintext
heo word
```

### 尋找並替換

**Pattern:** `tr <S1> <S2>`

e.g. 將 input 中的所有 "l" 換成 "L"

```bash
tr l L <<< "hello world"
```

Output

```plaintext
heLLo worLd
```

### 尋找並壓縮

**Pattern:** `tr -s <S1>`

e.g. 壓縮 input 中所有重複出現的空格

```bash
tr -s " " <<< "What   is   your        name?"
```

Output

```plaintext
What is your name?
```

# Set (集合)

上面關於 `tr` 的使用範例都是一次針對一個文字做刪除／替換／壓縮，不過其實一次可以針對屬於某個 set 內的所有 strings 做刪除／替換／壓縮。

當 argument `<S1>` 以 `":<CLASS>:"` 的方法表示時，`<S1>` 就是一個 Set，舉例來說：

```bash
tr "[:lower:]" "[:upper:]" <<< "hello world"
```

上方指令會將所有小寫的英文字母轉為大寫，因此 output 為：

```plaintext
HELLO WORLD
```

常用的 Set 包括：

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
