假設 B 型別為 A 型別的 [[Subtype vs. Subclass]]，若在某一種程式語言中，一個 `B[]` 可以被視為一個 `A[]`，則該程式語言中的 array 為「協變陣列」；若一個 `A[]` 可以被視為一個 `B[]`，則該程式語言中的 array 為「逆變陣列」；若以上皆不可行，則該程式語言中的 array 為「不變陣列」。若一個有參數且參數型別為 `A` 的 function $f$（簡記為 $f:A$）可以填入型別為 `B` 的引數，則該程式語言中的 function 為「協變函式」；若一個 $f:B$ 可以填入型別為 `A` 的引數，則該程式語言中的 function 為「逆變函式」，若都不行則稱為「不變函式」。

### Array

只有對於 immutable (read-only) array 而言，協變才是安全的，若 array 可寫入且協變，則當 `Dog` 與 `Cat` 皆為 `Animal` 的子型別時，是可以把 `Dog` 放入一個 `Cat[]` 的。因此，通常具有「協變陣列」的程式語言都會在 runtime 或 compile time 針對 array 的寫入做型別檢查，若試圖把 `Dog` 放入 `Cat[]` 就拋出錯誤。

### Function

在 function 被視為「一等公民」的程式語言中，function 具有型別，一個 function 的型別由它的輸入及輸出決定。比如當一個 function $f$ 接收型別為 `T` 的參數，return 型別為 `U` 的值，則可以將此 function 的型別記做 $f:T \to U$。

 *(註："$\to$" 為「函式建構運算子」)*

當一個 function $f$ 所接收的參數的型別比另一個 function $g$ 所接收的參數的型別還要 general，且 return value 的型別比 $g$ 的 return value 的型別更具體 (specific)，則稱 $f$ 的型別為 $g$ 的型別的 subtype，在程式碼中 $g$ 必可以安全地被替換成 $f$。以符號可表示成：

$$f:T1 \to U1 \leq g:T2 \to U2 \iff T2 \leq T1 \wedge U1 \leq U2$$

*(註："$\leq$" 為「子類別關係運算子」)*

也就是說在 function 中，==參數是逆變的，輸出是協變的==，而這其實就是[[Liskov Substitution Principle (LSP)]]的其中兩個原則。

此規則可以被連續使用，比如在處理[[Higher-Order Function (HOF)]]時，若 $(A1 \to B) \to C \leq (A2 \to B) \to C$，則可以推導出 $A1 \leq A2$。

因此，經由歸納可以得到以下結論：

$$某位置是協變的 \iff 某位置的右邊共有偶數個 \to 符號$$

### 物件導向中的繼承

（關於繼承的基本理論，詳見 [[OOP 四本柱#繼承 (Inheritance)|此文]]。）

在物件導向語言中，理論上必須規定：若 subclass overrides superclass 的 method，則 subclass 的 method 的型別要「與 superclass 的 method 的型別相同」或「為 superclass 的 method 的型別的 subtype」。

然而事實上在部分語言（如 Eiffel）中，method 的參數是被設計為協變的：

``` Java
class AnimalShelter {
    Animal getAnimalForAdoption() {
      ...
    }

    void putAnimal(Animal animal) {
      ...
    }
}

class CatShelter extends AnimalShelter {
    void putAnimal(Cat animal) {
       ...
    }
}
```

「協變參數」是不安全的，以上例而言，如果將 `CatShelter` up-casting 為 `AnimalShelter`，就可以試圖將 `Dog` 放入 `CatShelter` 中，進而導致 runtime error。

拋開型別安全問題不談，協變參數語言的設計者的想法似乎也有合理之處：「一個貓的收容所算是一種動物收容所，只是對收容動物的規定比較嚴格。」

「協變參數」其中一個派得上用場的地方，就是在 [[程式語言理論/零碎筆記#Binary Method|Binary Method]] 中。在「非協變參數」的程式語言中（比如舊版的 Java），當 `RationalNumber` implements `Comparable` 時，必須在 override function 時將參數 down-casting (倒數第 5 行)：

```Java
interface Comparable {
    int compareTo(Object o);
}

class RationalNumber implements Comparable {
    int numerator;
    int denominator;

    ...
    
    public int compareTo(Object other) {
        RationalNumber otherNum = (RationalNumber)other;
        return Integer.compare(
            numerator * otherNum.denominator,
            otherNum.numerator * denominator
        );
    }
}
```

但在「協變參數」的程式語言中，可以直接限制 `compareTo` method 接受的參數型別為 `RationalNumber`：

```Java
class RationalNumber implements Comparable {
    int numerator;
    int denominator;

    ...
    
    public int compareTo(RationalNumber other) {
        return Integer.compare(
            numerator * other.denominator,
            other.numerator * denominator
        );
    }
}
```

但其實「非協變參數」的語言也可以透過 [[泛型 (Generic)]] 的方式來彌補，比如：

```Java
class Shelter<T extends Animal> {
    T getAnimalForAdoption() {
        ...
    }

    void putAnimal(T animal) {
        ...
    }
}

class CatShelter extends Shelter<Cat> {
    Cat getAnimalForAdoption() {
        ...
    }

    void putAnimal(Cat animal) {
        ...
    }
}
```

或者：

```Java
class RationalNumber implements Comparable<RationalNumber> {
    int numerator;
    int denominator;
  
    ...
     
    public int compareTo(RationalNumber otherNum) {
        return Integer.compare(
            numerator * otherNum.denominator,
            otherNum.numerator * denominator
        );
    }
}
```
