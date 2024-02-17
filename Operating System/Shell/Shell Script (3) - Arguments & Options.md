# Positional Arguments

### 傳入 Positional Arguments

假設今天輸入下面這個指令：

```bash
mycommand a b c d
```

指令中的 `mycommand` 是指令名稱，會是環境變數 `PATH` 中的某個路徑底下的一個名為 mycommand 的 shell script file，且該檔案的型態是一個[[File System#一般檔案 vs 執行檔|執行檔]]；而後面的 `a b c d` 則是要傳入 mycommand 的 arguments，arguments 由空格分割，所以這個例子共有四個參數，分別是字串 a, b, c 與 d。

### 讀取 Positional Arguments

- 可以用 `$1` 取得第一個參數的值、`$2` 取得第二個參數值，依此類推可以使用到 `$9`
- `$0` 是執行此 file 時所輸入的「路徑 + 檔名」

# Options

### 傳入 Options

e.g.

```bash
mycommand -a
```

上方範例指令中的 `-a` 就是 option，option 可以搭配 argument 使用，像是：

```bash
mycommand -a hello
```

### 讀取 Options

最常見的做法是使用 `getopts` 指令將所有 options 照順序讀入，再搭配 `while` loop 以及 `case` 來處理每個 option 及跟隨在後的 argument。一個完整的範例如下：

```bash
#!/usr/bin/env bash

Help() {
    echo
    echo "Syntax: scriptTemplate [-h|n]"
    echo -e "\th) Print this Help."
    echo -e "\tn) Print specific name."
    echo
}

name="world"

while getopts ":hn:" option; do
    case $option in
        h)
            Help
            exit;;
        n)
            name=$OPTARG;;
        \?)
            echo "Error: Invalid option"
            exit;;
    esac
done

echo "hello $name!"
```

- 使用 `$OPTARG` 讀取跟隨在 option 後的 argument
- `case` statement 中的每個 branch 的最後都必須是 `;;`

# 參考資料

- <https://www.redhat.com/sysadmin/arguments-options-bash-scripts>
