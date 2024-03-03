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
