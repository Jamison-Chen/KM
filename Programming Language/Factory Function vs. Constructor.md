#FP

# Factory Function

以 JavaScript 舉例：

```JavaScript
function personFactory(name, age) {
    const greet = () => console.log(`Hello! My name is ${name}.`);
    return { name, age, greet };
};

let jeff = personFactory("Jeff", 27);

jeff.greet();  // Hello! My name is Jeff.
```

上面的例子中，`personFactory` 為一個 Factory Function，其中的 inner function `greet` 利用了 [Closure](</Programming Language/Closure.md>) 的特性，因此得以捕獲 (capture) `name` 這個變數，使得透過呼叫 Factory Function 所得到的物件，就像是使用 consturctor 建構出來的物件，可以有自己的 attributes，inner functions 則成為物件的 methods。

# Constructor

一樣以 JavaScript 舉例：

```JavaScript
function Person (name, age) {
    this.name = name;
    this.age = age;
    this.greet = () => console.log(`Hello! My name is ${this.name}.`)
}

let jeff = new Person("Jeff", 27);

jeff.greet();  // Hello! My name is Jeff.
```

### The `new` operator

雖然這件事對各位來說或許不陌生，但請還是先將目光放到初始化物件時的 `new` operator 上，然後試想一個問題：「如果不寫 `new`，直接呼叫 `Person("Jeff", 27)` 的話會怎麼樣呢？」

實際嘗試過後你應該會得到下面這個 error message:

```plaintext
<line 2>
Uncaught TypeError: Cannot set property of undefined (reading 'name')
```

由此可知，初始化時若沒有 `new`，`this` 就會是 `undefined`。

當然，`new` 除了==「讓 `this` 具有意義」==這個功能外還有其它，比如你或許會注意到，在定義 `Person` 這個 function 時，並沒有 return value，但在成功初始化後可以將其 assign 給變數 `jeff` 且可以進一步呼叫，其實這也是 `new` 的功勞：==令 constructor return 初始化完畢後的 object（其實就是 `this`）==。

事實上，今天如果要使用 constructor 來建立物件，上面提供的方法幾乎要被拋棄了，因為 JavaScript 的世界裡也有一般 OOP 語言中常見的 `class` 等語法，目的就是模仿 OOP，但這已並非撰寫本文之目的了，欲了解更多關於 `class` 以及其它 JavaScript 用來模仿 OOP 語言的相關語法，請見 [[JavaScript 中的 OOP]]。

回到 `new` 這個議題，最後一個值得注意的細節與 JavaScript 身為 prototype-based language 這件事相關，根據 [Prototype-Based Language](</Programming Language/Prototype-Based Language.md>) 的原則：「一個物件的原型會是它的 constructor」或者說「`[物件].__proto__ === [constructor].prototype`」，以上面的例子來說，我們可以發現：

```JavaScript
console.log(jeff.__proto_ === Person.prototype)  // true
```

而這件事其實也是 `new` 幫我們做到的。

# 參考資料

- <https://www.theodinproject.com/lessons/node-path-javascript-factory-functions-and-the-module-pattern>
- <https://chamikakasun.medium.com/javascript-factory-functions-vs-constructor-functions-585919818afe>
