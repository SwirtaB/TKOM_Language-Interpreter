# TKOM_Language-Interpreter - Dokumentacja wstępna

## Cel projektu

<p align="justify">
Celem projektu jest wytworzenie interpretera wymyślonego języka. Język ma wspierać użycie zmiennych, funkcji, warunków i pętli, oraz posiadać jeden specjalny typ danych.
</p>

## Opis funkcjonalny

<p align="justify">
Wymyślony język jest opraty na połaczeniu C++ i Pythona. Posiada on silne statyczne typowanie, wspiera instrukcje warunkowe
oraz pętle. Dodatkowo wprowadza wbudowany typ pozwalający na bezpośrednie operacje na ułamkach zwykłych, co ma ułatwić 
przeprowadzanie obliczeń.
</p>

Zostały przyjęte następujące założenia:
- Każda zmienna i funkcja musi posiadać typ -> silne statyczne typowanie.
- Typy wbudowane to: __int__, __float__, __frc__ - typ ułamkowy, __string__ - typ napisowy.
- Nie dopuszcza się istnienia innych typów niż wyżej wymienione.
- Język pozwala na rzutowanie typu, dopuszcza się następujące rzutowania:
    - *int -> frc*
    - *frc -> float*
    - *float -> int* (poprzez zaokrąglenie w górę)
    - *int -> string*
    - *float -> string*
- Funkcja musi być od razu zdefiniowana.
- W wyrażeniach warunkowych nie można tworzyć, ani przypisywać wartości. Można natomiast wykonywać operacje matematyczne, lub używać wywołań funkcji.
- Wartości boolowskie (true, false) są reprezentowane przez typ __int__, przyjmuję: 
    - *false* -> 0
    - *true* -> wszytsko inne
- Język definiuje cztery podstawowe operacje matematyczne: __dodawanie__, __odejmowanie__, __mnożenie__, __dzielenie__.
- Dla zdefiniowanych typów dozwolone są wszystkie powyższe operacje z wyjątkiem *float* dla którego nie dopuszcza się żadnej operacji z typem *frc*
- Język wspiera komentowanie kodu. Format komentarzy: *# komentarz* . Komentarz kończy się wraz z końcem linii.

### Przykładowe konstrukcje języka


```
fn main() -> int {
    int a = 0;
    int b = 0;
    return a + b;
}
```
<span style="font-size:0.9em">
Używanie zmiennych globalnych
</span>

```
int globalVariable = 1;

fn main() -> int {
    return globalVariable + 1;
}
```
<span style="font-size:0.9em">
Definiowanie i wołanie funkcji
</span>

```
fn add(int a, int b) -> int{
    return a + b;
}

fn main() -> int {
    int a = 1;
    int b = 2;
    int c = add(a,b);
    return c;
}
```
<span style="font-size:0.9em">
Funkcje nie zwracjaące wartości
</span>

```
fn no_return_function(int a, int b) {
    int c = a + b;
}
```
<span style="font-size:0.9em">
Pętla
</span>

```
fn main() -> int {
    int i = 0;
    while(i < 100){
        i = i + 1;
    }
    return i;
}
```
<span style="font-size:0.9em">
Blok if
</span>

```
if(i < 100) {
    i = 101;
}
```
<span style="font-size:0.9em">
Przypisywanie wartości
</span>

```
float floatVar = 0.15;
frc fraction = frc(1,2);
```
<span style="font-size:0.9em">
Rzutowanie typu
</span>

```
float floatVar = float(int_ret_fun());
```

<span style="font-size:0.9em">
Komentowanie
</span>

```
# pojedyńczy komentarz

# linia pierwsza komentarza
# linia drugra komentarza
```

Więcej bardziej rozbudowanych przykładów znajdzieś [tutaj](tests/grammar).

## Gramatyka
Gramatyka języka zapisana w EBNF.
```
(* Grammar version 1.4 *)
program = {functionDef | defineStatement};
functionDef = "fn", identifier, "(", [parameters], ")", ["->", type], statement;
functionCall = identifier, "(", [arguments] ,")";
statement = defineStatement | assignStatement | ifStatement | whileStatement | (functionCall, ";") | returnStatement | "{", statement, "}";


ifStatement = "if", "(", condition, ")", statement, ["else", statement];
whileStatement = "while", "(", condition, ")", statement;

condition = subCondition, [(relationalOp | logicOp), subCondition];
subCondition = [logicNegationOp], (parenthesesCondition | expression);
parenthesesCondition = "(", condition, ")";

expression = subExpression, {addOp, subExpression};
subExpression = [arithmeticNegationOp], factor, {multOp, factor};
factor = parenthesesExpression | functionCall | identifier | number | stringLiteral;
parenthesesExpression = [type], "(", expression, ")";

parameters = type, identifier, {",", type, identifier};
arguments = expression, {",", expression};

defineStatement = type, identifier, [assignOp, expression],";";
assignStatement = identifier, assignOp, expression, ";";
returnStatement = "return", expression, ";";

logicNegationOp = "!";
arithmeticNegationOp = "-";
assignOp = "=";
relationalOp = "<" | "<=" | ">" | ">=" | "==" | "!=";
logicOp = "&&" | "||";
addOp = "+" | "-";
multOp = "*" | "/";
type = "int" | "float" | "frc" | "string";

identifier = letter, {digit | letter};
number = digit, {digit}, [".", {digit}];
stringLiteral = '"', {visibleChar}, '"';

digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
letter = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s"
| "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
| "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "_";
(* Add # if you want test it in EBNF tester *)
visibleChar = "\S";
```
Symbole terminale
```
"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "_",
".", "!", "=", "<", "<=", ">", ">=", "==", "!=", "+", "-", "*", "/", ";", "->", "&&", "||" "int", "float", "frc", "(", ")", "fn", "if", "else", 
"while", "return", wszystkie symbole dopasowane przez regex \S
```
### Zarezerwowane słowa języka
> "int", "float", "frc", "string", "fn", "if", "else", "while", "return"

### Symbole języka
> ".", "!", "=", "<", "<=", ">", ">=", "==", "!=", "+", "-", "*", "/", ";", "->", "(", ")", "{", "}", "&&", "||"

## Implementacja

### Środowisko
- Język: Python
- Biblioteka i runner testów jednostkowych: unittest
- Biblioteka do wyznaczania pokrycia kodu testami: [Coverage.py](https://coverage.readthedocs.io/en/6.1.2/)

### Uruchomienie
- Program uruchamiany z terminala.
- Program przyjmuje jako parametr ścieżkę do pliku z interpretowanym kodem lub ciąg znaków będący kodem programu.
- Komunikaty programu (wynik/przebieg działania intepretowanego kodu, błędy) będą wyświetlane na standardowym wyjściu.
- Nie przewiduję interkacji z użytkownikiem po uruchomieniu programu.

### Sprawdzenie pokrycia kodu testami
- należy pobrać bibliotekę [Coverage.py](https://coverage.readthedocs.io/en/6.1.2/)
- testy uruchamiamy wykonując polecenie
    > coverage run -m unittest discover -v

### Opis modułów
Program będzie składał się z kolejnych modułów które są odpowiedzialne za przetwarzanie danych wejściowych.
Planuje implementację 5 głównych modułów i 2 modułów pomocniczych.

#### Główne moduły:
- Moduł leksera
- Moduł parsera
- Moduł analizy semantycznej
- Moduł interpretera
- Moduł obsługi błędów

#### Moduły pomocnicze:
- Moduł obsługi źródła
- Moduł zarządzania tablicą symboli

#### Moduł leksera
Realizuje analizę leksykalną, otrzymane od *Modułu obsługi źródła* znaki grupuje w tokeny w sposób leniwy.
Jest w stanie wykryć błędy leksykalne i zgłosić je do *Modułu obsługi błędów*. Dodatkowo przyjąłem założenie, 
że pojawiające się w kodzie komentarze będą rozpoznawane przez ten moduł i ignorowane (znaki budujące komentarz nie będą przekazywane dalej).
Ma on połączenie z *Modułem obsługi błędów*, *Modułem obsługi źródła*, *Modułem zarządzania tablicą symboli* oraz *Modułem parsera*.

#### Moduł parsera
Realizuje analizę składiową. Pobiera od *Modułu leksera* kolejne tokeny i weryfikuje czy są one zgodne z gramtyką języka.
W wyniku pracy modułu powstaje drzewo składniowe. Jest on w stanie wykryć i zgłosić podstawowe błędy.
Moduł ten ma połącznie z *Modułem obsługi błędów*, *Modułem leksera*, *Modułem analizy semantycznej* oraz *Modułem zarządzania tablicą symboli*.

#### Moduł analizy semantycznej
Realizuje analizę semantyczną - sprawdza czy struktury składniowe mają "odpowiednie" znaczenie w kontekście interpretowanego języka.
Przewiduje typy wyrażeń pośrednich, weryfikuje czy żądane operacje są dozwolone dla danych typów itp. Wynika z tego, że może on wychwycić szereg błędów semantycznych. Ma on połączenie z *Modułem obsługi błędów*, *Modułem parsera*, *Modułem interpretera* oraz *Modułem zarządzania tablicą symboli*.

#### Moduł interpretera
Realizuje proces wykonania analizowanego języka. Dostarczone dane przez *Moduł analizy semantycznej* przetwarza na ciąg prostych instrukcji, które następnie są wykonywane. Zgodnie z przyjętym założeniem, wynik swojego działania wypisuje na standardowe wyjście.
Ma on połączenie z *Modułem obsługi błędów*.

#### Moduł obsługi błędów
Obsługuje błędy zgłoszone przez inne moduły. Jej głównym zadaniem jest przekazanie odpowiedniej informacji zwrotnej do progamisty.

#### Moduł obsługi źródła
Moduł ma dostarczyć do *Modułu leksera* abstrakcyjne źródło danych, samemu przjmując obowiązek zarządzania faktycznym źródłem.
Planuję by modół ten potrafił obsługiwać źrdóło plikowe i strumieniowe.

#### Moduł zarządzania tablicą symboli
Jest odpowiedzialny za obsługę tablicy symboli - w której przechowywane są infromacje o wszytskich symbolach rozpoznawanych przez lekser, 
przechowywanie informacji o symbolach zdefiniowanych przez użytkownika. 

### Testowanie
Planuję przprowadzać dwa typy testów:
- testy modułów - testy jednostkowe każdego z modułów z osobna do weryfikacji poprawności działania konkretnego modułu.
- testy potoku przetwarzania - w ciagu postępujących prac na wejście programu będa wrzucane przypadki testowe, które zostaną częsciowo przetworzone (na tyle na ile pozwala obecna implementacja). Taki wynik pośredni będzie analizowany w celu zweryfikowania poprawności działania fragmentu potoku przetwarzania. Na koneic prac te testy pozwolą na przetestowanie całego programu.

