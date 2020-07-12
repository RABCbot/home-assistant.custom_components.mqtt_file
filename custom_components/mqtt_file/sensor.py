"""Support through MQTT."""
from homeassistant.components import mqtt
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.util import slugify
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
import logging
from homeassistant.const import (
    CONF_NAME,
    CONF_FILENAME,
    STATE_UNKNOWN,
    STATE_ON,
    )
import base64

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "MQTT File"
CONF_TOPIC = "topic"
 
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_TOPIC): cv.string,
    vol.Required(CONF_FILENAME): cv.string,
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up sensor."""
    sensors = []
    sensors.append(
        MQTTFileSensor(
            config.get(CONF_NAME), 
            config.get(CONF_TOPIC),
            config.get(CONF_FILENAME)
            )
        )
    async_add_entities(sensors)


class MQTTFileSensor(Entity):
    """Representation of the entity."""

    def __init__(self, name, topic, fname):
        """Initialize the sensor."""

        self._name = name
        self._topic = topic
        self._state = STATE_UNKNOWN
        self._filename = fname

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            _bytes = base64.b64decode(message.payload)
            with open(self._filename, "wb+") as fil:
                fil.write(_bytes)
            self._state = STATE_ON
            self.async_schedule_update_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic, message_received, 1)

    @property
    def name(self):
        """Return the name of the sensor supplied in constructor."""
        return self._name

    @property
    def state(self):
        """Return the current state of the entity."""
        return self._state