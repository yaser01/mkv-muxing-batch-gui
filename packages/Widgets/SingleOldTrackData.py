from packages.Widgets.SingleTrackData import SingleTrackData
import typing as typ


class SingleOldTrackData(SingleTrackData):
    def __int__(self):
        super().__init__()
        self.is_enabled: bool | int = False
        self.order = -1

    def __eq__(self, other: typ.Any):
        if not isinstance(other, SingleOldTrackData):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return (
            self.is_enabled == other.is_enabled
            and self.is_forced == other.is_forced
            and self.is_default == other.is_default
            and self.track_name == other.track_name
            and self.language == other.language
            and self.id == other.id
            and self.order == other.order
        )