# JavaScript is Single-Threaded

JavaScript 是一種 single-threaded language，意思是執行 JavaScript 的 engine 只會使用一個 thread 來執行程式碼（當然整個 engine 不只使用一個 thread）。

Single-threaded 使得 JavaScript engine 同一時間只能執行一個與程式碼相關的任務 (task)，如果有某個 task T 須要執行比較久，那其它 tasks 就必須排隊等它（這個現象稱為 blocking）。

但 JavaScript 透過 **event loop** 讓開發者可以進行 asynchronous programming，這樣一來即使某個 task T 要執行很久，也可以不等它，繼續執行後續的 tasks，等到有空時再回來處理 T。

# Event Loop

Event loop 是 JavaScript runtime model 中的一個 component，負責以下工作：

- 執行 code
- 收集 events
- 執行 events
- 執行 tasks

主要有三種 asynchronous programming 的方法，分別是使用 `setTimeout` 、`Promise` 與 `queueMicrotask`，但它們所造成的任務執行順序不同，在了解差異之前，我們需要先了解 JavaScript 是如何決定任務的處理順序的，而這就牽涉到 task queue。

# Task vs. Microtask

JavaScript 與其它多數程式語言一樣使用 queue 作為排序 tasks 的 [ADT](</Data Structures & Algorithms/ADT.draft.md>)，但與其它語言不同的是，JavaScript 有兩個 task queues，這是因為 JavaScript 中的 task 分為一般 task 與 microtask，所以一個 queue 用來給一般 tasks 排隊，另一個給 microtasks。



# Promise

`Promise` 是 JavaScript 在 ES6 以後才有的一種特殊的 object，專門用來處理「不是馬上有結果」的程式邏輯。

「不是馬上有結果的程式邏輯」的情境比如：

- 在 client 呼叫 API 與 server 溝通時，中間須要等待
- 使用者按下某個按鈕後，過一段時間才執行某個動做

在使用 `Promise` object 時，有些程式會希望「等」 `Promise` 的結果產生後才執行後續動作，有些則不希望被 `Promise` 擋住。另外，對 `Promise` 的執行結果也須要進行 error handling。

一個最簡單的 `Promise` 範例如下：

#TODO 

# `async`/`await`

到了 ES7 (ES2016) 後，除了 `Promise` 外還多了 `async`/`await` 兩個 syntax sugar。

#TODO 

# 實作一個 `sleep` Function

```JavaScript
function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

async function main() {
    console.log("start");
    await sleep(1000);
    console.log("stop");
}

main();
```

上面這個範例中，印出 "start" 後要等一秒才會印出 "stop"。

# Asynchronous 有比較快嗎？

有了 asynchronous mechanism 確實可以省下「等別人」的時間，但並不會讓「運算」時間變短，因為 JavaScript 還是只用一個 thread 在執行所有程式。以下方例子來說：

#TODO 

# 參考資料

- <https://dev.to/jeetvora331/difference-between-microtask-and-macrotask-queue-in-the-event-loop-4i4i>
- <https://medium.com/javascript-scene/master-the-javascript-interview-what-is-a-promise-27fc71e77261>
