Interpretation (轉譯) 與 Compilation (編譯) 並非互斥的概念，很多語言既需要 interpretation 也會經過 compilation。其實我們根本無法把程式語言乾淨地二分為編譯式語言與直譯式語言，因為我們對所有程式語言都可以選擇走編譯的流程，也可以選擇走直譯的流程，只是要看有沒有人寫出「編譯那個語言的工具」或「直譯那個語言的環境」而已。

# Compilation

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/compilation-process.png>)

由 **compiler** 將整包 **source code**（通常是[高階程式語言](</Programming Language/零碎筆記.md#程式語言的演進>)）編譯成與其語意等價 object code 後，交給後續的工具（assembler、linker 等）將 object code 進一步轉換為 [Machine Code](</Computer Organization & Architecture/Machine Code.md>)，最後交給 CPU 執行。

### Compile Time

Compiler 編譯程式語言的期間稱為 **compile time**（編譯期），編譯完後才進入 **run time**（執行期）。由於只要有更改到 source code 就必須將該變動所影響的部分重新 compile，且 compile time 會隨著 source code 越大包而越長，因爲程式在開發期通常會需要不斷「試執行」，所以開發者就會花比較多時間在等待編譯。

雖然將整包 source code 編譯須要花不少時間，但只要 source code 的內容沒有被更動，往後每次執行程式時，都是由 CPU 直接運行之前編譯好的 machine code，不須再次編譯。

>[!Note]
>關於 compilation 的完整步驟解說，請見 [The Process of Compilation](</Computer Science/The Process of Compilation.md>)。

# Interpretation

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/interpretation-process-1.png>)

從外部看起來，interpreter 就像是一個黑盒子，它可以在 run time 直接讀取 source code，將 [statements](</Programming Language/零碎筆記.md#Expression vs. Statement>) 一行一行執行，看其來好像不須要將 source code 翻譯成 machine code。不過當你了解 interpreter 本身如何實作後，你會發現 interpreter 內部也是將每一個 source code statement 都翻譯成 machine code 才執行，因為任何程式語言最後一定都是丟給 CPU 執行，而 CPU 只看得懂 machine code。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/interpretation-process-2.png>)

>[!Note]
>有些 interpreter 會在執行 source code 前做一些前置作業，比如 [JavaScript Engine](</Programming Language/JavaScript/JavaScript Engine.md>) 在執行程式碼前會先進行 [Hoisting](</Programming Language/JavaScript/Hoisting.md>)，這類的前置作業並不算 compilation，因為 compilation 的定義是將高階語言轉換成低階語言，而 hoisting 只是調整部分程式碼的結構而已。

### Longer Run Time

"No compile time" 是使用 interpreter 執行程式碼的優點，這讓開發的過程順暢很多；但因為 interpreter 是在 run time 才即時將 source code 翻譯成 machine code，且不能通盤檢視整份 machine code  並將其最佳化，所以 run time 比較長（白話文：「程式會跑比較慢」）。

舉例來說，interpreter 在執行「將兩個變數相加」的程式碼時，會須要透過 unique identifiers 去 main memory 存取兩個變數，再將它們相加；而 compiler 則可以直接把變數放在 CPU register，直接將它們相加。（存取 memory 比存取 register 慢很多）

理論上 interpreter 每執行到一個 statement 都要對該 statement 做解析，所以若某個 function 被呼叫了 n 次，function declaration 那段程式碼就會被解析 n 次，即使這 n 次根本就是在做一模一樣的事情。然而這只是最基本的 interpreter 的設計，現在的 interpreter 其實已經非常有效率了，在解析工作的眾多環節中，有些可以只做一次的環節會被抽離出來（比如 type analysis，此處暫不展開）。

# 跨平台相容性

跨平台相容性有時候有被稱為「可攜帶性」，為什麼要討論它呢？可以先想一個問題：「當我們開發完一款應用程式後，要怎麼發佈 (distribute) 才能讓它可以在其他人的電腦上直接跑起來？」總不可能你用 Python 寫了一個應用程式，結果別人下載完要執行，卻發現還要先到 Python 官方網站下載 Python interpreter 吧？我們平常從 Apple App Store 或 Google Play Store 下載應用程式時，好像從來不須要額外下載「解析該應用程式所使用的程式語言的工具」，那我們自己寫的應用程式要怎麼才能像市面上的應用程式一樣，直接在其他機器上運行呢？

其實這個問題的關鍵就是「別人的電腦可以直接執行什麼東西？」CPU 只能直接執行 machine code，特定語言的 interpreter 可以直接執行該語言的 source code，所以我們發佈應用程式的方法主要有三種：

- 使用 compiler 將應用程式的 source code 編譯成 machine code
    - 一般情況下，compiler 會根據目前 CPU 的 [[Instruction Set Architecture.draft|ISA]] 編譯出專屬於該 ISA 的 object code，最後產出專屬於該 ISA 的 machine code，所以在 x86 架構的 CPU 環境下編譯出來的 machine code 就不能給 ARM 架構的 CPU 運行（但也有 [cross compiler](https://en.wikipedia.org/wiki/Cross_compiler) 可以在 A 環境下編譯出 B 環境可用的 machine code）
    - 通常會採取這種做法的，會被稱為 compiled language，比如 C、C++、Go
- 將應用程式的 source code，以及整個可以執行該 source code 的 interpreter，打包並編譯成執行檔 (executable)
    - 給 Windows OS 的 executable 是 .exe file，給 MacOS 的是 .app file
    - Executable 除了一些 metadata 外，主要也是 machine code，所以也不能跨平台
    - 通常會採取這種做法的，會被稱為 interpreted language，比如 Python
- 如果幾乎所有人的電腦上都有可以執行該 source code 的 interpreter，則可以直接發佈 source code
    - 須要為不同 ISAs 實作可以在該平台的運作的 interpreter
    - 通常會採取這種做法的，也會被稱為 interpreted language，比如 JavaScript（幾乎每個人的電腦上都有瀏覽器，而瀏覽器中幾乎都有 [JavaScript Engine](</Programming Language/JavaScript/JavaScript Engine.md>)）

---

|-|Compiler|Interpreter|
|:-:|:-:|:-:|
|**Input**|一次整包 source code|一次一個 source code statement|
|**Output**|object code|執行結果|
|**運作方式**|先編譯，再執行|翻譯、執行、翻譯、執行…|
|**執行速度**|🚀 較快|較慢|
|**記憶體用量**|較高，因為要生成 object code|✅ 較低|
|**報錯方式**|一次告訴你所有 compile errors|執行時出錯就中斷，所以一次只有一個 root error|

# JIT Compilation

JIT 是 just-in-time 的縮寫。

大多數的應用程式都會符合某種八二法則：「只有少數程式碼會頻繁地被執行」，所以理論上只要解決這些「熱點片段」的效能問題，就可以有效改善應用程式整體的運行效率，而 JIT compilation 的誕生正是基於這個理由。

相對於在 compile time 就會將所有 source code 編譯成 machine code 並對編譯好的 machine code 進行最佳化的 AOT (ahead-of-time) compilation，走 JIT compilation 路線的程式語言會先被編譯成介於 source code 與 machine code 間的 intermediate representation（比如 bytecode），到了 run time，會走 interpretation 的方式直接運行 bytecode，但同時也會偵測已執行過且常被重複使用的熱點片段，把它們編譯成可以高效執行的 machine code，並進行最佳化。

執行這種程式的機器上須要有該語言專屬的 virtual machine（簡稱 VM，算 interpreter 的一部分）比如 JVM for Java、V8 engine for JavaScript，Python 也預計在 3.13 版中引入 JIT。須注意的是，通常 VM interpret 的是已經被開發者「初步編譯」過的 bytecode 而不是 source code。

# 參考資料

- <https://www.oreilly.com/library/view/java-performance-the/9781449363512/ch04.html>
- <https://www.ibm.com/docs/en/sdk-java-technology/8?topic=reference-jit-compiler>
