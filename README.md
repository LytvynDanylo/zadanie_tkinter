# Fyzikálne vzorce

Desktopová Python aplikácia vytvorená pre zadanie 2.

## Funkcie

- Generuje 60 náhodných teplôt v stupňoch Celzia.
- Zoraďuje pole a vypočítava priemer, minimum a maximum.
- Prevádza teplotu podľa vzorca `°F = °C × 1.8 + 32`.
- Zobrazuje pôvodné aj vypočítané hodnoty v jednom grafe.
- Umožňuje vygenerovať nových 60 náhodných hodnôt tlačidlom.
- Vypočítava tlak podľa vzorca `p = F / S`, kde `F` je sila v newtonoch a `S` je plocha v metroch štvorcových.
- Prepína medzi prevodom teploty a výpočtom tlaku; tabuľka aj graf zobrazujú pôvodné a vypočítané hodnoty podľa zvoleného vzorca.
- Obsahuje vstupné pole, tlačidlo a popis výsledku.

## Spustenie zo zdrojového kódu

```bat
py -m pip install -r requirements.txt
py main.py
```

## Zostavenie EXE

```bat
build_exe.bat
```

Výsledný súbor sa vytvorí v priečinku `dist\Fyzikalne_vzorce.exe`.
