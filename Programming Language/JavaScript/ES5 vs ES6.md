# Introduction

- ES5 與 ES6 指的分別是第五版與第六版的 ECMAScript
- ECMAScript 是用來規範 scripting language 的國際標準
- ES6 在 2015 年誕生，所以也被稱為 ES2015
- 在 ES6 之後，ECMAScript 仍陸續有更新的版本，只是它們之間的差異都沒有像 ES5 與 ES6 之間這麼大，所以比較少人在做比較

# `var` 的缺點

JavaScript 自從 ES6 開始使用 `let` 與 `const` 取代 ES5 的 `var`，原因是 `var` 有以下幾個缺點：

### `var` 會無視 Block Scope

e.g.

```JavaScript
function f(x) {
    for (var x = 1; x < 10; x++) {
        // ...
    }
    console.log(x);
}

f(20);  // 10
```

上面這個例子中，function `f` 內的 for loop 中的區域變數 `x`，影響到了與其同名的 function 參數 `x` 的值，一般的程式語言不會有這個問題，但 JavaScript 的 `var` 會。

### `var` 無法 [Capture](</Programming Language/Closure.md#Captured Variables>)

e.g.

```JavaScript
for (var x = 0; x < 3; x++) {
    setTimeout(() => console.log(x));
}
// 3
// 3
// 3
```

你可能會以為印出的是 0, 1, 2，但因為 `x` 沒有被 captured，所以大家都拿到 `x` 最後的狀態。

但若改用 `let` 就不會有這個問題：

```JavaScript
for (let x = 0; x < 3; x++) {
    setTimeout(() => console.log(x));
}
// 0
// 1
// 2
```

# Function Declaration 會無視 Block Scope

舉例而言：

```JavaScript
// Define function `f` using "function declaration"
function f() {
    console.log("hello");
}
if (true) {
    function f() {
        console.log("world");
    }
}

f();  // world
```

解決方法：

- 方法一：開啟「嚴格模式」

    ```Javascript
    "use strict"

    function f() {
        console.log("hello");
    }
    if (true) {
        function f() {
            console.log("world");
        }
    }

    f();  // hello
    ```

- 方法二：使用 **Function Expression** 的方式定義 function，並且使用 `let` 或 `const` 來定義變數

    ```JavaScript
    const f = function () {
        console.log("hello");
    }
    if (true) {
        const f = function () {
            console.log("world");
        }
    }

    f();  // hello
    ```

雖然現在有 function expression 這個解法，但 ES6 以及更新版本的 ECMAScript 並沒有棄用 function declaration，因為 function declaration 有 [Hoisting](</Programming Language/JavaScript/Hoisting.md>) 這個很棒的特性（可以先呼叫 function 再定義 function），function hoisting 可以增加程式碼的可讀性，這是使用 `const`/`let` 定義 function 時沒辦法享受的好處。

# Template Literals

若在 ES5 中要將變數與字串串接，必須使用 `+`，但自 ES6 以後，可以使用 template literals (\`\`)：

```JavaScript
// ES5
var price = 10;
var message = "An apple costs " + price + " dollars.";
console.log(message);  // An apple costs 10 dollars.

// ES6
const price = 10;
const message = `An apple costs ${price} dollars.`;
console.log(message);  // An apple costs 10 dollars.
```

Template literals 會自動將 `${}` 內非字串型別的變數轉為字串。

\`\` 也可以用來定義有換行或有 indent 的字串，這些換行／indent 會被保留，比如：

```JavaScript
const message = `<div>
    <p>
        <h1>Hello</h1>
    </p>
</div>`
console.log(message);
// <div>
//     <p>
//         <h1>Hello</h1>
//     </p>
// </div>
```

# Destructuring Assignment

JavaScript 從 ES6 開始支援 destructuring assignment（解構賦值），舉例而言：

```JavaScript
// Destructure array
const arr = [1, 2, 3];
let [a, b, c] = arr;
console.log(a);  // 1

// Destructure object
const obj = {a: 1, b: 2, c: 3};
let {a, b, c} = obj;
console.log(d)  // 1
```

在解構 object 時，只能用 object 中的 key 作為等號左側的變數名稱。換句話說，變數 `a` 被賦予的值必為 object 中 `"a"` 這個 key 所對應到的 value。

Function 定義要接收的參數時，也可以直接使用 destructuring assignment，比如：

```JavaScript
function f({a, b}) {
    console.log(a);
    console.log(b);
}

const x = {a: 1, b: 2, c: 3};
f(x);
// 1
// 2
```

上面這個寫法會比在 function 中直接定義「接收整個 object」，然後在 function 中再用 key 取值的方法可讀性更高：

```JavaScript
// ES5
function f(obj) {
    console.log(obj.a);
    console.log(obj.b);
}

const x = {a: 1, b: 2, c: 3};
f(x);
// 1
// 2
```

# Object Literals

定義 object 時，若要將一個變數塞進 object 當作某個 value，且此時「key 的名稱與此變數的名稱相同」時，在 ES6 以後可以用較簡潔的方式定義。

e.g.

```JavaScript
// ES5
const username = "Andy";
const profile = { username: username };

// ES6
const username = "Andy";
const profile = { username };
```

# Computed Property Names

- ES6 以後，可以動態計算出 property name 並提供給 object
- Property name 就是 key
- 將 expression 放在 `[]` 中
- 這個做法可以取代 ES5 中「先建立 empty object，再填 key & value」的做法

e.g.

```JavaScript
// ES5
const obj = {};
obj[new Date().toISOString().slice(0, 10)] = 100;
console.log(obj);  // {2023-11-15: 100}

// ES6
const obj = { [new Date().toISOString().slice(0, 10)]: 100 };
console.log(obj);  // {2023-11-15: 100}
```

# Class

JavaScript 雖然是一個 prototype-based 的程式語言，但在 ES6 後引入了 class 的概念，所以自此 JavaScript 也可以寫 [OOP](</Programming Language/OOP 四本柱.md>) 了！

e.g.

```JavaScript
class Person {
    constructor(name) {
        this.name = name;
        // ...
    }
    eat(food) {
        // ...
    }
    // ...
}

const alice = new Person("alice");
alice.eat("breakfast");
```

>[!Note]
>JavaScript 並沒有因為加入了 class 的概念就從 prototype-base 變成 class-based，因為 JavaScript 中的 class 只是 syntax sugar，底層還是由 function 與 prototype 實作的。

# Arrow Function

ES6 多了 arrow function：

```JavaScript
// ES5: Traditional Function Expression
var add = function (a, b) {
    return a + b;
};

// ES6: Arrow Function
const add = (a, b) => a + b;
```

關於 arrow function 的詳細介紹，請見[本文](</Programming Language/JavaScript/Arrow Function.md>)。

# Module System

JavaScript 直到 ES6 後才有 [Module System](</Programming Language/JavaScript/Module System.md>) 的概念，但在 ES6 之前，社群上已發展出 CommonJS 與 AMD (Asynchronous Module Definition) 兩套較知名的模組系統。

# Promise

`Promise` 是 JavaScript 在 ES6 以後才有的一種特殊的 object，專門用來處理「不是馬上有結果」的程式邏輯。

會遇到「不是馬上有結果的程式邏輯」的情境包括：

- 在 client 呼叫 API 與 server 溝通時，中間須要等待
- 須讓程式休息一段時間再繼續執行時

在使用 `Promise` object 時，有些程式會希望「等」 `Promise` 的結果產生後才執行後續動作，有些則不希望被 `Promise` 擋住。

對 `Promise` 的執行結果也要進行 error handling。

到了 ES7 (ES2016) 後，除了 `Promise` 外還多了 `async`/`await` 兩個 syntax sugar。

關於 `Promise` 的詳細介紹，請見 [Asynchronous Programming](</Programming Language/JavaScript/Asynchronous Programming.draft.md>)。
