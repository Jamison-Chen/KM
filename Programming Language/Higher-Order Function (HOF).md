#FP  

符合下列任一條件的 function，就是 HOF：

1. 接收一個以上的 function 作為參數（通常做為引數的這些 function 會被稱為 **procedural parameter**）
2. Return 一個 function

不是 HOF 者，則稱為 First-order function。

以 JavaScript 為例：

```TypeScript
const do_twice = (f: Function) => (x: any) => f(f(x));

const plus_three = (i: number) => i + 3;

console.log(do_twice(plus_three)(7)) // 13
```

上面這個例子中，`do_twice` 就是一個既接收 function 作為參數，又 return 一個 function 的 HOF；

在 JavaScript 中，Array prototype 也有很多專屬的 Higer-order methods，比如 `filter`：

```TypeScript
let arr: number[] = [2, 5, 1, 5, 3, 7, 3]
let biggerThanThree = arr.filter((num: number) => num > 3)
console.log(biggerThanThree) // [5, 5, 7]
```

如果要自己實作 `filter` 的話呢：

```TypeScript
function filter<T>(iterable: T[], predicate: (e: T) => boolean): T[] {
    let result: T[] = [];
    for (let t of iterable) {
        if (predicate(t)) result.push(t);
    }
    return result;
}

let arr: number[] = [2, 5, 1, 5, 3, 7, 3]
let biggerThanThree = filter(arr, (num: number) => num > 3)
console.log(biggerThanThree) // [5, 5, 7]
```

### Predicate & Functor

不知道你是否注意到，在自己實作 `filter` 的例子中，我定義了一個叫做 `predicate` 的參數，該參數是一個 return boolean 的 function，而它事實上也對應到了 JavaScript 原生的 `filter` 所接收的的第一個參數。

針對一個可迭代物件，若我想對其中的每個元素進行一些運算，同時我可以將運算的過程寫成一個函式 $f$，則此時 $f$ 被稱為是一個 functor；predicate 則泛指回傳值為 boolean 的 functor，或者較鬆散的定義是：只要一個 functor 的 return value 可以被 implicitly converted 為 boolean，那它就算是一個 predicate。

# First-Class Citizen

在一個程式語言中，若 function 符合以下三個條件，則可說該語言中的 function 為 First-class citizens（一等公民）：

1. Function 可以被當作參數放進另一個 function
2. Function 可以作為另一個 function 的 return value
3. Function 可以被 assign 為一個變數

我們再看一次本文開頭的 `do_twice` function 範例，這次我們多做一個 assign function to variable 的動作：

```TypeScript
const do_twice = (f: Function) => (x: any) => f(f(x));

const plus_three = (i: number) => i + 3;

const plus_six = do_twice(plus_three)

console.log(plus_six(7)) // 13
```

# 參考資料

<https://ithelp.ithome.com.tw/articles/10235555>
