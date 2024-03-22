# What is Hoisting?

不知道你有沒有注意到，在寫 JavaScript 時我們可以先呼叫一個不存在的 function，再定義那個 function：

```JavaScript
helloworld();

function helloworld() {
    console.log("helloworld");
}
```

上面這段程式不會出錯，而是會正常地印出 helloworld。這在其它程式語言中可不一定成立，比如如果我們這樣寫 Python：

```Python
helloworld()

def helloworld():
    print("helloworld")
```

就會得到下面這個錯誤：

```plaintext
NameError: name 'helloworld' is not defined
```

事實上許多 interpreted language 都不支援這種「先呼叫、再定義」的寫法，因為 interpreter 是按照 source code 撰寫的順序一行一行執行它們的。（compiled language 則大多數都支援「先呼叫、再定義」）

那為什麼 JavaScript 沒有這個限制呢？原因就是 JavaScript 中有 hoisting 機制。Hoisting 是 [[JavaScript Engine]] 在開始執行程式前會做的工作，它會先將整份 source code 掃過一遍，並==將所有 function declarations 與 variable declaration 移到其所屬 scope 的最上方==。

# 變數的 Hoisting 只會提升「宣告」，不會賦值

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

# `let` 與 `const` 無法享受 Hoisting？

舉例：

```JavaScript
console.log(a)
let a = 10;
```

執行結果：

```plaintext
Uncaught ReferenceError ReferenceError: Cannot access 'a' before initialization
```

有些人看到這個結果就會認為只有 function declaration 與 `var` 變數才可以享受 hoisting。

且慢！請注意 error message 寫的是 "Cannot access 'a' before **initialization**" 而不是 "a is not **defined**"，也就是說現在變數 `a` 是處在一個「已經 defined (declared) 但尚未 initialized (assigned value)」的狀態。

有趣的是我們沒有辦法透過其他「常規」的方式定義一個這種狀態的變數，即使是單一行 `var a;` 或 `let a;`，其實都隱含著「assign `undefined` 給 `a`」的動作，換句話說：

```JavaScript
var a;
// is equivalent to:
var a = undefined;

let a;
// is equivalent to:
let a = undefined;
```

但這其實已經算是後話了，我們真正應該注意的是：即使 `let a = 10;` 寫在 `console.log(a);` 後面，變數 `a` 也還是會在 `console.log(a);` 前就先被 declared，所以 ==`let` 仍然算是有被 hoist==（`const` 也是，這裡就不再贅述）。

破除 `let`/`const` 沒有 hoisting 這個迷思或許比想像中來的重要，因為這個現象在「不同 scope 出現同名的變數時」會體現地更為明顯，比如：

```JavaScript
let a = 10;
if (a > 0) {
    console.log("hi");
    console.log(a);
    let a = 11;
    console.log(a);
}
```

執行結果：

```plaintext
hi
Uncaught ReferenceError ReferenceError: Cannot access 'a' before initialization
```

有印出 hi，代表變數 `a` 在 `if (a > 0)` 時，其值還是 10，所以進入了 `if` 的 scope；但沒有接著印出 `a` 的值反而報錯，就代表在 `if` scope 中，`a` 因為 hoisting 而變成前面提到的 "declared but not initialized" 的狀態了。

這件事情告訴我們，==若使用 `let`/`const` 變數，則應將變數定義在當前 scope 內對這個變數的「首次存取之前」，否則在定義之前存取都會報錯==。

# JavaScript 是一行一行執行的？

你或許常聽到人說：「JavaScript 這類的 interpreted language 是直接將 source code 一行一行執行的」，現在你知道事情其實並不單純，經過 hoisting 的程式碼結構通常會和 source code 不一樣，舉個最簡單的例子：

```JavaScript
let a = 10;
console.log(a);
let a = 11;
```

你覺得上面這段程式碼執行的結果會是什麼呢？印出 10 嗎？還是印出 11？

答案是什麼都不會印，然後報錯：

```plaintext
SyntaxError: Identifier 'a' has already been declared
```

如果是直接將 source code 一行一行執行，那以上面的例子來說，一直到第二行看起來都很正常，沒理由報錯。實際上 JavaScript engine 看到的 code 應該已經被 hoisting 改成這樣了：

```JavaScript
let a = 10;
let a;
console.log(a);
a = 11;
```

值得注意的是，程式甚至不是在 run time 執行到第二行 `let a;` 時才報錯，而是在 hoisting 當下（run time 之前，但不叫 compile time，因為 hoisting 不算 compilation）就發現了，所以你會看到這個 error 被視為 `SyntaxError`。

# 參考資料

- <https://blog.techbridge.cc/2018/11/10/javascript-hoisting/>
