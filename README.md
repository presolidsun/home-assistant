# PREsolidsun – Home Assistant integrace

Vlastní integrace pro **Home Assistant**, která propojuje fotovoltaické elektrárny vybavené monitorovacím zařízením PREsolidsun. Data jsou načítána přímo z cloudu a zobrazena jako entity v Home Assistantu.

[![GitHub](https://img.shields.io/badge/GitHub-PREsolidsun%2Fhome--assistant-black?logo=github)](https://github.com/PREsolidsun/home-assistant)
[![HACS](https://img.shields.io/badge/HACS-custom-blue?logo=home-assistant)](https://hacs.xyz)
[![HA verze](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-41bdf5?logo=home-assistant)](https://www.home-assistant.io)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](LICENSE)

---

## Co integrace umí

| Funkce | Popis |
|--------|-------|
| Bezpečné přihlášení | Přihlášení pomocí čísla OP a hesla přes API PREsolidsun |
| Okamžité hodnoty | Aktuální výkon FVE v reálném čase (kW) |
| Denní přehled | Dnešní a včerejší hodnoty výroby a spotřeby |
| Celkové součty | Kumulované hodnoty od spuštění FVE |
| Diagnostické senzory | Info o zařízení – IP, MAC, verze FW/SW, DoD, poslední online |
| Více FVE | Každá elektrárna = samostatné zařízení v HA |
| Automatická aktualizace | Data se obnovují každé 2,5 minuty |

---

## Požadavky

- Home Assistant **2024.1 nebo novější**
- FVE vybavená monitorovacím zařízením PREsolidsun
- Přihlašovací údaje: **číslo OP** a **heslo**

> Přihlašovací údaje najdete ve smlouvě s PREsolidsun. Pokud je nemáte, kontaktujte podporu na [info@solidsun.cz](mailto:info@solidsun.cz).

---

## Instalace přes HACS

> **Doporučená metoda** – snadná aktualizace jedním kliknutím.

1. Otevřete **HACS** v postranním menu Home Assistantu
2. Klikněte na ⋮ → **Vlastní repozitáře**
3. Přidejte URL: `https://github.com/PREsolidsun/home-assistant` a kategorii **Integrace**
4. Vyhledejte **PREsolidsun** a klikněte **Stáhnout**
5. **Restartujte** Home Assistant

---

## Ruční instalace

1. Stáhněte obsah složky `custom_components/PREsolidsun/` z tohoto repozitáře
2. Zkopírujte ji do `config/custom_components/PREsolidsun/` na vašem HA serveru
3. **Restartujte** Home Assistant

> Pokud složka `custom_components` neexistuje, vytvořte ji vedle souboru `configuration.yaml`.

---

## Konfigurace

Po restartu HA:

1. Přejděte do **Nastavení → Zařízení a služby**
2. Klikněte na **+ Přidat integraci**
3. Vyhledejte **PREsolidsun**
4. Vyplňte přihlašovací údaje:

| Pole | Popis |
|------|-------|
| **Číslo OP** | Číslo vaší smlouvy (např. `OP-22-39017`) |
| **Heslo** | Heslo k vašemu účtu PREsolidsun |

5. Klikněte **Odeslat** – integrace ověří přihlášení a automaticky vytvoří všechny entity

---

## Entity

Integrace vytváří entity pojmenované ve formátu `sensor.solidsun_XXXXX_skupina_hodnota`, kde `XXXXX` je číslo vaší OP.

### Energetické senzory (kWh)

Dostupné pro čtyři časová období:

| Skupina | Popis |
|---------|-------|
| **Dnes** | Hodnoty akumulované od začátku dnešního dne |
| **Včera** | Hodnoty za celý předchozí den |
| **Celkem** | Kumulativní součty od spuštění FVE |
| **Nyní** | Okamžitý výkon v reálném čase (kW) |

V každé skupině jsou tyto hodnoty:

| Hodnota | Popis |
|---------|-------|
| Výroba FVE | Energie vyrobená solárními panely |
| Spotřeba objektu | Celková spotřeba objektu |
| Akumulace baterie | Energie uložená do baterie |
| Výroba z baterie | Energie dodaná z baterie |
| Odběr ze sítě | Spotřeba z distribuční sítě |
| Přetoky do sítě | Přebytky dodané do distribuční sítě |

### Diagnostické senzory

| Entita | Popis |
|--------|-------|
| Typ zařízení | Model monitorovacího zařízení |
| MAC adresa | Hardware identifikátor zařízení |
| Lokální IP | IP adresa zařízení v lokální síti |
| Sériové číslo měniče | Identifikátor střídače |
| Verze softwaru | Aktuální verze SW |
| Verze firmwaru | Aktuální verze FW |
| DoD online | Hloubka vybití baterie při připojení k síti (%) |
| DoD offline | Hloubka vybití baterie při výpadku sítě (%) |
| Naposledy online | Čas posledního kontaktu zařízení s cloudem |

---

## Více FVE

Integrace podporuje **více fotovoltaických elektráren** najednou. Každou přidáte jako samostatnou instanci:

1. Přejděte do **Nastavení → Zařízení a služby → PREsolidsun**
2. Klikněte na **+ Přidat konfiguraci**
3. Zadejte číslo OP a heslo pro další FVE

Každá FVE se zobrazí jako **samostatné zařízení** se svými entitami.

---

## Řešení problémů

| Problém | Řešení |
|---------|--------|
| Entity se nezobrazují | Restartujte HA a zkontrolujte logy |
| Neplatné přihlašovací údaje | Ověřte číslo OP a heslo; kontaktujte [info@solidsun.cz](mailto:info@solidsun.cz) |
| Chybí české texty v UI | Proveďte tvrdý refresh prohlížeče (Ctrl+F5) |
| Zařízení se nepřipojí | Zkontrolujte připojení HA k internetu |

V HA přejděte na **Nastavení → Systém → Logy** a vyhledejte `PREsolidsun`.

---

## 📄 Licence

MIT © PREsolidsun
