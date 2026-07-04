"""Config flow for PREsolidsun integration."""
from __future__ import annotations

import logging

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SolidsunApiClient, SolidsunAuthError, SolidsunConnectionError
from .const import CONF_CASE_NUMBER, CONF_PASSWORD, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CASE_NUMBER): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class SolidsunConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Solidsun."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            case_number = user_input[CONF_CASE_NUMBER].strip().upper()
            password = user_input[CONF_PASSWORD]

            # Prevent duplicate entries for same case number
            await self.async_set_unique_id(case_number)
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            client = SolidsunApiClient(case_number, password, session)

            try:
                client_info = await client.async_login()
                title = f"{client_info.get('name', case_number)}"
            except SolidsunAuthError:
                errors["base"] = "invalid_auth"
            except SolidsunConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during Solidsun login")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=title,
                    data={
                        CONF_CASE_NUMBER: case_number,
                        CONF_PASSWORD: password,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
