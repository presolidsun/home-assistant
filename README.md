# ☀️ PRESolidsun – Home Assistant integrace

Vlastní integrace pro **Home Assistant**, která připojuje fotovoltaické elektrárny provozované přes portál PRESolidsun a zobrazuje jejich data jako entity přímo v HA.

[![GitLab](https://img.shields.io/badge/GitLab-PRESolidsunHA-orange?logo=gitlab)](https://gitlab.com/presolidsun/PRESolidsunHA)
[![HACS](https://img.shields.io/badge/HACS-custom-blue?logo=home-assistant)](https://hacs.xyz)
[![HA verze](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-41bdf5?logo=home-assistant)](https://www.home-assistant.io)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](LICENSE)

---

## Obsah

- [Co integrace umí](#-co-integrace-umí)
- [Požadavky](#-požadavky)
- [Instalace přes HACS](#-instalace-přes-hacs)
- [Ruční instalace](#-ruční-instalace)
- [Konfigurace](#-konfigurace)
- [Entity](#-entity)
- [Více FVE](#-více-fve)
- [Řešení problémů](#-řešení-problémů)

---

## Co integrace umí

| Funkce | Popis |
|--------|-------|
| Bezpečné přihlášení | OAuth token přihlašování přes API Solidsun |
| Energetické senzory | Dnešní, včerejší a celkové hodnoty výroby a spotřeby |
| Diagnostické senzory | Info o zařízení – IP, MAC, verze FW, DoD, poslední online |
| Více FVE | Každá elektrárna = samostatné zařízení v HA |

---

## Požadavky

- Home Assistant **2024.1 nebo novější**
- FVE u společnosti PRESolidsun s aktivním zařízením pro monitoring FVE
- Číslo OP a heslo (z vaší smlouvy nebo od správce)

---

## Instalace přes HACS

> **Doporučená metoda** – snadná aktualizace jedním kliknutím.

1. Otevřete **HACS** v postranním menu Home Assistantu
2. Klikněte na ⋮ → **Vlastní repozitáře**
3. Přidejte URL: `https://gitlab.com/presolidsun/PRESolidsunHA`  
   Kategorie: **Integrace**
4. Vyhledejte **PRESolidsun** a klikněte **Stáhnout**
5. **Restartujte** Home Assistant

---

## Ruční instalace

1. Stáhněte obsah složky `custom_components/presolidsun/` z tohoto repozitáře
2. Zkopírujte ji do `config/custom_components/presolidsun/` na vašem HA serveru
3. **Restartujte** Home Assistant

> Pokud složka `custom_components` neexistuje, vytvořte ji vedle souboru `configuration.yaml`.

---

## Konfigurace

Po restartu HA:

1. Přejděte do **Nastavení → Zařízení a služby**
2. Klikněte na **+ Přidat integraci**
3. Vyhledejte **PRESolidsun**
4. Vyplňte přihlašovací údaje:

| Pole | Popis |
|------|-------|
| **Číslo OP** | Číslo vaší obchodní případu (např. `OP-22-39017`), uvedeno na smlouvě |
| **Heslo** | Heslo přidělené správcem k portálu PRESolidsun |

5. Klikněte **Odeslat** – integrace ověří přihlášení a vytvoří entity

---

## Entity

### Energetické senzory

Pro každé ze tří období (**dnes / včera / celkem**) jsou dostupné tyto hodnoty:

| Entita | Popis | Jednotka |
|--------|-------|----------|
| Akumulace baterie | Energie uložená do baterie | kWh |
| Výroba z baterie | Energie dodaná z baterie | kWh |
| Odběr ze sítě | Spotřeba z distribuční sítě | kWh |
| Přetoky do sítě | Přebytky dodané do sítě | kWh |
| Spotřeba objektu | Celková spotřeba objektu | kWh |
| Výroba FVE | Vyrobená energie ze solárních panelů | kWh |

### 🔍 Diagnostické senzory

| Entita | Popis |
|--------|-------|
| Typ zařízení | Model zařízení (např. Sunberry) |
| MAC adresa | Hardware identifikátor zařízení |
| Lokální IP | IP adresa zařízení v lokální síti |
| Sériové číslo měniče | Identifikátor střídače |
| Verze softwaru | Aktuální SW verze |
| Verze firmwaru | Aktuální FW verze |
| DoD online | Hloubka vybití při připojení k síti (%) |
| DoD offline | Hloubka vybití při výpadku sítě (%) |
| Naposledy online | Čas posledního kontaktu zařízení s cloudem |

---

## Více FVE

Integrace podporuje **více fotovoltaických elektráren** najednou.  
Každou přidáte jako samostatnou instanci:

1. Přejděte do **Nastavení → Zařízení a služby → PRESolidsun**
2. Klikněte na **+ Přidat konfiguraci**
3. Zadejte číslo OP a heslo pro další FVE

Každá FVE se zobrazí jako **samostatné zařízení** se svými entitami.

---

## 🔧 Řešení problémů

| Problém | Řešení |
|---------|--------|
| Entity se nezobrazují | Restartujte HA a zkontrolujte logy |
| Neplatné přihlašovací údaje |
| Chybí české texty v UI | Proveďte tvrdý refresh prohlížeče (Ctrl+F5) |
| Zařízení se nepřipojí | Zkontrolujte připojení HA k internetu |

### Logy

V HA přejděte na **Nastavení → Systém → Logy** a vyhledejte `presolidsun`.

---

## 📄 Licence

MIT © PRESolidsun contributors
