pdb 是 Python 內建的 debugger。

>[!Info] 官方文件
><https://docs.python.org/3/library/pdb.html>

# 埋設 Breakpoints

### 法一：`import pdb` + `pdb.set_trace()`

e.g.

```Python
import pdb

print("Hello")
pdb.set_trace()
print("World")
```

上方程式碼的意思是要設置 breakpoint 在 `print("World")` 這行，所以程式會暫停在 `print("World")` 之前。

### 法二：`breakpoint()`

>[!Note]
>此方法只適用於 Python 3.7 以後的版本，在這些版本中，`breakpoint()` 是 built-in function。

e.g.

```Python
print("Hello")
breakpoint()
print("World")
```

### 法三：Post-Mortem Debugging

這個方法適用在你不想或無法更改 source code 時：

```bash
python -m pdb {FILE_NAME}.py
```

進入 post-mortem 模式後，使用 `b {LINE_NUMBER}` 設置 breakpoint 在第 `{LINE_NUMBER}` 行（其它指令請見[[#Debugger Commands|此段]]）。

---

有了 breakpoints 後，執行 Python script 時若遇到 breakpoint 就會暫停，並且印出目前停下來的位置（breakpoint 設置的位置），然後出現 `(Pdb)` 提示字樣在 terminal 行首：

```plaintext
> /Users/test.py(3)<module>()
-> print("World")
(Pdb) 
```

輸入 `c` 然後按 `Enter` 可以繼續（其它指令請見[此段](</./Programming Language/Python/pdb - The Python Debugger.md#Debugger Commands>)）。

# Debugger Commands

[官方文件](https://docs.python.org/3/library/pdb.html#debugger-commands)有詳細說明所有 pdb 中可以使用的 commands，這裡僅列出常用的：

|Command|Description|
|---|---|
|`b {LINE_NUMBER}`|在第 `{LINE_NUMBER}` 行設置 breakpoint。|
|`n`/`next`|到下一行。|
|`c`/`cont`/`continue`|繼續執行 code，直到下次遇到 breakpoint 為止。|
|`r`/`return`|繼續執行 code，直到目前所在的 function return 為止。|
|`p {EXPRESSION}`|stdout `{EXPRESSION}`，主要用途是拿來檢視目前各個變數的值。|
|`q`/`quit`|離開 debugger 模式。|
