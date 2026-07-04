"""Solidsun API client."""
from __future__ import annotations

import logging
from datetime import date, timedelta

import aiohttp

from .const import API_ACTIVE, API_DAILY_SUM, API_LAST_LOG, API_LOGIN, API_TOTAL_SUM

_LOGGER = logging.getLogger(__name__)


class SolidsunAuthError(Exception):
    """Raised when authentication fails."""


class SolidsunConnectionError(Exception):
    """Raised when connection to API fails."""


class SolidsunApiClient:
    """Client for the Solidsun REST API."""

    def __init__(self, case_number: str, password: str, session: aiohttp.ClientSession) -> None:
        self._case_number = case_number
        self._password = password
        self._session = session
        self._token: str | None = None
        self._client_name: str | None = None

    @property
    def client_name(self) -> str | None:
        return self._client_name

    async def async_login(self) -> dict:
        """Authenticate and store bearer token. Returns client info dict."""
        try:
            async with self._session.post(
                API_LOGIN,
                json={"case_number": self._case_number, "password": self._password},
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 401:
                    raise SolidsunAuthError("Invalid credentials")
                if resp.status != 200:
                    raise SolidsunConnectionError(f"Login failed with status {resp.status}")
                data = await resp.json()
        except SolidsunAuthError:
            raise
        except aiohttp.ClientError as err:
            raise SolidsunConnectionError(f"Connection error: {err}") from err

        self._token = data["token"]
        self._client_name = data.get("client", {}).get("name", self._case_number)
        return data["client"]

    def _headers(self) -> dict:
        if not self._token:
            raise SolidsunAuthError("Not authenticated")
        return {"Authorization": f"Bearer {self._token}"}

    async def async_get_daily_sum(self, target_date: date) -> dict:
        """Fetch daily energy summary for given date."""
        try:
            async with self._session.get(
                API_DAILY_SUM,
                params={"date": target_date.isoformat()},
                headers=self._headers(),
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 401:
                    # Token expired – re-login and retry
                    await self.async_login()
                    return await self.async_get_daily_sum(target_date)
                if resp.status != 200:
                    raise SolidsunConnectionError(f"daily-sum failed: {resp.status}")
                return await resp.json()
        except SolidsunAuthError:
            raise
        except aiohttp.ClientError as err:
            raise SolidsunConnectionError(f"Connection error: {err}") from err

    async def async_get_total_sum(self) -> dict:
        """Fetch total energy summary (all-time)."""
        try:
            async with self._session.get(
                API_TOTAL_SUM,
                headers=self._headers(),
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if resp.status == 401:
                    await self.async_login()
                    return await self.async_get_total_sum()
                if resp.status != 200:
                    raise SolidsunConnectionError(f"total-sum failed: {resp.status}")
                return await resp.json()
        except SolidsunAuthError:
            raise
        except aiohttp.ClientError as err:
            raise SolidsunConnectionError(f"Connection error: {err}") from err

    async def async_get_active(self) -> dict:
        """Fetch active device info. Returns a flattened dict."""
        try:
            async with self._session.get(
                API_ACTIVE,
                headers=self._headers(),
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 401:
                    await self.async_login()
                    return await self.async_get_active()
                if resp.status != 200:
                    raise SolidsunConnectionError(f"active failed: {resp.status}")
                payload = await resp.json()
        except SolidsunAuthError:
            raise
        except aiohttp.ClientError as err:
            raise SolidsunConnectionError(f"Connection error: {err}") from err

        data = payload.get("data", {})
        return {
            "type_label": (data.get("type") or {}).get("label"),
            "mac": data.get("mac"),
            "local_ip": data.get("local_ip"),
            "serial_number_inverter": data.get("serial_number_inverter"),
            "sw_version": data.get("sw_version"),
            "version": data.get("version"),
            "dod_online": data.get("dod_online"),
            "dod_offline": data.get("dod_offline"),
            "last_online_at": (data.get("last_online_at") or {}).get("iso"),
        }

    async def async_get_last_log(self) -> dict:
        """Fetch the latest device log (current values, scaled to kW)."""
        try:
            async with self._session.get(
                API_LAST_LOG,
                headers=self._headers(),
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 401:
                    await self.async_login()
                    return await self.async_get_last_log()
                if resp.status != 200:
                    raise SolidsunConnectionError(f"last-log failed: {resp.status}")
                payload = await resp.json()
        except SolidsunAuthError:
            raise
        except aiohttp.ClientError as err:
            raise SolidsunConnectionError(f"Connection error: {err}") from err

        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    async def async_get_all_data(self) -> dict:
        """Fetch today, yesterday, total, now and device data in one call."""
        today = date.today()
        yesterday = today - timedelta(days=1)

        today_data = await self.async_get_daily_sum(today)
        yesterday_data = await self.async_get_daily_sum(yesterday)
        total_data = await self.async_get_total_sum()
        now_data = await self.async_get_last_log()
        device_data = await self.async_get_active()

        return {
            "today": today_data,
            "yesterday": yesterday_data,
            "total": total_data,
            "now": now_data,
            "device": device_data,
        }
