下面是一個使用傳統方法與 arrow function 定義 `add` function 的範例：

```JavaScript
// ES5: Traditional Function Expression
var add = function (a, b) {
    return a + b;
};

// ES6: Arrow Function
const add = (a, b) => a + b;
```

# Arrow Function 與傳統 Function 的差異

Arrow function 的除了比傳統的 function expression 更簡潔之外，它們之間還有一個本質上的差別：

> Arrow function 中的 `this` 永遠都指向「定義此 arrow function 的 class 的 instance」。

從下面這個例子可以看出來：

```JavaScript
class C1 {
    f() {
        console.log(this);
    }
    g = () => console.log(this);
}

class C2 {
    constructor(func) {
        this.h = func;
    }
}

const c1 = new C1();
const c2_1 = new C2(c1.f);
const c2_2 = new C2(c1.g);

c2_1.h();  // C2 {h: ƒ}
c2_2.h();  // C1 {g: ƒ}
```

從下面這個例子也可以看得出來：

```JavaScript
class C1 {
    f() {
        console.log(this);
    }
    g = () => console.log(this);
}

class C2 {
    h(func) {
        func();
    }
}

const c1 = new C1();
const c2 = new C2();

c2.h(c1.f);  // undefined
c2.h(c1.g);  // C1 {g: ƒ}
```

# Arrow Function 的限制

除此之外，arrow function 還有幾個限制：

- 不能用來定義 class 的 constructor
- 不能用來定義 generator function

# 可以簡化到什麼程度？

- 若 function block 內只有一行，且該行恰好要 return，可以省略 `{}` 與 `return`

    e.g.

    ```JavaScript
    const add = (a, b) => {
        return a + b;
    };
    // 可以簡寫成：
    const add = (a, b) => a + b;
    ```

    有兩點須注意：

    - 若有寫 `{ }`，就必須寫 `return` 才會 return
    - 若沒寫 `{ }`，則「不能」寫 `return`，且一定會 return

- 若 parameter 只有一個，可以省略 `()`

    e.g.

    ```JavaScript
    const pow = (n) => n * n;
    // 可以簡寫成：
    const pow = n => n * n;
    ```

    須注意的是，若 function 沒有 parameter，反而要寫一個空的 `()`。
