"""The CCIC1410-LAW Camera IO integration."""
import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .camera_io import CameraIO

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR, Platform.SWITCH]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Create camera instance
    camera = CameraIO(
        entry.data["host"],
        entry.data["username"],
        entry.data["password"]
    )
    
    # Test connection before proceeding
    try:
        is_connected = await hass.async_add_executor_job(camera.test_connection)
        if not is_connected:
            raise ConfigEntryNotReady(f"Failed to connect to camera at {entry.data['host']}")
            
        async def async_update_data() -> dict[str, Any]:
            """Fetch data from camera."""
            try:
                return await hass.async_add_executor_job(camera.get_io_status)
            except Exception as err:
                raise UpdateFailed(f"Error communicating with camera: {err}")

        coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=f"camera_io_{entry.entry_id}",
            update_method=async_update_data,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

        # Initial data fetch
        await coordinator.async_config_entry_first_refresh()
        
        # Store both camera and coordinator
        hass.data[DOMAIN][entry.entry_id] = {
            "camera": camera,
            "coordinator": coordinator,
        }
        
        # Set up platforms using the correct async method
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        
        return True
        
    except Exception as err:
        raise ConfigEntryNotReady(f"Error setting up camera: {str(err)}")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
