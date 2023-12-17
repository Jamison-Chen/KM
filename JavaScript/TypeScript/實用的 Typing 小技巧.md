### Custom Type Guard

```TypeScript
interface Square {
    sideLength: number;
}
interface Circle {
    radius: number;
}
function isSquare(obj: Square | Circle): obj is Square {
    return sideLength in Square;
}
```

上例的 `isSquare` function 就是 custom type guard。

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
