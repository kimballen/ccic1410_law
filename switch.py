"""Switch platform for CCIC1410-LAW camera."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    camera = data["camera"]
    coordinator = data["coordinator"]
    
    async_add_entities([CameraOutputSwitch(coordinator, camera, config_entry)], True)

class CameraOutputSwitch(CoordinatorEntity, SwitchEntity):
    """Switch for controlling CCIC1410-LAW camera output."""
    
    def __init__(self, coordinator, camera, config_entry):
        super().__init__(coordinator)
        self._camera = camera
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_output_switch"
        self._attr_name = f"Camera {camera.ip} Output Control"
        self._attr_icon = "mdi:electric-switch"

    @property
    def is_on(self):
        """Return true if switch is on."""
        if self.coordinator.data:
            return self.coordinator.data.get('output') == "grounded"
        return False

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        success = await self.hass.async_add_executor_job(
            self._camera.set_output, True
        )
        if success:
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        success = await self.hass.async_add_executor_job(
            self._camera.set_output, False
        )
        if success:
            await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return {
            "last_updated": self.coordinator.last_update_success,
            "camera_ip": self._camera.ip
        }
