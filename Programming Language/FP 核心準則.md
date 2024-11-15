#FP

FP 中包括以下幾個核心準則：

- 使用 [Pure Functions](<#Pure Function>)
- 善用 [Function Composition](</Programming Language/Function Composition.md>) 提高程式碼的複用性
- 避免 [Mutating Shared State](<#Mutable Shared State 所造成的困擾>)
- 避免產生 [Side Effects](<#Side Effects>)

# Pure Function

Pure function 泛指符合以下兩個條件的 function:

- 給定相同的 input，一定會得到相同的 output

    一個 pure function 就像一個數學函數，給定一個定義域 (domain) 內的 input，必定產生唯一且固定的 output。

    這個特性進一步使得 pure function 擁有 **Referential Transparency** 這個特性，意思就是在茫茫程式碼中，我可以把所有呼叫 function F 的地方替換成 function F（在給定 input 的情況下所產生）的 output，同時程式的運行結果與替換前相比不會有任何差異。

- 不會產生 [#Side Effects](</./Programming Language/FP 核心準則.md#Side Effects>)

# Mutable Shared State 造成的困擾

Mutable shared state 是造成 **race condition** 的元兇，有句話是這麼說的：

>non determinism = parallel/asynchronous processing + mutable shared state

這種情況常出現在前後端的溝通中，當 client 以非同步的方式發出多個 requests 後，並無法確定 responses 會以什麼順序回來（因為每次通訊的 network routing 路徑、通暢度不一定相同），如果 response handler 收到 resposnes 後會去更改 mutable shared state，那就有可能造成使用者看到的最終結果沒有對應到其所做的最後一個動作。

### Mutability

若一個資料結構的值在初始化後便無法更動，則可說其為 immutable data structure，反之則為 mutable data structure。

須要注意的是，JavaScript 中，定義變數所用的 `const` 關鍵字並不會使得一個變數變成 immutable，`const` 只會使得變數本身「在其所處的 scope 內」不能放在 `=` 的左側，如果把這個特性誤認為 immutable，則會造成下列兩個漏洞：

- **變數的 property 還是可以放在 `=` 左側**

    ```JavaScript
    const a = {a: 1, b: 2};
    a.a = 2;
    console.log(a)  // {a: 2, b: 2}
    
    const b = [0, 1];
    b[0] = 1;
    console.log(b)  // [1, 1]
    ```

- **變數本身在其它 scope 中會變成 mutable**

    ```JavaScript
    const a = 0;
    const func = num => num++; 
    
    func(a)
    console.log(a)  // 0
    ```

    上例中，雖然最後 `a` 時還是 `0`，但是如果 `a` 真的是 immutable data，理想上應該在執行 `func(a)` 時就要報錯了。

# Side Effects

若執行一個 function 時，function 外的 scope 會有任何資料或狀態被更動，這樣的情況就叫做 side effects。小至更動一個變數的值，大至更改檔案或資料庫的內容，就連在 console 印出東西都算是一種 side effect。

若程式裡充斥著會造成 side effects 的 functions，將使得它們彼此牽一髮而動全身，這並不是一個在開發上樂見的特徵，因為這將使得整個程式很難進行小部分的 refactoring，除此之外，debug 時「修好這個 bug 卻產生其它新的 bugs」的機率也會提升，因為你有可能會為了修好一個 bug 而去修改某個會產生 side effect 的 function。

# 參考資料

- <https://medium.com/javascript-scene/7f218c68b3a0>
