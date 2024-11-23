| |中文|解釋|
|---|---|---|
|**Covariance**|協變／共變|Subtype 可以被視爲 supertype、可以替代 supertype|
|**Contravariance**|逆變|Supertype 可以被視為 subtype、可以替代 subtype|
|**Invariance**|不變|Supertype 不能被視為 subtype，subtype 也不能被視爲 supertype|

# Array

令 `B` 型別為 `A` 型別的 [subtype](</Programming Language/Liskov Substitution Principle.md#Subtype vs. Subclass>)，若在某一種程式語言中，an array of `B`（簡記為 `B[]`）可以被視為 `A[]`，則該程式語言中的 array 是「協變」的；若 `A[]` 可以被視為 `B[]`，則該程式語言中的 array 是「逆變」的；若以上皆不可行，則該程式語言中的 array 是「不變」的。

==只有對於 immutable (read-only) array 而言，協變才是安全的==，舉一個可寫入且協變的 array 作為反例：

設 `Dog` 與 `Cat` 皆為 `Animal` 的 subtype，若一個 array 協變，則 `Dog[]` 與 `Cat[]` 都會被視為 `Animal[]`，若同時這個 array 是可寫入的，則可以把 `Dog` 放入 `Cat[]`，當要對這個 `Dog` 呼叫一個 `Cat` 才有的 method 或讀取一個 `Cat` 才有的 property 時，就會出錯。

因此，通常具有「協變陣列」的程式語言都會在 run time 或 compile time 針對 array 的寫入做型別檢查，若試圖把 `Dog` 放入 `Cat[]` 就拋出錯誤。

# Function

在 function 被視為「一等公民」的程式語言中，function 才具有型別，一個 function 的型別由它的輸入及輸出決定。

當一個 function $f$ 接收一個型別為 `T` 的參數，回傳值的型別為 `U`，則可以將此 function 的型別記做 $f:T \to U$。*(註："$\to$" 為「函式建構運算子」)*

令 `B` 型別為 `A` 型別的 subtype，若一個 function $f:A$ 可以填入型別為 `B` 的引數，則該程式語言中的 function 是「協變」的；若一個 function $f:B$ 可以填入型別為 `A` 的引數，則該程式語言中的 function 是「逆變」的，若都不行則該程式語言中的 function 是「不變」的。

當一個 function $f$ 所接收的參數的型別比另一個 function $g$ 所接收的參數的型別還要 general，且回傳值的型別比 $g$ 的回傳值的型別更具體 (specific)，則稱 $f$ 的型別為 $g$ 的型別的 subtype，在程式碼中 $g$ 必可以安全地被替換成 $f$。

以符號可表示成：

$$f:T1 \to U1 \leq g:T2 \to U2 \iff T2 \leq T1 \wedge U1 \leq U2$$

*(註："$\leq$" 為「子類別關係運算子」)*

也就是說，==一個 function 的參數是逆變的，輸出是協變的==，而這其實就是 [Liskov Substitution Principle](</Programming Language/Liskov Substitution Principle.md>) 的其中兩個原則。

用 OOP 的方式來說，若 class `C1` 為 class `C2` 的 subclass，且 `C1` 要 overrides `C2` 的 method `m`，則 `C1.m` 所接受的參數的型別要「與 `C2.m` 所接受的參數的型別相同」或「為 `C2.m` 所接受的參數的型別的 subtype」。

此規則可以被連續使用，比如在處理 [Higher-Order Function](</Programming Language/Higher-Order Function.md>) 時，若 $(A1 \to B) \to C \leq (A2 \to B) \to C$，則可以推導出 $A1 \leq A2$。

經由歸納還可以得到以下結論：

$$某位置是協變的 \iff 某位置的右邊共有偶數個 「\to」 符號$$

# 物件導向中的繼承

>[!Note]
>關於繼承的基本理論，詳見[此文](</Programming Language/OOP 四本柱.md#繼承 (Inheritance)>)。

「協變參數」普遍被認為是不安全的，先看一個例子：

``` Java
class AnimalShelter {
    Animal getAnimalForAdoption() {
      // ...
    }
    void putAnimal(Animal animal) {
      // ...
    }
}
class CatShelter extends AnimalShelter {
    void putAnimal(Cat animal) {
       // ...
    }
}
```

在這個例中，如果將 `CatShelter` up-casting 為 `AnimalShelter`，就可以試圖將 `Dog` 放入 `CatShelter` 中，進而導致 runtime error。

不過將參數設計為協變的思維似乎也有合理之處：「一個貓的收容所算是一種動物收容所，只是對收容動物的規定比較嚴格。」

### 一個程式語言天生就會規範參數是否為協變

在「非協變參數」的程式語言中（比如舊版的 Java），當 `RationalNumber` implements `Comparable` 時，必須在 override function 時將參數 down-casting (倒數第 7 行)：

```Java
interface Comparable {
    int compareTo(Object o);
}

class RationalNumber implements Comparable {
    int numerator;
    int denominator;
    // ...
    public int compareTo(Object other) {
        RationalNumber otherNum = (RationalNumber)other;  // down casting
        return Integer.compare(
            numerator * otherNum.denominator,
            otherNum.numerator * denominator
        );
    }
}
```

在「協變參數」的語言中，可以直接限制 `compareTo` method 接受的參數型別為 `RationalNumber`：

```Java
class RationalNumber implements Comparable {
    int numerator;
    int denominator;
    // ...
    public int compareTo(RationalNumber other) {
        return Integer.compare(
            numerator * other.denominator,
            other.numerator * denominator
        );
    }
}
```

「非協變參數」的語言則可以透過 [Generic Type](</Programming Language/Generic Type.md>) 的方式來彌補，以 `Shelter` 的例子而言：

```Java
class Shelter<T extends Animal> {
    T getAnimalForAdoption() {
        // ...
    }
    void putAnimal(T animal) {
        // ...
    }
}
class CatShelter extends Shelter<Cat> {
    Cat getAnimalForAdoption() {
        // ...
    }
    void putAnimal(Cat animal) {
        // ...
    }
}
```

以 `Comparable` 與 `RationalNumber` 的例子而言：

```Java
class RationalNumber implements Comparable<RationalNumber> {
    int numerator;
    int denominator;
    // ...
    public int compareTo(RationalNumber otherNum) {
        return Integer.compare(
            numerator * otherNum.denominator,
            otherNum.numerator * denominator
        );
    }
}
```
