### [Clean Code - Uncle Bob](https://www.youtube.com/playlist?list=PLe5y1VxKIEvdUXkj4DEGWwSiqK7pG_2qr)

- Function 的命名越詳細越好，且應該是動詞而非名詞
- Class 的命名應為名詞
- 一個 function/variable 如果需要註解才能讓人知道用途，那代表名字取得不好
- 命名風格盡量一致，比如同樣是 array，不要有些地方用 `books` 有些地方用 `book_array`
- 一個 function 接收的參數不宜過多（最好不要超過三個）
- 不要設計「輸出型的參數」

    Function 不要有 parameter 是拿來收集 output 然後 return 的，錯誤示範如下：

    ```JavaScript
    // 錯誤示範
    function appendCell(board) {
        board.push(new Cell());
    }
    ```

- 盡可能地拆解出 functions，每個 function 只做一件事情
- 一個被呼叫的 function，應該要出現在「執行呼叫的 function」的下方
- 不要把 try-catch 當作 if-else 使用
- [SOLID Principles](</Programming Language/SOLID Principles.md>)
- [Test-Driven Development (TDD)](</Programming Language/Test-Driven Development (TDD).md>)
- 變數的名稱長度（完整度）應該與其 scope 成正比，scope 越小的變數名稱可以取的越短
- 避免在 method 中使用 switch statement，應該將個原本要傳入 switch statement 的條件做成 classes，並且利用 polymorphism 的方式在每個 subclasses 中 override 該條件所對應的行為

>If you wanna go fast, you go well.

# 參考資料

- <https://www.mropengate.com/2022/10/clean-code.html>
