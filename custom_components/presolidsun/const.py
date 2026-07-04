"""Constants for the Solidsun integration."""

DOMAIN = "presolidsun"

CONF_CASE_NUMBER = "case_number"
CONF_PASSWORD = "password"

API_BASE = "https://servis.solidsun.cz/api"
API_LOGIN = f"{API_BASE}/auth/client-login"
API_DAILY_SUM = f"{API_BASE}/clients/devices/daily-sum"
API_TOTAL_SUM = f"{API_BASE}/clients/devices/total-sum"
API_ACTIVE = f"{API_BASE}/clients/devices/active"

UPDATE_INTERVAL_MINUTES = 30
TOTAL_SUM_INTERVAL_HOURS = 6

SENSOR_GROUPS = {
    "today": "Dnešní den",
    "yesterday": "Včerejší den",
    "total": "Celkem",
}

SENSOR_KEYS = {
    "battery_accumulation": {
        "name": "Akumulace baterie",
        "icon": "mdi:battery-charging",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "battery_production": {
        "name": "Výroba z baterie",
        "icon": "mdi:battery-arrow-up",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "distribution_delivery": {
        "name": "Odběr ze sítě",
        "icon": "mdi:transmission-tower-import",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "distribution_overflow": {
        "name": "Přetoky do sítě",
        "icon": "mdi:transmission-tower-export",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "object_consumption": {
        "name": "Spotřeba objektu",
        "icon": "mdi:home-lightning-bolt",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "sun_production": {
        "name": "Výroba FVE",
        "icon": "mdi:solar-panel",
        "unit": "kWh",
        "device_class": "energy",
        "state_class": "total_increasing",
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
