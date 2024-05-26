Imperative (命令式) programming 與 declarative (宣告式) programming 是兩種不同的「程式語法風格」，或者說是兩種不同的典範 (programming paradigm)。

既然「風格」不同，那麽在閱讀時肯定會有不同的「感受」。通常，在閱讀一個以 imperative paradigm 撰寫的完整程式碼片段時（比如一個 function），可以清楚地知道這段程式碼處理資料的==方法==以及==過程==；另一方面，閱讀一個 declarative 的程式碼片段時，則可以清楚知道這段程式碼的==目標==是什麼，以及用到哪些==工具==。

當然，面對問題時永遠只談論目標與工具而不實作方法與過程通常是沒辦法解決問題的，所以，並不是說在 declaretive paradigm 中就不必實作方法與過程，我們或許還是得用 imperative 的方式實作出一個個可以解決小問題的小工具，只是未來當遇到較複雜的問題時，我們可以使用更抽象的方式宣告如何使用或組合這些小工具來解決問題。

有些語言天生就被設計成只能用 declarative 的語法來撰寫，比如 SQL。

### 舉例

假設我現在需要一個 `transform` function，其目標是 input 一個 string array，output 一個 string array，其中 output 的結果會是：「將 input array 反轉後，篩選出所有長度大於 3 的元素，然後將它們全部轉為大寫」。

若要完全以 imperative 的方法達成上述需求，那就直接在 function 內部實作解決問題的方法：

```TypeScript
function transform(arr: string[]): string[] {
    let step_one_result: string[] = [...arr];
    step_one_result.reverse();

    let step_two_result: string[] = [];
    for (let each of step_one_result) {
        if (each.length > 3) {
            step_two_result.push(each.toUpperCase());
        }
    }
    return step_two_result;
}
```

透過閱讀上面的程式碼，你可以很清楚的知道它是如何處理每一個 input array 裡的元素，包括使用 `Array` prototype 的內建 method `reverse` 進行 in-place 翻轉、使用 `for` loop 逐一將 array 裡符合條件的元素挑選出來、使用 `String` prototype 的 `toUpperCase` method 轉大寫等...... 這就是 imperative paradigm 給我們的感覺。

當然還有很多不同的寫法可以達成題目的要求，比如我可以把「篩選長度」跟「轉大寫」分成兩個 `for` loop，甚至可以把「篩選長度」跟「轉大寫」獨立寫成兩個 functions 然後再在 `transform` 裡呼叫他們，像是這樣：

```TypeScript
function transform(arr: string[]): string[] {
    let result: string[] = [...arr];
    result.reverse();
    result = filter_long_string(result, 3)
    result = to_upper(result)
    return result;
}
```

甚至可以把上面 `transform` function 內部的 5 行縮短為 3 行：

```TypeScript
function transform(arr: string[]): string[] {
    let result: string[] = [...arr];
    result.reverse();
    return to_upper(filter_long_string(result, 3))
}
```

你會發現，後續這兩個動作已經使得整個 `transform` function 看起來不那麼囉唆，單看這個 function，我們漸漸地只能知道它做了哪些步驟 (what) 而無法知道每一個步驟是怎麼做到的 (how)，其實這就是一個朝向 declarative paradigm 靠近的過程。

那麼讓我們來看看最 declarative 的寫法：

```TypeScript
const transform = compose(
    reverse,
    filter((el: string) => el.length > 3),
    to_upper
);
```

這裡我們用到了 FP 中 [Function Composition](</Programming Language/Function Composition.md>) 的技巧，其中的 `reverse`, `filter((el: string) => el.length > 3)` 與 `to_upper` 皆為接收一個 string array 作為參數的 functions。

---

通常使用 FP 的精神所寫出來的程式都會偏 declarative，使用 [OOP](</Programming Language/OOP 四本柱.md>) 的精神寫出來的程式則會偏向 imperative，然而也並非絕對，比如一個符合 FP 精神的 [pure function](</Programming Language/FP 核心準則.md#Pure Function>)，其內容可能是 imperative 的，舉例而言：

```TypeScript
function sum(arr: number[]): number {
    let result: number = 0;
    for (let num of arr) result += num;
    return result;
}

let arr: number[] = [1, 2, 3]
sum(arr)  // 6
```

使用一些 [Higher-Order Function](</Programming Language/Higher-Order Function.md>) 會更 declarative 一些：

```TypeScript
let arr: number[] = [1, 2, 3]
arr.reduce((a, b) => a + b)  // 6
```

另一方面，在處理 iterable data 時，使用 recursion 會比使用 iteration 來得更 declarative，我們一樣拿上面的 `sum` 來舉例，上面已經示範了 iteration 的做法，那如果寫成 recursion 呢？

```TypeScript
function sum(arr: number[], n?: number): number {
    if (n===undefined) n = arr.length
    if (n <= 0): return 0
    return arr[n-1] + sum(arr, n-1)
}
```

Imperative `sum` 告訴我們：「加總就是把數字一個一個加起來，加到沒有為止。」；Declarative `sum` 告訴我們的則是：「加總就是把最後一個數字加上前面所有數字的加總。」

# 參考資料

- <https://ithelp.ithome.com.tw/articles/10233761>
- <https://dev.to/ruizb/declarative-vs-imperative-4a7l>
