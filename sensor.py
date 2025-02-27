"""Sensor platform for CCIC1410-LAW camera."""
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    camera = data["camera"]
    coordinator = data["coordinator"]
    
    entities = [
        CameraInputSensor(coordinator, camera, config_entry),
        CameraOutputSensor(coordinator, camera, config_entry)
    ]
    
    async_add_entities(entities, True)

class CameraInputSensor(CoordinatorEntity, SensorEntity):
    """Input sensor for CCIC1410-LAW camera."""
    
    def __init__(self, coordinator, camera, config_entry):
        super().__init__(coordinator)
        self._camera = camera
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_input"
        self._attr_name = f"Camera {camera.ip} Input"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = ["high", "low", "unknown"]
        self._attr_icon = "mdi:electric-switch"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get('input', 'unknown')
        return 'unknown'

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return {
            "last_updated": self.coordinator.last_update_success,
            "camera_ip": self._camera.ip
        }

class CameraOutputSensor(CoordinatorEntity, SensorEntity):
    """Output sensor for CCIC1410-LAW camera."""
    
    def __init__(self, coordinator, camera, config_entry):
        super().__init__(coordinator)
        self._camera = camera
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_output"
        self._attr_name = f"Camera {camera.ip} Output"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = ["grounded", "open", "unknown"]
        self._attr_icon = "mdi:power-plug"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get('output', 'unknown')
        return 'unknown'

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return {
            "last_updated": self.coordinator.last_update_success,
            "camera_ip": self._camera.ip
        }
