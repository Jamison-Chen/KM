# Escape Character（跳脫字元）

在程式語言中，字串中若有==某些特殊的字元組合會觸發特殊的 stdout 或行為，而非直接印出這些字元==，則稱這些特殊的字元組合為 escape characters。

舉例來說，在大部分的程式語言中，當要 stdout 的字串中出現 `\n` 時，並不會真的印出 `\n`，而是會在 `\n` 出現的地方進行「換行」。

### 常見的 Escape Characters

|Code|Result|Description|
|:-:|:-:|:-:|
|`\'`|`'`|多數程式語言的字串可以以 `''` 包覆，這類語言若要印出 `'` 就須使用 escape character，否則會被視為包覆字串用的符號。|
|`\"`|`"`|多數程式語言的字串可以以 `""` 包覆，這類語言若要印出 `"` 就須使用 escape character，否則會被視為包覆字串用的符號。|
|`\\`|`\`|多數程式語言是以 `\` 作為跳脫字元的開頭，這類語言若要印出 `\` 就須使用 escape character，否則會被視為跳脫字元的開頭。|
|`\n`|line feed|換行，詳見 [CR, LF](</Computer Science/CR, LF.md>)。|
|`\r`|carriage return|回到一行的開頭，詳見 [CR, LF](</Computer Science/CR, LF.md>)。|
|`\t`|tab|視同按下鍵盤的 tab 鍵，多用於縮排 (indentation)。|
|`\f`|form feed|換行，並且將新的一行縮排至上一行的結尾處。|
|`\b`|backspace|視同按下鍵盤的 backspace 鍵，也就是刪掉上一個輸出的字元。|
|`\u____`|[Unicode](</Computer Science/Character Encoding & Decoding.md#Unicode>)|後面接著四位 16 進制的英數字，會印出該 Unicode 所對應的字元，比如 `\u0410` 代表 `A`。|
|`\___`|octal value|後面接著三位 8 進制的數字，會印出該 octal value 所對應的字元，比如 `\101` 代表 `A`。|
|`\x__`|hex value|後面接著兩位 16 進制的英數字，會印出該 hex value 所對應的字元，比如 `\x41` 代表 `A`。|
