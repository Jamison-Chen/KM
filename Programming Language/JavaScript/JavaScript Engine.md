#MemoryManagement 

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/javascript-runtime-in-the-browser.png>)

上圖為瀏覽器中的 JavaScript runtime 的架構，其左半部是 JavaScript engine。JavaScript engine 泛指負責執行 JavaScript 的 engine（廢話），它會將 source code 轉譯 (interpret) 成 machine code 並執行。

JavaScript engine 之於 JavaScript code 猶如 Python interpreter 之於 Python code。

其中一個有名的 JavaScript engine 是由 Google 開發的 **V8 engine**，Google Chrome 與 Node.js 都是使用 V8 engine，V8 使用 C 與 C++ 撰寫而成。

JavaScript engine 中主要有兩個 components，分別是 memory heap 與 call stack：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/javascript-engine-components.png>)

# Call Stack

- Stack 是有序且「後進先出」(LIFO) 的 [ADT](</Data Structures & Algorithms/ADT.draft.md>)
- Call stack 主要用來儲存還未執行完以及準備被執行的 function call，它讓 JavaScript engine 知道現在程式執行到什麼地方
- 當程式碼呼叫了某個 function `f`，`f` 就會被 push 進 call stack 中；當 `f` 執行完畢後，`f` 就會被 pop 出 call stack
    - 如果 function `f` 內呼叫了另一個 function `g`，則 `g` 就會在 `f` 執行完之前被 push 進 call stack，執行完 `g` 後將 `g` pop，然後繼續執行 `f`，依此類推

# Memory Heap

>[!Note]
>Memory heap 雖然叫做 heap，但跟資料結構中的 heap 完全無關。

- Memory heap 是無序 (unordered) 的
- Memory heap 用來儲存 object
    - Object 的大小與內容在 compile time 無法確定，heap 剛好很適合拿來儲存這樣的資料型態
    - Array、function 在 JavaScript 中也是 object 的一種
        - 請留意 function 與 function call 的差別
- [Garbage Collection](</Computer Science/Garbage Collection.md>) mechanism 會定期將沒有 reference 的 objects 從 memory heap 中刪除
- 在 Node.js 中，可以用 `process.memoryUsage()` 來查詢目前記憶體的使用量

# Call Stack 其實也存變數

Call stack 裡第一個（最底下那個）元素一定是 **global scope**，而所有定義在 global 的 variables、functions 與 classes 就是 global scope 底下的 attributes。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/javascript-global-frame-in-stack-memory.jpg>)

- 如果變數是 non-primitive type，則 variable name 與一個 memory address（指向 memory heap 的 reference）是存在 call stack；value 存在 memory heap 中，並且會給這塊 memory 一個 address（就是剛剛存在 call stack 中的 address）
    - `let myArray = [1, 2, 3]` 的步驟：
        - Step1: 在 compile time，建立一個 **unique identifier**（比如 `0458AFCZX91`）給 `myArray`
        - Step2: 在 run time，產生一個 address（比如 `22VVCX011`），將 unique identifier 與 address 放進 call stack
        - Step3: 一樣在 run time，將 value（`[1, 2, 3]`）放進 memory heap
        - Step4: 還是在 run time，將 call stack 中的 address（`22VVCX011`）複製到 memory heap，作為這塊 memory 的 address

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/call-stack-memory-heap-mapping.png>)

- 如果變數是 primitive type，則 variable name 與 value 都存在 call stack（沒有指向 memory heap 的 reference）
- Primitive type 的變數在 pop 出 call stack 後就不再佔記憶體空間了；但 non-primitive type 的變數因為 pop 時只 pop name 與 memory address，所以 value 其實還留在 memory heap，需要由 GC 定期清

# V8 Engine

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/v8-engine.png>)

關於 V8 如何進行 memory management 的完整介紹，請見[這篇文章](https://deepu.tech/memory-management-in-v8/)

### JIT Compilation in V8 Engine

>[!Note]
>關於 JIT compilation 的細節，請見[本文](</Computer Science/Compilation vs Interpretation.md>)。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/jit-compilation-in-v8-engine.png>)

# 參考資料

- <https://pashazade-nazar.medium.com/bba2569524cb>
- <https://medium.com/@minhaz217/ff6276d131a1>
