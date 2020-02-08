#!/usr/bin/python3

import httplib2
import urllib

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    page = ""
    append = 0
    subdivs = 0
    advclass = "inner inzerat"

    def append_data(self, tag, data):
        ### tylko tekst - poza tagiem - dopisujemy i to koniec
        if tag == '':
            self.page += data
            return

        ### dane w tagu - trzeba interpretować
        # otwieramy tag i dopisujemy
        self.page += '<' + tag

        # jeśli to koniec danych, to od razu zamykamy i kończymy
        if tag[0] == '/' or len(data) == 0:
            self.page += '>'
            return

        # iteracja po strukturze data - są to argumenty tagu
        i = 0
        for x in data:
            # poniższe rodzaje opcji mają argumenty - trzeba je wyłuskać
            if x[0] in { "class", "href", "src", "alt" }:
                self.page += ' ' + x[0] + '="' + x[1] + '"'
            # a w przypadku innych po prostu dopisać
            else:
                print("debug;" + x[0])
                self.page += ' ' + x[0]
            # wreszcie, jeśli jest to koniec dla tego tagu - zamykamy go
            if i == len(data) - 1:
                self.page += '>'
            i += 1

    def handle_starttag(self, tag, attrs):
        ### każdy otwarty tag analizujemy
        # jeśli tagiem jest div, to analizujemy szczególnie mocno
        if tag == "div":
            # jeśli jesteśmy w zakresie diva z ogłoszeniem, to uznajemy to
            # za potrzebny, nowy div głębiej w strukturze HTML i zwiększamy licznik
            if self.append == 1:
                self.subdivs += 1
            for attr in attrs:
                # jeśli div należy do odpowiedniej klasy, to wchodzimy w tryb ogłoszenia - ustawiamy zmienną
                if self.advclass in attr:
                    self.append = 1
        # jeśli jesteśmy w trybie analizy ogłoszenia, to dopisujemy dane do finalnego outputu
        if self.append == 1:
            self.append_data(tag, attrs)
                    
    def handle_endtag(self, tag):
        ### jeśli jesteśmy w zakresie ogłoszenia, to dopisujemy zamknięcie do danych wynikowych
        if self.append == 1:
            self.append_data('/' + tag, '')
        ### jeśli zamykamy tag div, to jest ważne, czy to tag zamykający zakres ogłoszenia
        ### jeśli tak, zerujemy stan append - wychodzimy poza ogłoszenie
        if tag == "div":
            if self.subdivs == 0:
                self.append = 0
            elif self.subdivs > 0:
                self.subdivs -= 1

    def handle_data(self, data):
        ### jeśli jesteśmy w zakresie ogłoszenia, to dopisujemy zamknięcie do danych wynikowych
        if self.append == 1:
            self.append_data('', data)

# Instancjalizacja klasy analizatora HTTP
http = httplib2.Http()

# Parametry żądania - 60 ogłoszeń na stronie; URL do ArmyBazar
body = {'nastranku': '60'}
content = http.request("http://bron-i-amunicja.armybazar.eu/pl/", method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body))[1]

# Wywołujemy parse'owanie
parser = MyHTMLParser()
parser.feed(content.decode())

# Wypisujemy stały header strony
header = open("inc/header.html", "r")
print(header.read())
# Wypisujemy treść ogłoszeń w HTML
print(parser.page)
# Wypisujemy stały footer strony
footer = open("inc/footer.html", "r")
print(footer.read())
