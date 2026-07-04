"""DataUpdateCoordinator for PRESolidsun."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SolidsunApiClient, SolidsunConnectionError
from .const import DOMAIN, UPDATE_INTERVAL_MINUTES

_LOGGER = logging.getLogger(__name__)


class SolidsunCoordinator(DataUpdateCoordinator):
    """Coordinator that fetches all Solidsun data periodically."""

    def __init__(self, hass: HomeAssistant, client: SolidsunApiClient, case_number: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{case_number}",
            update_interval=timedelta(minutes=UPDATE_INTERVAL_MINUTES),
        )
        self.client = client
        self.case_number = case_number

    async def _async_update_data(self) -> dict:
        """Fetch data from API."""
        try:
            return await self.client.async_get_all_data()
        except SolidsunConnectionError as err:
            raise UpdateFailed(f"Error fetching Solidsun data: {err}") from err
