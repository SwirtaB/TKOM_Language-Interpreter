# TKOM_Build-in-fractions-language-interpreter - Dokumentacja końcowa

## Cel projektu

<p align="justify">
Celem projektu jest wytworzenie interpretera wymyślonego języka. Język ma wspierać użycie zmiennych, funkcji, warunków i pętli, oraz posiadać jeden specjalny typ danych.
</p>

## Opis funkcjonalny

<p align="justify">
Wymyślony język jest opraty na C++. Posiada on silne statyczne typowanie, wspiera instrukcje warunkowe
oraz pętle. Dodatkowo wprowadza wbudowany typ pozwalający na bezpośrednie operacje na ułamkach zwykłych, co ma ułatwić 
przeprowadzanie obliczeń.
</p>

Lista wymagań:

- Interpretacja programu zapisanego w wymyślonym języku z pliku tekstowego, bądź bezpośrednio ze strumienia wejściowego.
- Kontrola poprawności leksykalnej, składniowej i semantycznej interpretowanego programu. Poprawne zgłaszanie wykrytych błędów.
- Poprawne wykonanie programu napisanego zgodnie z zasadmi języka.
- Obsługa instrukcji warunkowych.
- Obsługa pętli.
- Możliwość definiowania własnych funkcji i zmiennych.
- Komunikacja z użytkownikiem poprzez standardowe wyjście.

## Gramatyka
Gramatyka języka zapisana w EBNF.
```
(* Grammar version 1.4 *)
program = {functionDef | defineStatement};
functionDef = "fn", identifier, "(", [parameters], ")", ["->", type], statement;
functionCall = identifier, "(", [arguments] ,")";
statement = defineStatement | assignStatement | ifStatement | whileStatement | (functionCall, ";") | returnStatement | "{", { statement }, "}";


ifStatement = "if", "(", condition, ")", statement, ["else", statement];
whileStatement = "while", "(", condition, ")", statement;

condition = subCondition, [(relationalOp | logicOp), subCondition];
subCondition = [logicNegationOp], (parenthesesCondition | expression);
parenthesesCondition = "(", condition, ")";

expression = subExpression, {addOp, subExpression};
subExpression = [arithmeticNegationOp], factor, {multOp, factor};
factor = parenthesesExpression | functionCall | identifier | number | stringLiteral;
parenthesesExpression = "(", expression, ")";

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
(* Add # before "\S" if you want test it in EBNF tester *)
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
- Język: Python 3.8+ - implementacja była testowana z użyciem Python 3.9.5 
- Biblioteka i runner testów jednostkowych: unittest
- Biblioteka do wyznaczania pokrycia kodu testami: [Coverage.py](https://coverage.readthedocs.io/en/6.1.2/)

### Typy drzewa dokumentu
- __INode__ - abstakcyjna klasa bazowa zapewniająca pożądany interfejs
- __Program__ - reprezentuje program: lista zdefiniowanych funkcji i zmiennych globalnych
- __FunctionDef__ - reprezentuje definicję funkcji: identyfikator, parametry, typ zwracany, instrukcja/e do wykonania
- __FunctionCall__ - repezentuje wywołanie funkcji, w wyniku ewaluacji obiektu zostanie zwrócony wynik wywołania funkcji: identyfikator, argumenty wywołania
- __StatementBlock__ - reprezentuje blok instrukcji ujętych w nawiasy klamrowe: lista instrukcji budujących blok
- __ReturnStatement__ - reprezentuje instrukcje *__return__*: wyrażenie zwracane po ewaluacji
- __AssigneStatement__ - reprezentuje instrukcję przypisania: identyfikator zmiennej, wyrażenie
- __DefineStatement__ - reprezentuje instrukcję przypisania: typ, identyfikator zmiennej, wyrażenie
- __IfStatement__ - reprezentuje instrukcję warunkową: warunek, instrukcja/blok instrukcji, else (jako konstrukcja *__IfStatement__*)
- __WhileStatement__ - reprezentuje instrukcję pętli *__while__*: warunek, instrukcja/blok instrukcji
- __Expression__ - reprezentuje wyrażenie arytmetyczne z operatorami '__+__' i '__-__' : lewa część wyrażenia, prawa część wyrażenia, operator
- __SubExpression__ - reprezentuje wyrażenie arytmetyczne z operatorami '__*__' i '__/__' : lewy czynnik, prawy czynnik, operator, czy zanegowane
- __ParenthesesExpression__ - reprezentuje wyrażenie nawiasowe: wyrażenie
- __Condition__ - reprezentuje warunek np. *i < 0*: lewa część warunku, prawa część warunku, operator
- __SubCondition__ - reprezentuje składową warunku np. *!i*: wyrażenie, czy zanegowana
- __ParenthesesCondition__ - reprezentuje warunek ujęty w nawiasy: warunek
- __Variable__ - reprezentuje zmienną/dostęp do zmiennej: identyfikator zmiennej

### Opis modułów
Program składa się z kolejnych modułów które są odpowiedzialne za przetwarzanie danych wejściowych.
Implementacja zawiera 4 główne modułu i 2 moduły pomocnicze.

#### Główne moduły:
- Moduł leksera
- Moduł parsera
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
W wyniku pracy modułu powstaje drzewo dokumentu, które jest gotowe do interpretacji. Jest on w stanie wykryć i zgłosić podstawowe błędy.
Moduł ten ma połącznie z *Modułem obsługi błędów*, *Modułem leksera*, *Modułem interpretera* oraz *Modułem zarządzania tablicą symboli*.

#### Moduł interpretera
Realizuje proces wykonania analizowanego języka. Dostarczone dane przez *Moduł parsera* obiekty poddaje ewaluacji, jednocześnie sprawdzając ich poparwność w kontekście języka. Zgodnie z przyjętym założeniem, wynik swojego działania wypisuje na standardowe wyjście.
Ma on połączenie z *Modułem obsługi błędów*.

#### Moduł obsługi błędów
Obsługuje błędy zgłoszone przez inne moduły. Jego głównym zadaniem jest przekazanie odpowiedniej informacji zwrotnej do progamisty.

#### Moduł obsługi źródła
Moduł ma dostarczyć do *Modułu leksera* abstrakcyjne źródło danych, samemu przyjmując obowiązek zarządzania faktycznym źródłem.
Modół ten potrafi obsługiwać źrdóło plikowe i strumieniowe.

#### Moduł zarządzania tablicą symboli
Jest odpowiedzialny za obsługę tablicy symboli - w której przechowywane są infromacje o wszytskich symbolach rozpoznawanych przez lekser.

### Testowanie
Niniejszy projekt udostępnia dwa zestawy testów:
- testy modułów - w formie testów jednostkowych dla każdego z modułów w celu weryfikacji poprawności jego działania.
- testy potoku przetwarzania - program dostaje na wejście plik lub strumień znaków z programem napisanym w proponowanym języku, dokonuje analizy leksykalnej, składniowej i interpretacji. Wynik wypisuje na standardowe wyjście (zgodnie z zapisem programu). Testy te zostały napisane z użyciem biblioteki *__unittest__* co pozwala na proste ich uruchomienie i weryfikację poprawności wyniku.

## Podręcznik użytkownika

### Cechy języka
- Każda zmienna musi posiadać typ - silne statyczne typowanie.
- Zmienne mogą być definiowa w zasięgu globalnym i lokalnym, możliwe jest przysłaniane zmiennych.
Ponowna definicja zmiennej w tym samym zasięgu (redefinicja) jest niepoprawna i skutkuje błędem.
- Typy wbudowane to: __int__, __float__, __frc__ - typ ułamkowy, __string__ - typ napisowy.
- Nie dopuszcza się istnienia innych typów niż wyżej wymienione.
- Język pozwala na rzutowanie typu za pomocą wbudowanych funkcji, udostępnione zostały nastepujące rzutowania:
    - *int -> frc*
    - *int -> float*
    - *frc -> float*
    - *float -> int* (zaokrąglenie w dół do najbliższej liczby całkowitej)
    - *frc -> int* (zaokrąglenie w dół do najbliższej liczby całkowitej)
    - *int -> string*
    - *float -> string*
    - *frc -> string*
- W szczególności w języku nie wystepują automatyczne konwersje między typami.
- Funkcja musi być od razu zdefiniowana.
- Funkcje mogą być definiowane tylko w zasiegu globalnym i nie mogą być nadpisywane/przeciążane.
- Funkcja może nie mieć wartości zwracanej, wówczas wyrażenie zapisane po słowie kluczowym *return* zostanie zignorowane.
- W przypadku gdy funkcja zwraca wartość typ wyrażenia za słowem kluczowym *return* zostanie porównany z deklarownym, w przypadku różnicy będzie to błąd.
- W przypadku gdy funkcja nie zwraca wartości, a chcemy z niej wyjść należy napisać *return 0;*.
- W wyrażeniach warunkowych nie można tworzyć, ani przypisywać wartości. Można natomiast wykonywać operacje arytmetyczne, lub używać wywołań funkcji.
- Wartości boolowskie (__true__, __false__) są reprezentowane przez typ __int__: 
    - *false* -> 0
    - *true* -> wszytsko inne
- Język definiuje cztery podstawowe operacje arytmetyczne: __dodawanie__, __odejmowanie__, __mnożenie__, __dzielenie__.
- Operacje można wykonywać tylko na tych samych typach.
- Dozwolone operacje:
    - *__string__ + __string__* - konkatenacja napisów
    - wszytskie operacje dla typu __int__, __float__ i __frc__
- Język wspiera komentowanie kodu. Format komentarzy: *# komentarz* . Komentarz kończy się wraz z końcem linii.
- Każdy program musi posiadać funkcję __main__, jest ona punktem wejścia do programu.
- Każda instrukcja z wyłączeniem instrukcji blokowych (*__fn__*, *__while__*, *__if__*) musi kończyć się średnikiem.

### Przykładowe konstrukcje języka
Każdy program musi posiadać funkcję __main__. Funkcję definiujemy w następujący sposób __fn identyfikator ( [*parametry*] ) [* -> typ zwracany*] ciało funkcji__   
Funkcja __main__ nie posiada żadnych argumentów, może ona zwracać wartość, ale nie musi. W przypadku, gdy zwraca wartość na standardoweym wyjściu pojawi się wynik działania programu.
```
fn main() -> int {
    int a = 0;
    int b = 0;
    return a + b;
}
```
Zmienne globalne definiujemy w ten sam sposób jak zmienne lokalne, definicja odbywa się poza nawiasami klamrowymi.
Zmienne mogą zostać zdefiniowane przed lub po ich pierwszym użyciu w kontekście funkcji, gdyż zakres globalny jest ewaluowany przed rozpoczeciem wykonywania instrukcji w funkcji __main__.
```
int globalVariable = 1;

fn main() -> int {
    return globalVariable + 1;
}
```
Możliwe jest definiowanie własnych funkcji. Definicja wygląda w ten sam sposób co dla funkcji __main__. Funkcje użytkownika mogą posaidać parametry i zwracać wartość. 

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
Przykład funkcji nie zwracająca wartości.

```
fn no_return_function(int a, int b) {
    print(int_to_string(a + b));
}
```
Język wspiera pętle w postaci pętli *while*. W warunku nie możemy definiować zmiennych, możemy za to korzystać z wyrażeń.

```
fn main() -> int {
    int i = 0;
    while(i < 100){
        i = i + 1;
    }
    return i;
}
```
Obsługiwane są również wyrażenia warunkowe. Warto zaznaczyć, że pojedyńcze instrukcje nie wymagają otwarcia nawisów klamrowych. Dotyczy to wszytskich instrukcji blokowych.

```
if(i < 100) 
    i = 101;

...

if(i < 100)
    return 0;
else {
    ...
    some instructions
    ...
}

```
Przypisanie wartości odbywa się intuicyjnie z użyciem znaku '*=*'. By utworzyć zmienną typu *frc* należy skorzystać z wbudowanej funkcji *frc(int licznik, int mianownik)*.

```
float floatVar = 0.15;
frc fraction = frc(1,2);

...

floatVar = 1.0;
fraction = frc(2, 5);
```
Interpretar udostępnia bibliotekę standardową w której zdefiniowane są dostępne rzutowania. Więcej informacji w sekcji __Biblioteka standardowa__ i __Cechy języka__.

```
float floatVar = int_to_float(int_ret_fun());
```

Poniżej przykłady użycia komentarzy.

```
# pojedyńczy komentarz

...

# linia pierwsza komentarza
# linia drugra komentarza
```

Więcej bardziej rozbudowanych przykładów znajdzieś [tutaj](Tests/grammar) i [tutaj](Tests/acceptance).

### Biblioteka standardowa

Język udostępnia bibliotekę standardową oferującą podstawowe funkcje:
- __print(string)__ - wypisanie zmiennej typu *__string__* na standardowe wyjście
- __frc(int, int) -> frc__ - zwraca zmienną typu *__frc__*, jako argumenty przyjmuje licznik i mianownik  ułamka
- __int_to_frc(int) -> frc__ - rzutowanie typu *__int__* na typ *__frc__*
- __int_to_float(int) -> float__ - rzutowanie typu *__int__* na typ *__float__*
- __frc_to_float(frc) -> float__ - rzutowanie typu *__frc__* na typ *__float__* - wykonuje dzielenie licznik/mianownik
- __float_to_int(float) -> int__ - rzutowanie typu *__float__* na typ *__int__* - zaokrąglenie w dół do najbliższej liczby całkowitej
- __frc_to_int(frc) -> int__ - rzutowanie typu *__frc__* na typ *__int__* - zaokrąglenie w dół do najbliższej liczby całkowitej
- __frc_to_string(frc) -> string__ - rzutowanie typu *__frc__* na typ *__string__*
- __float_to_string(float) -> string__ - rzutowanie typu *__float__* na typ *__string__*
- __int_to_string(int) -> string__ - rzutowanie typu *__int__* na typ *__string__*

### Operatory

- __+__ - dodawanie
- __-__ - odejmowanie/negacja arytmetyczna - np. -int_return_fun()
- __\*__ - mnożenie
- __/__ - dzielenie - w przypadku dzielenie __int/int__ jest to dzielenie całkowito liczbowe - zaokrąglenie wyniku w dół
- __!__ - negacja logiczna
- __<__ - mniejsze niż
- __>__ - większe niż
- __<=__ - mniejsze równe
- __>=__ - większe równe
- __==__ - równe
- __!=__ - nierówne

### Uruchomienie
- Interpreter uruchamiamy wykorzystując program *__Bif-il.py__* posiadający następujące opcje uruchomienia:
    - *-f /ścieżka/do/pliku* - uruchomienie w trybie interpretacji programu z podanego pliku
    - *-t 'program napisany w języku'* - uruchomienie w trybie interpretacji programu ze strumienia wejściowego
    - *-h* - wyświetla pomoc uruchomienia programu
- Komunikaty programu (wynik/przebieg działania intepretowanego kodu, błędy) wyświetlane są na standardowym wyjściu.
- Interpreter nie pozwala na wejście w interakcję z użytkownikiem

### Uruchomienie testów i sprawdzenie pokrycia kodu
- należy pobrać bibliotekę [Coverage.py](https://coverage.readthedocs.io/en/6.1.2/)
- testy uruchamiamy wykonując polecenie
    > coverage run -m unittest discover -v
- raport z testów
    > coverage report -m
- wykonanie zestawu testów *InterpreterPositiveTestSuite* bez błędów świadczy o poprawnym zinterpretowaniu przykładowych programów. Kod ich można znaleźć w pliku *test_interpreter.py*