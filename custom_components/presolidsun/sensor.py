"""Sensor platform for Solidsun."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfEnergy, UnitOfPower, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    CONF_CASE_NUMBER,
    DEVICE_INFO_KEYS,
    DOMAIN,
    NOW_EXTRA_KEYS,
    SENSOR_GROUPS,
    SENSOR_KEYS,
    WORK_MODE_LABELS,
)
from .coordinator import SolidsunCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solidsun sensors."""
    coordinator: SolidsunCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for group_key, group_meta in SENSOR_GROUPS.items():
        for sensor_key, meta in SENSOR_KEYS.items():
            entities.append(
                SolidsunSensor(coordinator, entry, group_key, group_meta, sensor_key, meta)
            )

    for data_key, meta in NOW_EXTRA_KEYS.items():
        entities.append(SolidsunNowExtraSensor(coordinator, entry, data_key, meta))

    for info_key, meta in DEVICE_INFO_KEYS.items():
        entities.append(SolidsunDeviceSensor(coordinator, entry, info_key, meta))

    async_add_entities(entities)


def _build_device_info(coordinator: SolidsunCoordinator, case_number: str) -> DeviceInfo:
    """Shared DeviceInfo so all entities group under one device."""
    return DeviceInfo(
        identifiers={(DOMAIN, case_number)},
        name=f"FVE - {case_number}",
        manufacturer="PREsolidsun",
        model="FVE",
        configuration_url="https://www.solidsun.cz",
    )


def _short_op(case_number: str) -> str:
    """Return the last segment of the OP number (e.g. OP-22-39017 -> 39017)."""
    return case_number.split("-")[-1]


class SolidsunSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Solidsun energy sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SolidsunCoordinator,
        entry: ConfigEntry,
        group_key: str,
        group_meta: dict,
        sensor_key: str,
        meta: dict,
    ) -> None:
        super().__init__(coordinator)
        self._group_key = group_key
        self._sensor_key = sensor_key
        self._entry = entry

        case_number = entry.data[CONF_CASE_NUMBER]
        short_op = _short_op(case_number)

        self._attr_unique_id = f"{case_number}_{group_key}_{sensor_key}"
        self.entity_id = f"sensor.solidsun_{short_op}_{group_meta['slug']}_{meta['slug']}"
        self._attr_name = f"{group_meta['label']} – {meta['name']}"
        self._attr_icon = meta["icon"]

        if group_meta["instant"]:
            self._attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
            self._attr_device_class = SensorDeviceClass.POWER
            self._attr_state_class = SensorStateClass.MEASUREMENT
        else:
            self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING

        self._attr_device_info = _build_device_info(coordinator, case_number)

    @property
    def native_value(self) -> float | None:
        """Return sensor value."""
        if self.coordinator.data is None:
            return None
        group_data = self.coordinator.data.get(self._group_key, {})
        return group_data.get(self._sensor_key)


class SolidsunDeviceSensor(CoordinatorEntity, SensorEntity):
    """Diagnostic sensor with device info from the active endpoint."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: SolidsunCoordinator,
        entry: ConfigEntry,
        info_key: str,
        meta: dict,
    ) -> None:
        super().__init__(coordinator)
        self._info_key = info_key
        case_number = entry.data[CONF_CASE_NUMBER]

        self._attr_unique_id = f"{case_number}_device_{info_key}"
        self.entity_id = f"sensor.solidsun_{_short_op(case_number)}_{meta['slug']}"
        self._attr_name = meta["name"]
        self._attr_icon = meta["icon"]
        if meta.get("unit"):
            self._attr_native_unit_of_measurement = meta["unit"]
        self._attr_device_info = _build_device_info(coordinator, case_number)

    @property
    def native_value(self):
        """Return device info value."""
        if self.coordinator.data is None:
            return None
        device_data = self.coordinator.data.get("device", {})
        return device_data.get(self._info_key)


class SolidsunNowExtraSensor(CoordinatorEntity, SensorEntity):
    """Doplňkový senzor skupiny Nyní (stav baterie, režim, platnost dat)."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SolidsunCoordinator,
        entry: ConfigEntry,
        data_key: str,
        meta: dict,
    ) -> None:
        super().__init__(coordinator)
        self._data_key = data_key
        self._kind = meta["kind"]
        case_number = entry.data[CONF_CASE_NUMBER]
        now_meta = SENSOR_GROUPS["now"]

        self._attr_unique_id = f"{case_number}_now_{data_key}"
        self.entity_id = f"sensor.solidsun_{_short_op(case_number)}_{now_meta['slug']}_{meta['slug']}"
        self._attr_name = f"{now_meta['label']} – {meta['name']}"
        self._attr_icon = meta["icon"]

        if self._kind == "battery":
            self._attr_native_unit_of_measurement = PERCENTAGE
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif self._kind == "timestamp":
            self._attr_device_class = SensorDeviceClass.TIMESTAMP
        elif self._kind == "work_mode":
            self._attr_device_class = SensorDeviceClass.ENUM
            self._attr_options = list(WORK_MODE_LABELS.values())

        self._attr_device_info = _build_device_info(coordinator, case_number)

    @property
    def native_value(self):
        """Return the current value converted for the sensor kind."""
        if self.coordinator.data is None:
            return None
        now_data = self.coordinator.data.get("now", {})
        raw = now_data.get(self._data_key)
        if raw is None:
            return None

        if self._kind == "battery":
            try:
                return float(raw)
            except (TypeError, ValueError):
                return None
        if self._kind == "work_mode":
            return WORK_MODE_LABELS.get(str(raw))
        if self._kind == "timestamp":
            return dt_util.parse_datetime(raw)
        return raw
