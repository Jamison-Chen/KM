# `History` Interface

Browser 中的每一個 tab 都會有一個唯一的 `History` instance，可以使用 JavaScript 的 `window.history` 來取得這個 instance 。

下面是 `console.log(window.history)` 的結果：

```json
{
    "length": 1,
    "scrollRestoration": "auto",
    "state": null
}
```

更多關於 `History` interface 的細節，詳見 [MDN](https://developer.mozilla.org/en-US/docs/Web/API/History)。

# History Stack

History stack 顧名思義是一個 stack 資料結構，記錄使用者在當前 browser tab 的網頁造訪歷史，只能從頭拿取與放入資料，當我們造訪一個網頁時，該網頁就會被 push 進 history stack，換句話說，現在造訪的網頁就是 history stack 中的第一筆資料、上一頁則是第二筆… 依此類推。

# 無法得知歷史的細節

如上面的範例所示，使用 `window.history` 可以獲一些 browser history 的資訊，但無法查看使用者過往的瀏覽歷史。

只能使用 `.back()`、`.forward()` 以及 `.go(n)` 來實際造訪這些網頁。

# 無法覆寫 Browser 內建的上／下一頁按鈕的行為

包括電腦版瀏覽器的上／下一頁按鈕，以及大部分 Android 手機的 back 按鈕，其功能皆固定為 `window.history.back()`，無法透過 JavaScript 覆寫這個行為。

# 但是可以自己創造新的歷史

前面有提到在同一個 tab 造訪新網頁時就會將該網頁 push 進 history stack，主要有兩種實現方式：

- 使用 `window.location = "..."` 跳轉頁面
- 讓使用者點選 `<a>` link 在原 tab 跳轉頁面（沒有 `target="_blank"`）

但其實還可以使用 `window.history` 的 `pushState` method 來加入新的歷史到 stack 中（詳細使用方法請見 [MDN](https://developer.mozilla.org/en-US/docs/Web/API/History/pushState)）

`pushState` method 的特色是==並不會真的跳轉到指定的 URL==（不會實際送出 request，也不會 reload page），只有網址列中的網址會變（甚至當你沒有指定 URL 時，網址也不會變），這個 method 的主要功能除了新增歷史以外，就是設定 state。

State 可以是任何 JavaScript 中的資料型態，通常拿來紀錄進入指定頁面前的狀態，每一個歷史頁面都可以有自己的 state，且不會因為 reload page 而被清空，比如：

```JavaScript
window.history.pushState({"data": 1}, "");
console.log(window.history.state)  // {"data": 1}
window.locationl.reload();
console.log(window.history.state)  // {"data": 1}
```

# 無法竄改歷史

已經發生的歷史連查看細節都不行了，更別談要篡改。唯一可以做的就是更改目前 history stack 中的第一筆資料（目前所在頁面），須使用 `window.history` 的 `replaceState` method（詳細使用方法請見 [MDN](https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState)）。

`replaceState` 的特色與 `pushState` 相似，可以達到「更改 URL 與 state，但不實際跳轉到指定 URL」的效果。
