### Hoisting 對於變數只會提升「宣告」，不會執行賦值

舉例：

```JavaScript
console.log(a);
var a = 10;
```

執行結果：

```plaintext
undefined
```

執行結果不是 `Uncaught ReferenceError ReferenceError: a is not defined`，這代表變數 `a` 是有被宣告的；但印出的內容是 `undefined` 而非 `10`，這代表 `a` 此時還沒有被賦值。

### `let` 與 `const` 無法享受 Hoisting？

舉例：

```JavaScript
console.log(a)
let a = 10;
```

執行結果：

```plaintext
Uncaught ReferenceError ReferenceError: Cannot access 'a' before initialization
```

有些人看到這個結果就會認為「只有 function declaration 與 `var` 變數才可以享受 hoisting」……且慢！請注意 error message 寫的是 "Cannot access 'a' before **initialization**" 而不是 "a is not **defined**"，也就是說現在變數 `a` 是處在一個「已經 defined (declared) 但尚未 initialized (assigned value)」的狀態。

有趣的是我們沒有辦法透過其他「常規」的方式定義一個這種狀態的變數，即使是單一行 `var a;` 或 `let a;`，其實都隱含著「assign `undefined` 給 `a`」的動作，換句話說：

```JavaScript
var a;
// is equivalent to:
var a = undefined;

let a;
// is equivalent to:
let a = undefined;
```

但這其實已經算是後話了，我們真的應該注意的是：即使 `let a = 10;` 寫在 `console.log(a);` 後面，變數 `a` 其實還是會在 `console.log(a);` 之前就先被 declared，所以 ==`let` 仍然算是有 hoisting==（`const` 也是，這裡就不再贅述）。

破除 `let`/`const` 沒有 hoisting 這個迷思或許比想像中來的重要，因為這個現象在「不同 scope 出現同名的變數時」會體現地更為明顯，比如：

```JavaScript
let a = 10;
if (a > 0) {
    console.log("hi");
    console.log(a);
    let a = 11;
}
```

執行結果：

```plaintext
hi
Uncaught ReferenceError ReferenceError: Cannot access 'a' before initialization
```

有印出 "hi"，代表變數 `a` 在 `if (a > 0)` 時，其值還是 10，所以進入了 `if` 的 scope；但沒有接著印出 `a` 的值反而報錯，就代表在 `if` scope 中，`a` 因為 hoisting 而變成前面提到的 "declared but not initialized" 的狀態了。

這個件事情我們，==在不同層級的 scopes 間若有同名的變數，則應將 child scope 中的變數定義在 scope 內對這個變數的「首次存取之前」，否則在定義之前存取都會報錯==。

### JavaScript 真的不是「一行一行執行」的

有些人或許會認為執行 JavaScript 這類的 interpreted language 時，就是直接將 source code 一行一行執行，但其實 hoisting 就是一個很好的反證，這點在[[程式語言的分類#直譯式 (Interpreted)|這篇文章]]中已經提過，這裡再提一個更明顯的例子：

```JavaScript
let a = 10;
console.log(a)
let a = 11;
```

你覺得上面這段程式碼執行的結果會是什麼呢？印出 10 嗎？還是印出 11？

公布答案，什麼都不會印，而是直接報錯！

```plaintext
SyntaxError: Identifier 'a' has already been declared
```

# 參考資料

- <https://blog.techbridge.cc/2018/11/10/javascript-hoisting/>
