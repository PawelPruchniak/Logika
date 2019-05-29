import sys

#funkcje dające wynik A,K,N,C,E
def koniunkcja(p,q):
    if p and q:
        return 1
    else:
        return 0
def alternatywa(p,q):
    if p or q:
        return 1
    else:
        return 0
def implikacja(p,q):
    if p and not q:
        return 0
    else:
        return 1
def negacja(p):
    if p:
        return 0
    else:
        return 1
def rownowaznosc(p,q):
    if (p and q) or (not p and not q):
        return 1
    else:
        return 0

#>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>

#funkcja tworzy liste zdań np. p , q itp  | przyjmuję: całą formułę | zwraca: liste zdań |
def stworz_liste_zdan(formula):
    tabela_zdan = []
    for letter in formula:
        if letter.islower() and letter not in tabela_zdan:
            tabela_zdan.append(letter)

    return tabela_zdan

#funkcja zamienia duże litery na znaki np E = ⇔ | przyjmuję: literę | zwraca: znak |
def zmiana_uppercase_letter(letter):
    if letter == 'K':
        letter = '∧'
    elif letter == 'C':
        letter = '⇒'
    elif letter == 'E':
        letter = '⇔'
    elif letter == 'A':
        letter = '∨'
    elif letter == 'N':
        letter = '¬'
    else:
        letter = '?'
    return letter

#funkcja tworzy liste podformuł  tj. do tabeli zdań dodaje wszystkie kolejne podformuły | przyjmuję: całą formułę | zwraca: liste podformuł |
def tworzenie_listy_podformul(formula):
    cała_formuła = formula
    wyrazenia = []
    ilosc_wyrazen = 0
    tabela_zdan = stworz_liste_zdan(cała_formuła)
    while (len(cała_formuła) != 1):
        licznik = len(cała_formuła)
        for letter in reversed(cała_formuła):
            licznik = licznik - 1
            if letter.isupper():
                uppercase_letter = letter
                lowercase_letter_1 = cała_formuła[licznik + 1]
                if uppercase_letter != 'N':
                    lowercase_letter_2 = cała_formuła[licznik + 2]
                break;
        uppercase_letter = zmiana_uppercase_letter(uppercase_letter)
        if (uppercase_letter != '¬'):
            wyrazenia.append(lowercase_letter_1 + uppercase_letter + lowercase_letter_2)
            del cała_formuła[licznik + 1]
            del cała_formuła[licznik + 1]
            cała_formuła[licznik] = wyrazenia[ilosc_wyrazen]
            if licznik > 0:
                cała_formuła[licznik] = '(' + cała_formuła[licznik] + ')'
            ilosc_wyrazen = ilosc_wyrazen + 1
        else:
            wyrazenia.append(uppercase_letter + lowercase_letter_1)
            del cała_formuła[licznik + 1]
            cała_formuła[licznik] = wyrazenia[ilosc_wyrazen]
            if licznik > 0 and len(cała_formuła[licznik]) > 2:
                cała_formuła[licznik] = '(' + cała_formuła[licznik] + ')'
            ilosc_wyrazen = ilosc_wyrazen + 1

    global liczba_zdan
    global liczba_podformuł
    liczba_zdan = len(tabela_zdan)
    liczba_podformuł = liczba_zdan + len(wyrazenia)

    return tabela_zdan + wyrazenia

#funkcja tworzy tablice wartosciowania formuły | przyjmuję: listę podformuł | zwraca: niepowartościowaną tabele wartosciowań |
def tworzenie_tablicy_wartosciowania_formuły(lista_podformuł):
    global ilosc_wierszy
    ilosc_wierszy = 2**liczba_zdan
    if ilosc_wierszy == 1:
        ilosc_wierszy = 2
    tablica_wartosciowania_formuły = [0] * ilosc_wierszy
    for x in range(len(tablica_wartosciowania_formuły)):
        tablica_wartosciowania_formuły[x] = [0] * liczba_podformuł
    potega = int((ilosc_wierszy) / 2)
    for i in range(0,liczba_zdan):
        x = 0
        liczba = 1
        for j in range(0,ilosc_wierszy):
            while x == potega:
                x = 0
                liczba = 1 - liczba
            x = x + 1
            tablica_wartosciowania_formuły[j][i] = liczba
        potega = int(potega / 2)
    return tablica_wartosciowania_formuły

#>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>

#funkcja wartościuję całą tablice wartosciowania formuły | przyjmuję: niepowartościowaną tabele wartosciowań, cała formułe w notacji Łukasiewicza | zwraca: powartościowaną tabele wartosciowań |
def wartosciowanie_tablicy(tablica,cała_formuła):

    # zmienne do obsługi funkcji wartościującej
    licznik = liczba_podformuł - liczba_zdan
    licznik_indeksów = liczba_zdan
    licznik_zdan = len(cała_formuła)
    # lista indeksów
    lista_indekow = []
    for x in range(0,len(cała_formuła)):
        lista_indekow.append(0)

    # funkcja wartosciująca
    while licznik > 0:
        for x in reversed(cała_formuła):
            licznik_zdan = licznik_zdan - 1
            if x.isupper():
                if x == "N":
                    if lista_indekow[licznik_zdan + 1] != 0:
                        podstawiana_wartosc = lista_indekow[licznik_zdan + 1]
                    else:
                        podstawiana_wartosc = lista_podformuł.index(cała_formuła[licznik_zdan + 1])

                    for y in range(0,ilosc_wierszy):
                        tablica[y][licznik_indeksów] = negacja(tablica[y][podstawiana_wartosc])

                    cała_formuła[licznik_zdan] = cała_formuła[licznik_zdan] + cała_formuła[licznik_zdan + 1]
                    del cała_formuła[licznik_zdan + 1]
                    lista_indekow[licznik_zdan] = licznik_indeksów
                    del lista_indekow[licznik_zdan + 1]
                    licznik_indeksów = licznik_indeksów + 1
                else:
                    if lista_indekow[licznik_zdan + 1] != 0:
                        podstawiana_wartosc1 = lista_indekow[licznik_zdan + 1]
                    else:
                        podstawiana_wartosc1 = lista_podformuł.index(cała_formuła[licznik_zdan + 1])
                    if lista_indekow[licznik_zdan + 2] != 0:
                        podstawiana_wartosc2 = lista_indekow[licznik_zdan + 2]
                    else:
                        podstawiana_wartosc2 = lista_podformuł.index(cała_formuła[licznik_zdan + 2])

                    if x == "A":
                        for y in range(0, ilosc_wierszy):
                            tablica[y][licznik_indeksów] = alternatywa(tablica[y][podstawiana_wartosc1],tablica[y][podstawiana_wartosc2])
                    elif x == "K":
                        for y in range(0, ilosc_wierszy):
                            tablica[y][licznik_indeksów] = koniunkcja(tablica[y][podstawiana_wartosc1],tablica[y][podstawiana_wartosc2])
                    elif x == "C":
                        for y in range(0, ilosc_wierszy):
                            tablica[y][licznik_indeksów] = implikacja(tablica[y][podstawiana_wartosc1],tablica[y][podstawiana_wartosc2])
                    elif x == "E":
                        for y in range(0, ilosc_wierszy):
                            tablica[y][licznik_indeksów] = rownowaznosc(tablica[y][podstawiana_wartosc1],tablica[y][podstawiana_wartosc2])

                    cała_formuła[licznik_zdan] = cała_formuła[licznik_zdan] + cała_formuła[licznik_zdan + 1] + cała_formuła[licznik_zdan + 2]
                    del cała_formuła[licznik_zdan + 1]
                    del cała_formuła[licznik_zdan + 1]
                    lista_indekow[licznik_zdan] = licznik_indeksów
                    del lista_indekow[licznik_zdan + 1]
                    del lista_indekow[licznik_zdan + 1]
                    licznik_indeksów = licznik_indeksów + 1
        licznik = licznik - 1

#funkcja wyświetla tablice wartosciowania formuły odpowiednio ją modelując | przyjmuję: tabele wartosciowań |
def rysowanie_tablicy(tablica):
    dlugosc_znakow = []
    print("| ",end="")
    ilosc_znakow_specialnych = 0
    z = 0
    for i in lista_podformuł:

        print(i,"|", end=" ")
        for x in i:
            if x == '∧' or x == '⇒' or x == '⇔' or x == '∨' or x == '¬':
                ilosc_znakow_specialnych = ilosc_znakow_specialnych + 1
                if ilosc_znakow_specialnych == 6:
                    z = z + 1
                    ilosc_znakow_specialnych = 0
        dlugosc_znakow.append(len(i) + z)
        z = 0
    print("")
    for i in range(len(tablica)):
        print("|",end="")
        x = 0
        for j in tablica[i]:
            print(" " * int(dlugosc_znakow[x] / 2), j," " * int(dlugosc_znakow[x] / 2), end="|")
            x  = x + 1
        print("")


# main
if __name__== "__main__":
    print("Wprowadź zdanie w notacji prefiksowej:")

    cała_formuła = list(input())
    cała_formuła2 = list(cała_formuła)

    print("Wprowadzona formuła: ")
    for item in cała_formuła:
        sys.stdout.write("%c" % item)
    print("")

    lista_podformuł = tworzenie_listy_podformul(cała_formuła)
    tablica_wartosciowania_formuły = tworzenie_tablicy_wartosciowania_formuły(lista_podformuł)
    wartosciowanie_tablicy(tablica_wartosciowania_formuły, cała_formuła2)

    print("Lista podformuł: ", lista_podformuł)
    print("Liczba podformuł: ", liczba_podformuł)
    print("Liczba zdan: ", liczba_zdan)
    rysowanie_tablicy(tablica_wartosciowania_formuły)
