"""Constants for the Solidsun integration."""

DOMAIN = "presolidsun"

CONF_CASE_NUMBER = "case_number"
CONF_PASSWORD = "password"

API_BASE = "https://servis.solidsun.cz/api"
API_LOGIN = f"{API_BASE}/auth/client-login"
API_DAILY_SUM = f"{API_BASE}/clients/devices/daily-sum"
API_TOTAL_SUM = f"{API_BASE}/clients/devices/total-sum"
API_ACTIVE = f"{API_BASE}/clients/devices/active"
API_LAST_LOG = f"{API_BASE}/clients/devices/last-log"

UPDATE_INTERVAL_MINUTES = 2.5
TOTAL_SUM_INTERVAL_HOURS = 6

# Skupiny senzorů. "instant" = okamžitá hodnota (výkon kW), jinak kumulovaná energie (kWh).
SENSOR_GROUPS = {
    "today": {"label": "Dnešní den", "slug": "dnes", "instant": False},
    "yesterday": {"label": "Včerejší den", "slug": "vcera", "instant": False},
    "total": {"label": "Celkem", "slug": "celkem", "instant": False},
    "now": {"label": "Nyní", "slug": "nyni", "instant": True},
}

SENSOR_KEYS = {
    "battery_accumulation": {
        "name": "Akumulace baterie",
        "icon": "mdi:battery-charging",
        "slug": "baterie_akumulace",
    },
    "battery_production": {
        "name": "Výroba z baterie",
        "icon": "mdi:battery-arrow-up",
        "slug": "baterie_vyroba",
    },
    "distribution_delivery": {
        "name": "Odběr ze sítě",
        "icon": "mdi:transmission-tower-import",
        "slug": "distribuce_nakup",
    },
    "distribution_overflow": {
        "name": "Přetoky do sítě",
        "icon": "mdi:transmission-tower-export",
        "slug": "distribuce_pretok",
    },
    "object_consumption": {
        "name": "Spotřeba objektu",
        "icon": "mdi:home-lightning-bolt",
        "slug": "objekt_spotreba",
    },
    "sun_production": {
        "name": "Výroba FVE",
        "icon": "mdi:solar-panel",
        "slug": "slunce_vyroba",
    },
}

DEVICE_INFO_KEYS = {
    "type_label": {"name": "Typ zařízení", "icon": "mdi:chip"},
    "mac": {"name": "MAC adresa", "icon": "mdi:network"},
    "local_ip": {"name": "Lokální IP", "icon": "mdi:ip-network"},
    "serial_number_inverter": {"name": "Sériové číslo měniče", "icon": "mdi:barcode"},
    "sw_version": {"name": "Verze softwaru", "icon": "mdi:information-outline"},
    "version": {"name": "Verze firmwaru", "icon": "mdi:information-outline"},
    "dod_online": {"name": "DoD online", "icon": "mdi:battery-70", "unit": "%"},
    "dod_offline": {"name": "DoD offline", "icon": "mdi:battery-30", "unit": "%"},
    "last_online_at": {"name": "Naposledy online", "icon": "mdi:clock-check-outline"},
}
