`Promise` 是 JavaScript 在 ES6 以後才有的一種特殊的 object，專門用來處理「不是馬上有結果」的程式邏輯。

會遇到「不是馬上有結果的程式邏輯」的情境包括：

- 在 client side 呼叫 API 與 server 溝通時
- 需要讓程式休息一段時間再繼續執行時

在使用 `Promise` object 時，有時候會有某些程式必須在 `Promise` 的結果產生後才執行，有些則不希望被 `Promise` 擋住；且與處理一般的程式邏輯時類似，對 `Promise` 的執行結果也要進行 error handling。

#TODO 

# 實作一個 `sleep` Function

```JavaScript
function wait(time) {
    return new Promise((resolve, reject) => {
        setTimeout(() => resolve(), time);
    });
}

async function main() {
    console.log("start");
    await wait(1000);
    console.log("stop");
}

main();
```

上面這個範例中，印出 "start" 一秒後才會印出 "stop"。

這個範例結合了 ES7 後才有的 syntax sugar: `async`/`await`

#TODO 

# 參考資料

- <https://medium.com/javascript-scene/master-the-javascript-interview-what-is-a-promise-27fc71e77261>
