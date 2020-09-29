#!/usr/bin/python3
# This Python file uses the following encoding: utf-8

import argparse
import httplib2
import urllib
import re
from past.builtins import execfile
from html.parser import HTMLParser

parser = argparse.ArgumentParser()

### Ustawienia
# klasa div, w której są dane każdego poszczególnego ogłoszenia
advclass = "inner inzerat"
# wyrażenie regularne do pobierania nazwy i URL-a sprzedawcy
sellerNameRegExp = ".*Ogłoszeniodawca: (<a href.*\">)?([a-zA-Z0-9_-]*)(</a>)?"
sellerURLRegExp  = ".*Ogłoszeniodawca: <a href=\"(.*)\">.*"
# lista wszystkich województw
available_vovoidships = ["Dolnośląskie", "Kujawsko-Pomorskie", "Lubelskie", "Lubuskie", "Łódzkie", "Małopolskie", "Mazowieckie", "Opolskie", "Podkarpackie", "Podlaskie", "Pomorskie", "Śląskie", "Świętokrzyskie", "Warmińsko-Mazurskie", "Wielkopolskie", "Zachodniopomorskie"]

# wartości do konfiguracji przez użytkownika (w osobnym pliku)
execfile('ab_settings.py')

### Początek kodu
class Adv:
	def __init__ (self):
		self.advtype = "" # Sprzedaż / Zakup
		self.sellerName = ""
		self.sellerURL = ""
		self.url = ""
		self.imgPrevUrl = ""
		self.imgPrevAlt = ""
		self.lead = ""
		self.text = ""
		self.price = ""
		self.date = ""
		self.time = ""
		self.location = ""

	def getSellerName(self):
		if self.url == "":
			return

		# Dodatkowe połączenie do ArmyBazar (niestety) i pobranie pełnej strony przedmiotu
		httpSeller = httplib2.Http()
		sellerContent = httpSeller.request(self.url, method="GET")[1]

		# Regexp, wyodrębniający nazwę sprzedawcy
		sellerName_search = re.search(sellerNameRegExp, sellerContent.decode())

		if sellerName_search:
			self.sellerName = sellerName_search.group(2).strip()

			# Jeśli poprzedni regexp pobrał nazwę sprzedawcy, to wywołanie kolejnego, do URL-a (nie zawsze istnieje)
			sellerURL_search = re.search(sellerURLRegExp, sellerContent.decode())

			if sellerURL_search:
				self.sellerURL = sellerURL_search.group(1).strip()

	def __str__(self):
		# Omijamy ogłoszenia, które nie są sprzedażą, nie mają kompletnych danych lub są natrętne/powtarzalne
		if self.advtype != "Sprzedaż" or not self.location in selected_vovoidships or re.match(re.compile(blacklisted_leads, flags=re.IGNORECASE), self.lead) != None or re.match(re.compile(blacklisted_text, flags=re.IGNORECASE), self.text) != None or (self.price != "Do uzgodnienia" and float(self.price.split()[0]) < minimal_price):
			return ""

		# Pobieranie nazwy sprzedawcy - w tym miejscu (po podstawowych filtrach) ze względów wydajnościowych
		# Niestety każde ogłoszenie oznacza jedno pełne dodatkowe pobranie strony z ArmyBazar
		self.getSellerName()

		# Domyślnie pokazywany jest tylko nick sprzedawcy
		sellerString = "[" + self.sellerName + "]"

		# Natomiast jeśli obiekt ma również niepustą wartość sellerURL to ubieramy ją w HTML razem z nazwą
		if self.sellerURL != "":
			sellerString = "<a href=\"" + self.sellerURL + "\">[" + self.sellerName + "]</a>"

		# Dodatkowe filtrowanie po sprzedawcach
		if re.match(re.compile(blacklisted_sellers, flags=re.IGNORECASE), self.sellerName) != None:
			return ""

		# Pozostałe ubieramy w odpowiedni HTML i zwracamy
		finalOutput  = '<div class="' + advclass + '">\n\t\t<a href="' + self.url + '" class="img"><img src="' + self.imgPrevUrl + '" alt="' + self.imgPrevAlt + '"></img></a>\n\t\t'
		finalOutput += '<div class="top"><h2><a href="' + self.url + '">' + self.lead + '</a></h2></div>\n\t\t<p>' + self.text + '</p>\n\t\t'
		finalOutput += '<ul class="cendat">\n\t\t\t<li class="cena"><strong>' + self.price + '</strong></li>\n\t\t\t<li class="datum">' + self.date + ' ' + self.time + '</li>\n\t\t\t'
		finalOutput += '<li class="lokalita">' + self.location + '</li>' + sellerString + '\n\t\t</ul>\n</div>\n'
		return finalOutput

# Zmienna przechowująca wszystkie obiekty ogłoszeń, inicjalnie pusta
AdvList = []

def printAdvs():
	for adv in AdvList:
		print(str(adv))

class ABHTMLParser(HTMLParser):
	inside_adv = 0
	subdivs = 0

	def process_data(self, tag, data):
		### przychodzące dane interesują nas tylko w trybie analizy konkretnego ogłoszenia
		if self.inside_adv != 1:
			return

		### jeśli otrzymaliśmy tylko tekst - poza tagiem - uzupełniamy odpowiednie atrybuty obiektu
		if tag == '':
			# jeśli mamy tylko białe znaki lub frazę spacja-myślnik-spacja - nic z nimi nie robimy - return
			if re.match(re.compile("^[\s]+$"), data) != None or data == " - ":
				return

			# w przeciwnym wypadku uzupełniamy atrybuty
			if AdvList[-1].lead == "":
				AdvList[-1].lead = data.strip()
			elif AdvList[-1].advtype == "":
				AdvList[-1].advtype = data
			elif AdvList[-1].text == "":
				AdvList[-1].text = data.strip()
			elif AdvList[-1].price == "":
				AdvList[-1].price = data
			elif AdvList[-1].date == "":
				AdvList[-1].date = data
			elif AdvList[-1].time == "":
				AdvList[-1].time = data
			elif AdvList[-1].location == "":
				AdvList[-1].location = data

			return

		### jeśli otrzymaliśmy tag a/img to musimy go zinterpretować
		# iteracja po strukturze data - są to argumenty tagu
		for attr in data:
			# poniższe rodzaje opcji mają argumenty - trzeba je wyłuskać
			if tag == "a":
				if attr[0] == "href":
					AdvList[-1].url = attr[1]
			if tag == "img":
				if attr[0] == "src":
					AdvList[-1].imgPrevUrl = attr[1]
				elif attr[0] == "alt":
					AdvList[-1].imgPrevAlt = attr[1]

	def handle_starttag(self, tag, attrs):
		### każdy otwarty tag analizujemy
		# jeśli tagiem jest div, to analizujemy szczególnie mocno
		if tag == "div":
			# jeśli już jesteśmy w zakresie diva z ogłoszeniem, a pojawia się kolejny div,
			# to uznajemy go za potrzebny, głębiej w strukturze HTML i zwiększamy licznik
			if self.inside_adv == 1:
				self.subdivs += 1
			for attr in attrs:
				# jeśli nowy div należy do odpowiedniej klasy, to wchodzimy w tryb ogłoszenia
				# ustawiamy zmienną oraz tworzymy nowy obiekt reprezentujący ogłoszenie
				if advclass in attr:
					newAdv = Adv()
					AdvList.append(newAdv)
					self.inside_adv = 1
		### a generalnie przekazujemy dane do interpretacji
		self.process_data(tag, attrs)
					
	def handle_endtag(self, tag):
		### jeśli zamykamy tag div, to jest ważne, czy to tag zamykający zakres ogłoszenia
		### jeśli tak, zerujemy stan inside_adv - wychodzimy z trybu analizy konkretnego ogłoszenia
		if tag == "div":
			if self.subdivs == 0:
				self.inside_adv = 0
			elif self.subdivs > 0:
				self.subdivs -= 1

	def handle_data(self, data):
		### przekazujemy dane do interpretacji
		self.process_data('', data)

def parseVovoidship(argList):
	if argList.vovoidship:
		vovoidshipArgSplit = argList.vovoidship.split(',')
		for v in vovoidshipArgSplit:
			if v in available_vovoidships:
				selected_vovoidships.append(v)
	if len(selected_vovoidships) < 1:
		for v in available_vovoidships:
			selected_vovoidships.append(v)
		
	
# wczytanie argumentów
parser.add_argument("-v", "--vovoidship", help="wpisz województwa z których ogłoszenia cię interesują (oddzielone przecinkiem)", type=str)

args = parser.parse_args()
parseVovoidship(args)

# parsowanie argumentu województw

# Instancjalizacja klasy analizatora HTTP
http = httplib2.Http()

# Parametry żądania - 60 ogłoszeń na stronie; URL do ArmyBazar
body = {'nastranku': '60'}
# Pobranie contentu z ArmyBazar - domyślnie dwa requesty (dwie strony po 60 przedmiotów), aby zwiększyć liczbę treści, którą można filtrować
# Liczba stron jest konfigurowalna w pliku ustawień
content = http.request("http://bron-i-amunicja.armybazar.eu/pl/", method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body))[1]
page = 2
while page <= ab_numPages:
	content += http.request("http://bron-i-amunicja.armybazar.eu/pl/strona/" + str(page) + "/", method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body))[1]
	page += 1

# Wywołujemy parse'owanie
parser = ABHTMLParser()
parser.feed(content.decode())

# Wypisujemy stały header strony
header = open("inc/header.html", "r")
print(header.read())
# Wypisujemy treść ogłoszeń w HTML
printAdvs()
# Wypisujemy stały footer strony
footer = open("inc/footer.html", "r")
print(footer.read())
