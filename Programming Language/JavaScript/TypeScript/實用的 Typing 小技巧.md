### Custom Type Guard

```TypeScript
interface Square {
    sideLength: number;
}
interface Circle {
    radius: number;
}

// Declare the custom type guard
function isSquare(obj: Square | Circle): obj is Square {
    return sideLength in Square;
}

// Use the custom type guard
if (isSquare()) // ...
else // ...
```

---

### Mapped Type

```TypeScript
type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]:  () => T[K];
};
type Client = {
    name: string;
    address: string;
};
type clientGetter = Getters<Client>;

// is equivalent to:

// type clientGetter = {
//     getName: () => string;
//     getAddress: () => string;
// }
```

---

### Literal Tuple Type

```TypeScript
const sizeOptions = ["s", "m", "l"] as const;
type SizeOption = (typeof sizeOptions)[number];
```

- 型別被定義為 `SizeOption` 的變數，其值只能是 `"s"` 或 `"m"` 或 `"l"`
- 如果 `const sizeOptions = ["s", "m", "l"]` 後面沒有加上 `as const`，`type SizeOption` 其實就只是 `string` 而已
