Machine code 又叫做 machine language、binary code，是一連串人類無法解讀、但 CPU 看得懂的 0/1 組合。

Machine code 的一個指令為 32 bits，指令分 R-type, I-type, J-type 三種，結構如下：

```plaintext
   6      5     5     5     5      6 bits
[  op  |  rs |  rt |  rd |shamt| funct]  R-type
[  op  |  rs |  rt | address/immediate]  I-type
[  op  |        target address        ]  J-type
```

# Bytecode vs Machine Code

- Bytecode 是介於 machine code 與 source code 的 intermediate representation (IR)，它和 machine code 一樣是 0/1 的組合，但是 CPU 看不懂，需要特定的 virtual machine (VM) 將 bytecode 轉譯 (interpret) 成 machine code 再交給 CPU 執行
- Bytecode 又被稱為 p-code (p for "portable")，強調其可以跨平台執行
    - 前提是目標平台上有可以 interpret 該 bytecode 的 VM（所以其實也沒有那麼 portable）
- 其實狹義的 "interpreter"（比如 Python 中的 CPython）只負責把 source code 轉成 bytecode，後面的工作是 VM 負責的；但[廣義的 interpreter](</Computer Science/Compilation vs Interpretation.md>) 就包含狹義的 interpreter 與 VM

# 參考資料

- <https://en.wikipedia.org/wiki/Machine_code>
