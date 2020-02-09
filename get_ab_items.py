#!/usr/bin/python3

import httplib2
import urllib
import re

from html.parser import HTMLParser

### Ustawienia
# klasa div, w której są dane każdego poszczególnego ogłoszenia
advclass = "inner inzerat"
# tytuły ogłoszeń natrętnych/powtarzalnych (regexp)
blacklisted_leads = "^(walther GSP|PM63 RAK SEMI PM 63|.*[Uu]chwyt.*|[ŁłLl]adownica.*|[Kk]abura.*|[Kk]upi.*|[Ll]atarka.*)$"

### Początek kodu
class Adv:
	advtype = "" # Sprzedaż / Zakup
	url = ""
	imgUrl = ""
	imgAlt = ""
	lead = ""
	text = ""
	price = ""
	date = ""
	time = ""
	location = ""

	def __str__(self):
		# Omijamy ogłoszenia, które nie są sprzedażą, nie mają kompletnych danych lub są natrętne/powtarzalne
		if self.advtype != "Sprzedaż" or self.advtype == "" or re.match(re.compile(blacklisted_leads), self.lead) != None:
			return ""

		# Pozostałe ubieramy w odpowiedni HTML i zwracamy
		finalOutput  = '<div class="' + advclass + '">\n\t\t<a href="' + self.url + '" class="img"><img src="' + self.imgUrl + '" alt="' + self.imgAlt + '"></img></a>\n\t\t'
		finalOutput += '<div class="top"><h2><a href="' + self.url + '">' + self.lead + '</a></h2></div>\n\t\t<p>' + self.text + '</p>\n\t\t'
		finalOutput += '<ul class="cendat">\n\t\t\t<li class="cena"><strong>' + self.price + '</strong></li>\n\t\t\t<li class="datum">' + self.date + ' ' + self.time + '</li>\n\t\t\t'
		finalOutput += '<li class="lokalita">' + self.location + '</li>\n\t\t</ul>\n</div>\n'
		return finalOutput

AdvList = []

def printAdvs():
	for adv in AdvList:
		print(str(adv))

class MyHTMLParser(HTMLParser):
	append = 0
	subdivs = 0

	def append_data(self, tag, data):
		### przychodzące dane interesują nas tylko w trybie analizy konkretnego ogłoszenia
		if self.append != 1:
			return

		### jeśli otrzymaliśmy tylko tekst - poza tagiem - uzupełniamy odpowiednie atrybuty obiektu
		if tag == '':
			# jeśli mamy tylko białe znaki lub frazę spacja-myślnik-spacja - nic z nimi nie robimy - return
			if re.match(re.compile("^[\s]+$"), data) != None or data == " - ":
				return

			# w przeciwnym wypadku uzupełniamy atrybuty
			if AdvList[-1].lead == "":
				AdvList[-1].lead = data
			elif AdvList[-1].advtype == "":
				AdvList[-1].advtype = data
			elif AdvList[-1].text == "":
				AdvList[-1].text = data
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
					AdvList[-1].imgUrl = attr[1]
				elif attr[0] == "alt":
					AdvList[-1].imgAlt = attr[1]

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
				# oraz tworzy nowy obiekt reprezentujący ogłoszenie
				if advclass in attr:
					newAdv = Adv()
					AdvList.append(newAdv)
					self.append = 1
		# jeśli jesteśmy w trybie analizy ogłoszenia, to przekazujemy dane do interpretacji
		if self.append == 1:
			self.append_data(tag, attrs)
					
	def handle_endtag(self, tag):
		### jeśli zamykamy tag div, to jest ważne, czy to tag zamykający zakres ogłoszenia
		### jeśli tak, zerujemy stan append - wychodzimy poza ogłoszenie
		if tag == "div":
			if self.subdivs == 0:
				self.append = 0
			elif self.subdivs > 0:
				self.subdivs -= 1

	def handle_data(self, data):
		### jeśli jesteśmy w trybie analizy ogłoszenia, to przekazujemy dane do interpretacji
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
printAdvs()
# Wypisujemy stały footer strony
footer = open("inc/footer.html", "r")
print(footer.read())
