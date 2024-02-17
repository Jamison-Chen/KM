Module system（模組系統）是 JavaScript 在 [[ES5 vs ES6|ES6]] 才引入的概念。

# Module Import & Export in ES6

若要在 client-side JavaScript 中使用 `import`/`export` statement，則必須在 html 引入 root script 時聲明 `type="module"`，像是這樣：

```html
<script type="module" src="./js/main.js"></script>
```

### Export

```JavaScript
// lib.js
export const aString = "test";

export function aFunction() {
    console.log("function test");
}

export const aObject = { a: 1 };

export class aClass {
    constructor(name) {
        this.name = name;
    }
}
```

### Import

```JavaScript
import { aObject, aString } from "./lib.js";

console.log(aString);
console.log(aObject);
```

or

```JavaScript
import * as myModule from "./lib.js";

console.log(myModule.aString);
console.log(myModule.aObject);

myModule.aFunction();
const newObj = new myModule.aClass("Inori", 16);
console.log(newObj);
```

### Export Default

```JavaScript
// lib2.js
function aFunction(param) {
    return param * param;
}

export default aFunction;
```

一個 module 只能有一個 `export default` statement。

### Import Default

```JavaScript
import aFunction from "./lib2.js";

console.log(aFunction(5));
```

Import 的東西若沒有 `{}` 包裹，就是在 import default，此時若 imported file 中有 `export default xxx` 語句，就會將 `xxx` import 進來；若 imported file 中沒有 `export default xxx` 語句，就會噴 SyntaxError。

# CommonJS vs. AMD

雖說模組系統是 JavaScript 在 ES6 才引入的概念，然而在 ES6 之前，社群上已發展了兩套較知名的模組系統，它們分別是 CommonJS 與 AMD (Asynchronous Module Definition)。

- CommonJS 在載入模組時是 synchronous 的；AMD (Asynchronous Module Definition) 則是 asynchronous 的
- CommonJS 是給 server-side 的 Node.js 用的；AMD 則適合 client-side 使用
- CommonJS 人如其名，在 import/export 模組所使用的語法是與其他主流程式語言更像的；相對的 AMD 的 import/export 方式則很繁瑣

# Dynamic Import

#TODO 

- <https://dmitripavlutin.com/ecmascript-modules-dynamic-import/>
- <https://medium.com/unalai/%E8%AA%8D%E8%AD%98-dynamic-import-3a6f75da2fc9>

# Import vs. Require

#TODO 

# Module System in Node.js

在 [[JavaScript/Node.js/Introduction|Node.js]] 中，不能直接在副檔名為 .js 的檔案中寫 `import`/`export` statement，必須將副檔名改為 **.mjs**（聲明這是一個 module file）。

# 參考資料

- <https://www.greatfrontend.com/questions/quiz/what-do-you-think-of-amd-vs-commonjs>
- <https://eyesofkids.gitbooks.io/javascript-start-from-es6/content/part4/module_system.html>
