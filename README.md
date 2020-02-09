# Super duper script by ppqa

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
docker build . -t get_ab_items           # tylko za pierwszym razem
docker run get_ab_items > armybazar.html
```

### Wersja standalone

#### Wymagania
- python3 (apt install python3)
- python3-httplib2 (apt install python3-httplib2 )

#### Użycie
```shell script
python3 get_ab_items.py > armybazar.html
firefox armybazar.html
```
