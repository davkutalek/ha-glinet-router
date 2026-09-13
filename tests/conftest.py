"""Pytest configuration for the ha-glinet-router test suite.

The integration depends on the `glinet` library (which itself depends on
`aiohttp` and `passlib`). Those packages are installed as regular
dependencies in the test environment, so this conftest only needs to stub
the Home Assistant runtime modules (which are not available when running
the integration tests in isolation).
"""

from __future__ import annotations

import asyncio
import inspect
import sys
import types
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import IntFlag
from typing import Any


def pytest_configure() -> None:
    try:
        import voluptuous
    except ModuleNotFoundError:
        voluptuous = types.ModuleType("voluptuous")
        sys.modules.setdefault("voluptuous", voluptuous)
    if not hasattr(voluptuous, "Schema"):
        voluptuous.Schema = type(
            "Schema",
            (),
            {"__call__": lambda self, x: x, "__init__": lambda *a, **k: None},
        )
        voluptuous.Required = lambda *args, **kwargs: args[0] if args else None
        voluptuous.Optional = lambda *args, **kwargs: args[0] if args else None
        voluptuous.All = lambda *args, **kwargs: args[0] if args else None
        voluptuous.Coerce = lambda *args, **kwargs: args[0] if args else None
        voluptuous.Clamp = lambda *args, **kwargs: args[0] if args else None
        voluptuous.In = lambda *args, **kwargs: args[0] if args else None
        voluptuous.Range = lambda *args, **kwargs: args[0] if args else None

    try:
        __import__("homeassistant")
    except ModuleNotFoundError:
        homeassistant = types.ModuleType("homeassistant")
        config_entries = types.ModuleType("homeassistant.config_entries")

        class MockFlow:
            def __init_subclass__(cls, **kwargs: Any) -> None:
                super().__init_subclass__()

        config_entries.ConfigFlow = MockFlow
        config_entries.OptionsFlow = MockFlow
        homeassistant.config_entries = config_entries

        components = types.ModuleType("homeassistant.components")
        device_tracker = types.ModuleType("homeassistant.components.device_tracker")
        device_tracker.CONF_CONSIDER_HOME = "consider_home"
        device_tracker.DEFAULT_CONSIDER_HOME = types.SimpleNamespace(total_seconds=lambda: 180)
        device_tracker.DOMAIN = "device_tracker"
        device_tracker.SourceType = types.SimpleNamespace(ROUTER="router")
        device_tracker.ScannerEntity = object

        const = types.ModuleType("homeassistant.const")
        const.CONF_HOST = "host"
        const.CONF_MAC = "mac"
        const.CONF_MODEL = "model"
        const.CONF_PASSWORD = "password"
        const.CONF_USERNAME = "username"
        const.PERCENTAGE = "%"
        const.EntityCategory = types.SimpleNamespace(DIAGNOSTIC="diagnostic", CONFIG="config")
        const.UnitOfTemperature = types.SimpleNamespace(CELSIUS="C")

        exceptions = types.ModuleType("homeassistant.exceptions")
        exceptions.HomeAssistantError = type("HomeAssistantError", (Exception,), {})
        exceptions.ConfigEntryAuthFailed = type("ConfigEntryAuthFailed", (Exception,), {})
        exceptions.ConfigEntryNotReady = type("ConfigEntryNotReady", (Exception,), {})

        helpers = types.ModuleType("homeassistant.helpers")
        helpers.selector = types.ModuleType("homeassistant.helpers.selector")
        helpers.selector.TextSelector = lambda *args, **kwargs: None
        helpers.selector.TextSelectorConfig = lambda *args, **kwargs: None
        helpers.selector.TextSelectorType = types.SimpleNamespace(
            URL="url", PASSWORD="password", TEXT="text"
        )
        helpers.selector.SelectSelector = lambda *args, **kwargs: None
        helpers.selector.SelectSelectorConfig = lambda *args, **kwargs: None
        helpers.selector.SelectSelectorMode = types.SimpleNamespace(DROPDOWN="dropdown")

        entity_registry = types.ModuleType("homeassistant.helpers.entity_registry")
        entity_registry.async_get = lambda hass: None
        entity_registry.async_entries_for_config_entry = lambda registry, entry_id: []

        aiohttp_client = types.ModuleType("homeassistant.helpers.aiohttp_client")
        aiohttp_client.async_get_clientsession = lambda hass: None

        device_registry = types.ModuleType("homeassistant.helpers.device_registry")
        device_registry.CONNECTION_NETWORK_MAC = "mac"
        device_registry.format_mac = lambda mac: str(mac).lower()
        device_registry.async_get = lambda hass: types.SimpleNamespace(
            async_get_device_by_connection=lambda connection, config_entry_id: None,
            async_get_device_by_identifier=lambda identifier, config_entry_id: None,
        )

        dispatcher = types.ModuleType("homeassistant.helpers.dispatcher")
        dispatcher.async_dispatcher_connect = lambda *args, **kwargs: lambda: None
        dispatcher.async_dispatcher_send = lambda *args, **kwargs: None

        entity = types.ModuleType("homeassistant.helpers.entity")
        entity.DeviceInfo = dict

        helpers.config_validation = types.ModuleType("homeassistant.helpers.config_validation")
        helpers.config_validation.string = lambda v: v
        helpers.config_validation.boolean = lambda v: v
        helpers.config_validation.integer = lambda v: v

        event = types.ModuleType("homeassistant.helpers.event")
        event.async_track_time_interval = lambda *args, **kwargs: None

        update_coordinator = types.ModuleType("homeassistant.helpers.update_coordinator")

        class MockCoordinator:
            def __init__(self, *args, **kwargs):
                self.hass = args[0]
                self.data = None
                self.update_interval = kwargs.get("update_interval")

            def __class_getitem__(cls, _):
                return cls

            async def async_config_entry_first_refresh(self):
                pass

            async def async_request_refresh(self):
                pass

            async def async_refresh(self):
                pass

        update_coordinator.DataUpdateCoordinator = MockCoordinator
        update_coordinator.UpdateFailed = type("UpdateFailed", (Exception,), {})

        class MockCoordinatorEntity:
            def __init__(self, coordinator, *args, **kwargs):
                self.coordinator = coordinator
                self.hass = coordinator.hass

            def __class_getitem__(cls, _):
                return cls

            def _handle_coordinator_update(self) -> None:
                pass

        update_coordinator.CoordinatorEntity = MockCoordinatorEntity

        core = types.ModuleType("homeassistant.core")
        core.HomeAssistant = object
        core.callback = lambda func: func
        core.SupportsResponse = types.SimpleNamespace(ONLY="only", OPTIONAL="optional", NONE="none")

        data_entry_flow = types.ModuleType("homeassistant.data_entry_flow")
        data_entry_flow.AbortFlow = type("AbortFlow", (Exception,), {})

        util = types.ModuleType("homeassistant.util")
        dt = types.ModuleType("homeassistant.util.dt")
        dt.utcnow = lambda: datetime.now(UTC).replace(tzinfo=None)
        components.device_tracker = device_tracker
        helpers.entity_registry = entity_registry
        helpers.aiohttp_client = aiohttp_client
        helpers.device_registry = device_registry
        helpers.dispatcher = dispatcher
        helpers.entity = entity
        helpers.event = event
        helpers.update_coordinator = update_coordinator
        util.dt = dt

        @dataclass(frozen=True, kw_only=True)
        class SensorEntityDescription:
            key: str
            name: str | None = None
            has_entity_name: bool | None = None
            icon: str | None = None
            entity_category: str | None = None
            translation_key: str | None = None
            device_class: str | None = None
            native_unit_of_measurement: str | None = None
            state_class: str | None = None
            suggested_display_precision: int | None = None
            options: list[str] | None = None

        sensor = types.ModuleType("homeassistant.components.sensor")
        sensor.SensorDeviceClass = types.SimpleNamespace(
            DATA_RATE="data_rate",
            DATA_SIZE="data_size",
            ENUM="enum",
            TEMPERATURE="temperature",
            TIMESTAMP="timestamp",
        )
        sensor.SensorEntity = object
        sensor.SensorEntityDescription = SensorEntityDescription
        sensor.SensorStateClass = types.SimpleNamespace(
            MEASUREMENT="measurement",
            TOTAL_INCREASING="total_increasing",
            TOTAL="total",
        )
        switch = types.ModuleType("homeassistant.components.switch")
        switch.SwitchEntity = object
        select = types.ModuleType("homeassistant.components.select")
        select.SelectEntity = object
        binary_sensor = types.ModuleType("homeassistant.components.binary_sensor")
        binary_sensor.BinarySensorEntity = object
        binary_sensor.BinarySensorDeviceClass = types.SimpleNamespace(
            CONNECTIVITY="connectivity",
            RUNNING="running",
        )
        update = types.ModuleType("homeassistant.components.update")

        class _UpdateEntityFeature(IntFlag):
            INSTALL = 1
            RELEASE_NOTES = 2
            PROGRESS = 4

        update.UpdateEntity = object
        update.UpdateEntityFeature = _UpdateEntityFeature
        update.UpdateDeviceClass = types.SimpleNamespace(FIRMWARE="firmware")
        homeassistant.components = components
        homeassistant.components.sensor = sensor
        homeassistant.components.switch = switch
        homeassistant.components.select = select
        homeassistant.components.binary_sensor = binary_sensor
        homeassistant.components.update = update
        homeassistant.config_entries = config_entries
        homeassistant.core = core
        homeassistant.const = const
        homeassistant.data_entry_flow = data_entry_flow
        homeassistant.exceptions = exceptions
        homeassistant.helpers = helpers
        homeassistant.util = util

        sys.modules["homeassistant"] = homeassistant
        sys.modules["homeassistant.config_entries"] = config_entries
        sys.modules["homeassistant.core"] = core
        sys.modules["homeassistant.data_entry_flow"] = data_entry_flow
        sys.modules["homeassistant.components"] = components
        sys.modules["homeassistant.components.device_tracker"] = device_tracker
        sys.modules["homeassistant.const"] = const
        sys.modules["homeassistant.exceptions"] = exceptions
        sys.modules["homeassistant.helpers"] = helpers
        sys.modules["homeassistant.helpers.selector"] = helpers.selector
        sys.modules["homeassistant.helpers.config_validation"] = helpers.config_validation
        sys.modules["homeassistant.helpers.entity_registry"] = entity_registry
        sys.modules["homeassistant.helpers.aiohttp_client"] = aiohttp_client
        sys.modules["homeassistant.helpers.device_registry"] = device_registry
        sys.modules["homeassistant.helpers.dispatcher"] = dispatcher
        sys.modules["homeassistant.helpers.entity"] = entity
        sys.modules["homeassistant.helpers.event"] = event
        sys.modules["homeassistant.helpers.update_coordinator"] = update_coordinator
        sys.modules["homeassistant.util"] = util
        sys.modules["homeassistant.util.dt"] = dt
        sys.modules["homeassistant.components.sensor"] = sensor
        sys.modules["homeassistant.components.switch"] = switch
        sys.modules["homeassistant.components.select"] = select
        sys.modules["homeassistant.components.binary_sensor"] = binary_sensor
        sys.modules["homeassistant.components.update"] = update


def pytest_pyfunc_call(pyfuncitem: Any) -> bool:
    testfunction = pyfuncitem.obj
    if not inspect.iscoroutinefunction(testfunction):
        return False

    kwargs = {name: pyfuncitem.funcargs[name] for name in pyfuncitem._fixtureinfo.argnames}
    asyncio.run(testfunction(**kwargs))
    return True
