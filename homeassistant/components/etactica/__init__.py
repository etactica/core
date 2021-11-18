"""The eTactica Gateway integration."""
from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import (
    CONNECTION_NETWORK_MAC,
    EVENT_DEVICE_REGISTRY_UPDATED,
    DeviceRegistry,
    async_entries_for_config_entry,
)


from .const import DOMAIN, DATA_UNSUB

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up eTactica Gateway from a config entry."""
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)
    _LOGGER.warning("karl - async setup entry setting up platforms? %s", entry.as_dict())
    device_registry = await hass.helpers.device_registry.async_get_registry()

    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        configuration_url=f"http://{entry.data[CONF_HOST]}/",
        #connections={(CONNECTION_NETWORK_MAC, config[CONF_MAC])},
        manufacturer="eTactica",
        model=entry.data["model"],
        name=entry.title,
        identifiers={(DOMAIN,entry.unique_id)},
    )

    # No platforms, we're only marking discovery with device cards.
    # no platforms to setup, they're autodiscovered by mqtt!
    #hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


# We don't have any "unloading" or "removing" to do thats component specific
# at least, to my understanding..
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("No-op unload of entry: %s", entry.as_dict())
    return True
