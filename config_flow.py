from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
import voluptuous as vol
from .camera_io import CameraIO
from .const import DOMAIN

class CCIC1410FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Test connection
            camera = CameraIO(
                user_input[CONF_HOST],
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD]
            )

            success = await self.hass.async_add_executor_job(camera.test_connection)
            
            if success:
                # Create entry
                return self.async_create_entry(
                    title=f"Camera {user_input[CONF_HOST]}",
                    data=user_input
                )
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
        )
