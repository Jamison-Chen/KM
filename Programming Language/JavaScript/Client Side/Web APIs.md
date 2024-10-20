[MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API)

Web APIs 是一系列瀏覽器原生（由瀏覽器提供而非 JavaScript engine 提供）的 APIs，這些 APIs 只有在瀏覽器中可以使用，但某些 API 名稱也被 server side runtime 拿去當作類似功能的 API 名稱。舉例來說，Web APIs 中的 `console.log` 的功能是將輸出值 stdout 在瀏覽器的 developer tool 中；在 Node.js 則是拿來將輸出值 stdout 在 terminal 中。

其中一個 client-side runtime 與 server-side runtime 最大的差別就是 client side 有許多與 event listening 相關的 Web APIs（因為在 client side 要處理各式各樣的 user actions 才能與 user 互動）。
