from typing import List, Optional, Literal

from .preset_models import ServerPreset


Location = Literal["ru-1", "ru-2", "kz-1", "nl-1", "us-2", "ru-3"]

ALLOWED_LOCATIONS: set[str] = {
    "ru-1",
    "ru-2",
    "kz-1",
    "nl-1",
    "us-2",
    "ru-3",
}


class PresetSelector:
    def __init__(self, presets: List[ServerPreset]):
        self._presets = presets
        self._filters: List[ServerPreset] = presets.copy()

    @staticmethod
    def _validate_location(location: str):
        if location not in ALLOWED_LOCATIONS:
            raise ValueError(
                f"Invalid location '{location}'. " f"Allowed: {sorted(ALLOWED_LOCATIONS)}"
            )

    def _filter(self, fn):
        self._filters = list(filter(fn, self._filters))
        return self

    def reset(self):
        self._filters = self._presets.copy()
        return self

    def location(self, location: Location):
        self._validate_location(location)
        return self._filter(lambda p: p.location == location)

    def nvme_only(self):
        return self._filter(lambda p: p.disk_type.lower() == "nvme")

    def high_cpu(self, location: Optional[Location] = None):
        if location:
            self.location(location)

        return self._filter(lambda p: float(p.cpu_frequency) >= 5.0)

    def recommended(self, location: Optional[Location] = None):
        if location:
            self.location(location)

        return self._filter(lambda p: any("recommended" in tag for tag in p.tags))

    def by_hardware(
        self,
        cpu: Optional[int] = None,
        ram: Optional[int] = None,
    ):
        if cpu is not None:
            self._filter(lambda p: p.cpu == cpu)

        if ram is not None:
            self._filter(lambda p: p.ram == ram)

        return self

    def by_bandwidth(self, bandwidth: Literal[200, 1000]):
        if bandwidth is not None:
            self._filter(lambda p: p.bandwidth == bandwidth)

        return self

    def cheapest(self, location: Optional[Location] = None) -> ServerPreset:
        if location:
            self.location(location)

        if not self._filters:
            raise ValueError("No presets match the criteria")

        return min(self._filters, key=lambda p: p.price)

    def most_expensive(self, location: Optional[Location] = None) -> ServerPreset:
        if location:
            self.location(location)

        if not self._filters:
            raise ValueError("No presets match the criteria")

        return max(self._filters, key=lambda p: p.price)

    def all(self) -> List[ServerPreset]:
        return self._filters
