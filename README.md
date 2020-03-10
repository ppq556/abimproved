# Skrypt do wygodniejszego przeglądania ArmyBazar by ppq556 / avltree

## Motywacja
- usunięcie reklam i ogłoszeń sponsorowanych - zrobione
- usunięcie ofert kupna - zrobione
- usunięcie ofert nachalnych i powtarzalnych (np. GSP / RAK od Atena Guns) - zrobione

## Instrukcja

### Wersja z dockerem

#### Wymagania
- [Docker](https://docs.docker.com/install/)

#### Użycie
```shell script
docker build . -t abimproved           # tylko za pierwszym razem
docker run abimproved > armybazar.html
```

### Wersja standalone

#### Wymagania
- python3 (apt install python3)
- python3-httplib2 (apt install python3-httplib2 )

#### Użycie
```shell script
python3 abimproved.py > armybazar.html
firefox armybazar.html
```

### Parametry
``` -v ``` - (OPCJONALNY) oddzielona przecinkami lista województw, z których ogłoszenia zostaną wyświetlone. Jeżeli nie jest podany, wyświetlają się ogłoszenia z wszystkich województw.