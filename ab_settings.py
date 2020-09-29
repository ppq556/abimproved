#!/usr/bin/python3
# This Python file uses the following encoding: utf-8

# ilość stron do pobrania z ArmyBazar (domyślnie 2 po 60 przedmiotów)
ab_numPages = 3

# tytuły/treść ogłoszeń natrętnych/powtarzalnych (regexp)
blacklisted_leads = "^(walther GSP|PM63 RAK SEMI PM 63|.*uchwyt.*|[łl]adownica.*|kabura.*|kupi.*|latarka.*|amunicj.*|kolb.*|.*magazyne.*|.*DOWOZIMY.*|.*łuski.*|.*AMUNICJA.*|Chwyt.*|S[lł]uchawki.*|.*ulary.*|.*pocisk.*|.*Umarex.*|.*CO2.*|.*magazyn.*k.*|.*bagnet.*|.*maxim.*|.*d[pt]28.*|.*Anschutz.*|pas.*|uchyt.*|Mosin.*|.*Torb[ay].*|Konwersj.*|Przyrząd.*|Zawiesz.*|.*[lł]adowni.*|.*Pouch.*|.*Chest.*rig.*|.*szyn.*RIS.*|.*Beryl.*szyn.*|.*ok[lł]adzi.*|.*Nosid.*|Mata.*|.*Range.*bag.*|.*kabur.*|.*kurtka.*|.*etui.*|.*szelki.*|.*plecak.*|.*iglica.*|.*bezpiecznik.*|.*pazur.*|Szafa.*|.*PBS-1.*|.*PBS1.*|.*Montaż.*|Cel.*|.*sprężyn.*|.*smarow.*|.*podchwy.*|.*Norinco.*|.*[zż]elow.*|.*wynajem.*|.*Beryl.*o[zże].*|.*kompensator.*|.*Maska.*|.*Przeziernik.*|.*xgrip.*|.*wiatr[oó]wka.*|.*czyszczeni.*|.*laser.*|.*Kolce.*|.*dwójn.*)$"
blacklisted_text = "(.*polarms.*|.*DOWOZIMY.*|.*amunicj.*|█.*)"
blacklisted_sellers = "(stefmar|magnum44)"

# minimalna cena oferty do rozważenia
minimal_price = 500

# wybrane województwa
selected_vovoidships = []
