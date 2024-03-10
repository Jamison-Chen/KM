每個 `Event` object 都會有一個叫 `eventPhase` 的 attribute，`eventPhase` 依順序分為三種：

- Capturing phase
- At target
- Bubbling phase

比如當你點擊表格中的某個 cell 時， mouse click event 的傳遞過程會如下圖：

![[javascript-event-propagation.png]]

# 誰是 Target？

Target 的定義是「所有接收到 event 的 DOM elements 中的所有 leaf elements」

# 如何捕獲？

[MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)

有時候你可能會希望某個不是 target 的 element （但 target 在它底下）可以捕獲 event，此時你有兩種做法：

- 在 `addEventListener` 的第三個參數如果放 boolean，則 `true` 就是要捕獲，`false` 就是不要捕獲，預設為 `false`。

    ```JavaScript
    myElement.addEventListener("click", (e) => {
      // ...
    }, true)
    ```

- 在 `addEventListener` 的第三個參數如果放一個 object，且該 object 中有一個 key 叫 `capture`、value 為 boolean 的 attribute，則 `true` 就是要捕獲，`false` 就是不要捕獲，預設為 `false`。

    ```JavaScript
    myElement.addEventListener(
        "click",
        (e) => {
            // ...
        },
        { capture: true }
    );
    ```


# 如何阻止事件繼續傳遞下去？

### `stopPropagation`

捕獲一個並不代表阻擋它，所以 event 會繼續傳遞 (propagate) 下去／上去，如果希望 event 不要繼續傳遞，則要在 event handler 中呼叫 event object 的 `stopPropagation` method：

```JavaScript
myElement.addEventListener("click", (e) => {
  e.stopPropagation();
});
```

### `stopImmediatePropagation`

`stopPropagation` 只會阻止事件往下／上一層傳，不會阻止同一個 element 上的其他 event listeners 被觸發（event listener 會依照 register 的順序被觸發），若要阻止同一個 element 上的其他 event listeners 被觸發，則須呼叫 `stopImmediatePropagation` method：

```JavaScript
myElement.addEventListener("click", (e) => {
  e.stopImmediatePropagation();
});
```

# `preventDefault` 與事件傳遞無關

[MDN Web Docs](https://developer.mozilla.org/zh-TW/docs/Web/API/Event/preventDefault)

呼叫 event object 的 `preventDefault` method 只是避免執行瀏覽器對該類型事件的預設行為，並不會阻止事件的傳遞。但須注意的是，一旦事件傳遞鏈前方的 event listener 呼叫了 `preventDefault`，這個 event 就會一直帶著這個 flag 到後續的 event handler 中，所以後續 elements 的對此事件的預設行為都不會被觸發。

# 參考資料

- <https://blog.huli.tw/2017/08/27/dom-event-capture-and-propagation/>
- <https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener>
- <https://developer.mozilla.org/zh-TW/docs/Web/API/Event/preventDefault>
