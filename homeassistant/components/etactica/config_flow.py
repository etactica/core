"""Config flow to configure the eTactica integration."""
import logging
from typing import Any, Final

import voluptuous as vol

from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_HOST
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.typing import DiscoveryInfoType


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class eTacticaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    # FIXME - we need an async_step_user() to let people pick etactic from the list
    # even if it just says, "you need to go to an url now.." or something?

    # async def async_step_user(self, user_input=None):
    #     """Handle a flow initiated by the user."""
    #     errors = {}
    #     _LOGGER.warning("karl - step user hit: %s", user_input)
    #     if user_input is None:
    #         return self._show_setup_form(user_input, errors)
    #
    #     self._host = user_input[CONF_HOST]
    #
    #     # Check if already configured
    #     await self.async_set_unique_id(self._host)
    #     self._abort_if_unique_id_configured()
    #
    #     return await self.async_step_link()
    #

    async def async_step_confirm_discovery(self, user_input=None):
        """Handle user-confirmation of discovered node."""
        if user_input is not None:
            return self.async_create_entry(
                title=self.name,
                data={
                    # "hostname": self.hostname,
                    "host": self.host,
                    "model": "EG200",
                    # "name": self.name,
                }
            )

        self._set_confirm_only()
        # this still doesn't seem to be doing anything meaningful?
        return self.async_show_form(
            step_id="confirm_discovery",
            description_placeholders={
                "name": self.name,
                "host": self.host,
          },
        )


# {'host': '192.168.122.177',
#  'hostname': 'eg-6BB42F.local.',
#  'name': 'eg-6BB42F._rme-sg._tcp.local.',
#  'port': 22,
#  'properties': {'_raw': {'gid': b'5254006BB42F',
#                          'info': b'eTactica gateway locator'},
#                 'gid': '5254006BB42F',
#                 'info': 'eTactica gateway locator'},
#  'type': '_rme-sg._tcp.local.'}


    async def async_step_zeroconf(self, discovery_info: DiscoveryInfoType) -> data_entry_flow.FlowResult:
        """Initialize flow from zeroconf."""
        _LOGGER.warning("karl: zeroconfi discovered: %s", discovery_info)
        self.host = discovery_info["host"]
        self.hostname = discovery_info["hostname"]
        self.name = discovery_info["name"].split(".", 1)[0]
        # hostname is a shitty fallback, but it's prebaked and ~never changed
        # if they do change their gateway hostname, they should expect things to break
        self.identifier = discovery_info["properties"].get("gid", self.hostname)
        await self.async_set_unique_id(self.identifier)
        _LOGGER.info("karl: set unique id to %s", self.identifier)
        self._abort_if_unique_id_configured()
        _LOGGER.info("karl: not already configrued... continuing?")

        self.context["title_placeholders"] = {"name": self.name}
        # "validate_input" is common here, but whatevs, if it's on zerconf it's as good as we can do right now
        return await self.async_step_confirm_discovery()
