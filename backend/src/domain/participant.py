from dataclasses import dataclass

from backend.src.domain.meter import Meter


@dataclass
class Participant:

    active: bool
    meters: list[Meter]

    def add_meterdata(self, meterdata):
        self.meterdata.append(meterdata)