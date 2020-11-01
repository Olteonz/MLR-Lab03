###############################################################################
#
# Python 3
#
# Wcięcia realizowane są czterema spacjami.
#
# Doczytanie bibliotek numpy i matplotlib:
# pip install numpy
# pip install matplotlib
#
# Uruchamianie skryptu:
# python dane.py
# albo wymuszając Pythona 3 gdy nie jest on domyślny:
# py -3 dane.py
#
###############################################################################
#
# Plik dane.csv zawiera dane zbierane na węźle ciepłowniczym przez 
# przedsiębiorstwo dostarczające ciepło do budynku (patrz opisy kolumn w pliku). 
# Niniejszy skrypt dokonuje podstawowej analizy tych danych.
#
# A.
# Wczytanie obserwacji dla wybranych zmiennych.
#
# B.
# Sprawdzenie podstawowych statystyk dla poszczególnych zmiennych.
# Wykreślenie histogramów.
#
# C.
# Identyfikacja zmiennych, w których występują potencjalnie błędne dane (obserwacje)
# lub braki danych. Naprawa danych.
#
# D.
# Obliczenie unormowanych korelacji pomiędzy poszczególnymi zmiennymi.
#
# E.
# Przeprowadzenie regresji liniowej dla wybranych zmiennych, wraz z wykresami.
#
###############################################################################
#
# Należy wykonać zadania na sumarycznie co najmniej 4 punkty 
#
###############################################################################



import csv
import numpy as np
import matplotlib.pyplot as plt
  
#######################
# A. Wczytanie danych #
#######################
  
przeplyw = []        # Przepływ wody przez węzeł
temp_zas = []         # Temperatura wody na wejściu do węzła
temp_pow = []        # Temperatura wody na wyjściu z węzła 
rozn_temp = []    # Różnica temperatur, wynikająca z oddanej energii w węźle
moc = []             # Moc oddana w węźle

plik = open('dane.csv', 'rt')
dane = csv.reader(plik, delimiter=',')
next(dane)                # Opuszczamy pierwszy wiersz
for obserwacja in dane:   # Iterujemy po poszczególnych obserwacjach.
    przeplyw.append(float(obserwacja[6]))
    temp_zas.append(float(obserwacja[7]))
    temp_pow.append(float(obserwacja[8]))
    rozn_temp.append(float(obserwacja[9]))
    moc.append(float(obserwacja[12]))
plik.close()

### ZADANIE (0.5p.) ###
# Dane w listach są ułożone od najnowszych do najstarszych.
# Odwrócić dane na listach tak, żeby były ułożone chronologicznie.
przeplyw.reverse()
temp_zas.reverse()
temp_pow.reverse()
rozn_temp.reverse()
moc.reverse()
### KONIEC ###
        
# Tworzymy słownik: kluczem jest nazwa zmiennej a wartością - zmienna
zmienne = {"temp_zas":temp_zas, "temp_pow":temp_pow, "rozn_temp":rozn_temp, "przeplyw":przeplyw, "moc":moc}


######################################
# B. Podstawowe statystyki i wykresy #
######################################
    
# Iterujemy po słowniku, wyświetlając statystyki dla poszczególnych zmiennych

zmienne_do_naprawienia = dict()
for nazwa,zmienna in zmienne.items():
    print()
    print("Zmienna:",nazwa)
    print("MIN:", min(zmienna))   
    print("MAX:", max(zmienna))
    print("ŚREDNIA:", np.mean(zmienna))
    print("MEDIANA:", np.median(zmienna))
    print("ZAKRES:", np.ptp(zmienna))
    print("ODCHYLENIE STANDARDOWE:", np.std(zmienna))
    print("WARIANCJA:", np.var(zmienna))
    print("PERCENTYL 90%:", np.percentile(zmienna,90) )
    print("HISTOGRAM:", np.histogram(zmienna))
    # Następne zadanie
    if max(zmienna) > np.median(zmienna)*20:
        zmienne_do_naprawienia[nazwa] = zmienna
        print("Do naprawienia ", nazwa)
    # Czcionka do wykresów, z polskimi znakami.
    plt.rc('font', family='Arial')

    # Wykres - histogram
    plt.hist(zmienna, 100)
    plt.title('Histogram dla: ' + nazwa)
    plt.xlabel('Przedział')
    plt.ylabel('Liczba obserwacji')
    plt.show()
    
############################################
# C. Analiza anomalii i czyszczenie danych # 
############################################

# Zidentyfikowaliśmy problem - "dziwne", znacząco za duże niektóre wartości dla zmiennych:
##zmienne_do_naprawienia = {"rozn_temp":rozn_temp, "przeplyw":przeplyw, "moc":moc}

### ZADANIE (1p.) ###
# Zrealizować automatyczne dodawanie "podejrzanych" zmiennych do słownika "zmienne_do_naprawienia",
# na podstawie analizy statystyk danej zmiennej.

#zrobione powyżej

### KONIEC ###


print()
print("CZYSZCZENIE DANYCH")

for nazwa,zmienna in zmienne_do_naprawienia.items():
    mediana_zmiennej = np.median(zmienna)
    for index,wartosc in enumerate(zmienna): # Iterujemy po wszystkich obserwacjach
        # Zakładamy (na podstawie analizy danych), że anomalia to wartość powyżej 10000
        # Dla następnego zadania zakładam że anomalia to wartości 10 krotnie większe od mediany zmiennej
        if (wartosc > mediana_zmiennej*10):
            print("Dla zmiennej {} pod indeksem {} znaleziono anomalię o wartości {}".format(nazwa, index, wartosc))
            # Wstawiamy medianę:
            mediana = np.median(zmienna)
            print("Naprawiam. Stara wartość: {}, nowa wartość: {}".format(zmienna[index], mediana))
            zmienna[index] = mediana

### ZADANIE (1p.) ###
# Znaleźć inną metodę wyznaczania progu anomalii w powyższej pętli tak, aby nie była to
# mediana_zmiennej*10
# "hardkodowana" wartość 10000, ale liczba wyznaczana indywidualnie dla każdej zmiennej.
### KONIEC ###

        
# Statystyki dla naprawionych zmiennych
for nazwa,zmienna in zmienne.items():
    print()
    print("Zmienna (naprawiona):",nazwa)
    print("MIN:", min(zmienna))   
    print("MAX:", max(zmienna))
    print("ŚREDNIA:", np.mean(zmienna))
    print("MEDIANA:", np.median(zmienna))
    print("ZAKRES:", np.ptp(zmienna))
    print("ODCHYLENIE STANDARDOWE:", np.std(zmienna))
    print("WARIANCJA:", np.var(zmienna))
    print("PERCENTYL 90%:", np.percentile(zmienna,90)) 
    print("HISTOGRAM:", np.histogram(zmienna))

    plt.hist(zmienna, 100)
    plt.title('Histogram dla: ' + nazwa)
    plt.xlabel('Przedział')
    plt.ylabel('Liczba obserwacji')
    plt.savefig(nazwa + '.pdf')
    plt.show() 
        
### ZADANIE (1p.) ###
# Zapisać powyższe statystyki i wykresy do plików PDF, osobnych dla poszczególnych zmiennych
# plt.savefig(nazwa + '.pdf')
# (można wykorzystać dowolny moduł/bibliotekę).

#zrobione powyzej plt.savefig(nazwa + '.pdf')

### KONIEC ###


#########################################
# D. Badanie korelacji między zmiennymi #
#########################################
       
print()      
print("KORELACJE")

# Piszemy funkcję, która zwróci korelację unormowaną między zestawami danych
def ncorrelate(a,b):
    '''Funkcja zwraca unormowaną wartość korelacji'''
    a = (a - np.mean(a)) / (np.std(a) * len(a))
    b = (b - np.mean(b)) / np.std(b)
    return np.correlate(a, b)[0]

### ZADANIE (0.5p.) ###
# Zademonstrować działanie funkcji ncorrelate() na przykładach:
# a. dwóch list zawierających dane silnie skorelowane
x_list = []
y_list = []
for x in range(20):
    x_list.append(x)
    y_list.append(x*2)
# b. dwóch list zawierające dane słabo skorelowane
import random
a_list = []
b_list = []
for x in range(20):
    a_list.append(random.randint(0,100))
    b_list.append(random.randint(0,100))
# Listy należy generować automatycznie
print("DEMONSTRACJA DZIALANIA ncorrelate()")
print("silna korelacja listy y i x: ", ncorrelate(x_list[:],y_list[:]))
print("slaba korelacja listy a i b: ", ncorrelate(a_list[:],b_list[:]))
### KONIEC ###


### ZADANIE (0.5p.) ###
# Poszukać funkcji z pakietu numpy, która wykonuje identyczne zadanie jak
# funkcja ncorrelate() i ją wykorzystać.
print("DEMONSTRACJA DZIALANIA numpy.corrcoef()")
print("silna korelacja listy y i x: ", np.corrcoef(x_list[:],y_list[:]))
print("slaba korelacja listy a i b: ", np.corrcoef(a_list[:],b_list[:]))
### KONIEC ###


# Badamy korelacje między wszystkimi (różnymi od siebie) zmiennymi
lista_korelacji = []
for nazwa1,zmienna1 in zmienne.items():
    for nazwa2,zmienna2 in zmienne.items():
        if nazwa1 != nazwa2:
            print("Korelacja między", nazwa1,"a", nazwa2,"wynosi:", end=" ")
            print(ncorrelate(zmienna1,zmienna2))
            #lista_korelacji.append([zmienna1, zmienna2, ncorrelate(zmienna1,zmienna2)])
            #Wydaje mi się że w zadaniu lista powinna mieć postać [[nazwa1, nazwa2, korelacja[, [..., ..., ...], ... ] bo nie widzę sensu w zapisywaniu wszystkich zmiennych na nowo
            lista_korelacji.append([nazwa1, nazwa2, ncorrelate(zmienna1, zmienna2)])

### ZADANIE (1p.) ###
# Zebrać powyższe wyniki korelacji w dwuwymiarowej liście postaci:
# [[zmienna1, zmienna2, korelacja], [..., ..., ...], ... ] tak, aby elementy tej listy
# były posortowane malejąco wg. wartości korelacji.
sorted_lista_korelacji = sorted(lista_korelacji, key=lambda x: x[2], reverse=True)
print("Posortowana lista korelacji:", sorted_lista_korelacji)
### KONIEC ###
            
            
# Przykładowe wykresy

# 1. Zmienne z dużą korelacją dodatnią: moc, przeplyw

# Wykres liniowy
plt.plot(range(len(moc)), moc, "x")
plt.plot(range(len(przeplyw)), przeplyw, "+")
plt.title("Duża korelacja dodatnia")
plt.ylabel('x: moc; +: przeplyw')
plt.xlabel('Numer obserwacji')
plt.show()

# Dla lepszej ilustracji: wycinek danych.
# Zmienna moc przemnożnona przez 10, aby lepiej było widać korelację.
plt.plot(range(len(moc[1000:1100])), [i*10 for i in moc[1000:1100]])
plt.plot(range(len(przeplyw[1000:1100])), przeplyw[1000:1100])
plt.title("Duża korelacja dodatnia. Zmienna moc przemnożona przez 10.")
plt.ylabel('dół: moc; góra: przeplyw')
plt.xlabel('Numer obserwacji')
plt.show()

# Wykres zależności przeplyw od moc
plt.plot(moc, przeplyw, '.')
plt.title("Duża korelacja dodatnia")
plt.xlabel('moc')
plt.ylabel('przeplyw')
plt.show()


# 2. Zmienne skorelowane ujemnie: rozn_temp, temp_pow

# Wykres liniowy
plt.plot(range(len(rozn_temp)), rozn_temp, "x")
plt.plot(range(len(temp_pow)), temp_pow, "+")
plt.title("Średnia korelacja ujemna")
plt.ylabel('x: rozn_temp; +: temp_pow')
plt.xlabel('Numer obserwacji')
plt.show()

# Dla lepszej ilustracji: wycinek danych
plt.plot(range(len(rozn_temp[1000:1100])), rozn_temp[1000:1100])
plt.plot(range(len(temp_pow[1000:1100])), temp_pow[1000:1100])
plt.title("Średnia korelacja ujemna.")
plt.ylabel('dol: rozn_temp; gora: temp_pow')
plt.xlabel('Numer obserwacji')
plt.show()

# Wykres zależności temp_pow od rozn_temp
plt.plot(rozn_temp, temp_pow, '.')
plt.title("Średnia korelacja ujemna.")
plt.xlabel('rozn_temp')
plt.ylabel('temp_pow')
plt.show()


#######################
# E. Regresja liniowa #
#######################

# Analiza przeprowadzona tylko dla jednej zmiennej, temp_zas

print()
print("REGRESJA LINIOWA")
# Wybieramy zmienną temp_zas w funkcji numeru obserwacji
x = range(len(temp_zas))
y = temp_zas
# Liczymy współczynniki regresji - prostej
a,b = np.polyfit(x,y,1)  # Wielomian 1 rzędu - prosta
print("Wzór prostej: y(x) =",a,"* x +",b)
# Wyliczamy punkty prostej otrzymanej w wyniku regresji
yreg =  [a*i + b for i in x] 
# Wykresy
plt.plot(x,y)
plt.plot(x,yreg)
plt.title("Regresja liniowa dla całosci danych zmiennej temp_zas")
plt.xlabel('Numer obserwacji')
plt.ylabel('temp_zas')
plt.show()


print()
print("REGRESJA WIELOMIANOWA")
# Wybieramy zmienną temp_zas w funkcji numeru obserwacji
x = range(len(temp_zas))
y = temp_zas
# Liczymy współczynniki regresji - prostej
a,b,c = np.polyfit(x,y,2)  # Wielomian 1 rzędu - prosta
print("Wzór krzywej: y(x) =",a,"* x *x  +",b,"* x +",c)
# Wyliczamy punkty prostej otrzymanej w wyniku regresji
yreg =  [a*i*i + b*i + c for i in x] 
# Wykresy
plt.plot(x,y)
plt.plot(x,yreg)
plt.title("Regresja wielomianowa dla całosci danych zmiennej temp_zas")
plt.xlabel('Numer obserwacji')
plt.ylabel('temp_zas')
plt.show()




### ZADANIE (1.5p.) ###
# Z wykresu widać, że regresja liniowa dla całości zmiennej temp_zas słabo się sprawdza.
# Wynika to z tego, że inaczej dane rozkładają się w róznych porach roku.
# Należy więc podzielić dane na kilka podzakresów i regresję wykonać osobno
# dla każdego z podzakresu. Narysować odpowiedni wykres.

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))
n = len(temp_zas)/4
chunked_list = chunks(temp_zas, int(n))
#del chunked_list[-1] Z jakiegos powodu kompilator nie pozwala mi usunac ostatniego elementu listy, wiec lista zawiera 4 elementy oraz 1 pusty element
chunk_nr = 1
for chunk in chunked_list:
    print("REGRESJA LINIOWA NA PORY ROKU")
    # Wybieramy zmienną temp_zas w funkcji numeru obserwacji
    x = range(len(chunk))
    y = chunk
    # Liczymy współczynniki regresji - prostej
    a, b = np.polyfit(x, y, 1)  # Wielomian 1 rzędu - prosta
    print("Wzór prostej: y(x) =", a, "* x +", b)
    # Wyliczamy punkty prostej otrzymanej w wyniku regresji
    yreg = [a * i + b for i in x]
    # Wykresy
    plt.plot(x, y)
    plt.plot(x, yreg)
    plt.title("Regresja liniowa dla całosci danych zmiennej temp_zas chunk nr: "+str(chunk_nr))
    plt.xlabel('Numer obserwacji')
    plt.ylabel('temp_zas')
    plt.show()
    chunk_nr += 1
### KONIEC ###



# Regresja liniowa dla zmiennych z dużą korelacją dodatnią: moc, przeplyw
a,b = np.polyfit(moc,przeplyw,1)  # Wielomian 1 rzędu - prosta
yreg =  [a*i + b for i in moc] 
# Wykresy
plt.plot(moc,przeplyw,".")
plt.plot(moc,yreg)
plt.title("Regresja liniowa")
plt.xlabel('moc')
plt.ylabel('przeplyw')
plt.show()


# Regresja liniowa dla zmiennych ze słabą korelacją ujemną: rozn_temp, temp_pow
a,b = np.polyfit(rozn_temp,temp_pow,1)  # Wielomian 1 rzędu - prosta
yreg =  [a*i + b for i in rozn_temp] 
# Wykresy
plt.plot(rozn_temp,temp_pow,".")
plt.plot(rozn_temp,yreg)
plt.title("Regresja liniowa")
plt.xlabel('rozn_temp')
plt.ylabel('temp_pow')
plt.show()

# Predykcja danych z losowej listy
rozn_temp = []	
import random
for i in range(20):
	rozn_temp.append(random.randint(0,100))
	
# Wyliczenie wyników na podstawie regresji i zapis do listy
temp_pow = [[i, a*i+b] for i in rozn_temp]
print("Wyniki predykcji temp_pow(rozn_temp):",temp_pow)

### ZADANIE (0.5p.) ###
# Zapisać wyniki powyższej predykcji do pliku predykcja-rozn_temp-temp_pow.json
import json
with open('predykcja-rozn_temp-temp_pow.json', 'w') as outfile:
    json.dump(temp_pow, outfile)
### KONIEC ###

#Aleksander Mielczarek 2020