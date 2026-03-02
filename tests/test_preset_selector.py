import pytest

from timeweb_cloud_sdk.servers.preset_models import ServerPreset
from timeweb_cloud_sdk.servers.preset_selector import PresetSelector


def make_preset(id, cpu=2, ram=2048, disk_type="ssd", name="basic"):
    return ServerPreset(
        id=id,
        price=100,
        cpu=cpu,
        cpu_frequency="3.0",
        ram=ram,
        disk=20,
        disk_type=disk_type,
        bandwidth=100,
        is_allowed_local_network=True,
        vds_node_configuration_name=name,
        tags=[],
    )


def test_selector_reset():
    presets = [make_preset(1), make_preset(2)]
    selector = PresetSelector(presets)

    selector._filters = []
    selector.reset()

    assert len(selector._filters) == 2


def test_selector_invalid_location():
    presets = [make_preset(1)]
    selector = PresetSelector(presets)

    with pytest.raises(ValueError):
        selector.location("invalid")


def test_selector_nvme():
    presets = [
        make_preset(1, disk_type="nvme"),
        make_preset(2, disk_type="ssd"),
    ]

    selector = PresetSelector(presets)
    result = selector.nvme_only()._filters

    assert len(result) == 1
    assert result[0].disk_type == "nvme"
