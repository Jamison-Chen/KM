### Destructuring Assignment

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

>[!Note]
>在解構 object 時，只能用 object 中的 key 作為等號右側的變數名稱，換句話說，一個變數被賦予的值必為 object 中與該變數同名的 key 所對應到的 value。

---

### 使用 `var` 的缺點

JavaScript 自從 ES6 開始使用 `let` 與 `const` 取代 ES5 的 `var`，原因是 `var` 有以下幾個缺點：

- `var` 會無視 block scope

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

- `var` 無法被 [[Closure#Captured Variables|captured]]

    e.g.

    ```JavaScript
    for (var x = 0; x < 3; x++) {
        setTimeout(() => console.log(x));
    }
    // Output:
    // 3
    // 3
    // 3
    ```

    你可能會以為 output 是 0, 1, 2，但因為 `x` 沒有被 captured，所以大家都拿到 `x` 最後的狀態。