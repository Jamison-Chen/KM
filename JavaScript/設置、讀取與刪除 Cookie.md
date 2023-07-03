### 設置 Cookie

使用 `document.cookie` API 可以對 browser 的 cookies  進行 "get" 與 "set"。其中，"set" cookie 的方式如下：

```JavaScript
document.cookie = "my_cookie=a1234"
```

注意，上面的語法只會新增或修改 `my_cookie` 這個 cookie 的值，並不會把其它已存在的 cookie 清除。

### 讀取與刪除 Cookie

```TypeScript
function getCookie(key: string): string | null {
    const divider = key + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(";");

    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === " ") c = c.substring(1);
        if (c.indexOf(divider) === 0) {
            return c.substring(divider.length, c.length);
        }
    }

    return null;
}

function deleteCookie(key: string): void {
    if (getCookie(key)) {
        const d = new Date();
        d.setTime(d.getTime() - 10);
        document.cookie = `${key}=;expires=${d.toUTCString()};path=${Env.frontendRootPath}`;
        document.cookie = `${key}=;expires=${d.toUTCString()};path=/`;
    } else throw Error("Cookie Not Found");
}
```