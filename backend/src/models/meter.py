from dataclasses import dataclass
from typing import NewType

EAN = NewType("EAN", str)

ean541448820044186577 = EAN("541448820044186577")
ean541448820060527996 = EAN("541448820060527996")
ean541449500000446547 = EAN("541449500000446547")


class MeterType:
    CONSUMER = 0
    PRODUCER = 1


@dataclass
class Meter:
    meter_type: MeterType
    ean: EAN

    @property
    def is_producer(self):
        return self.meter_type == MeterType.PRODUCER

    @property
    def is_consumer(self):
        return self.meter_type == MeterType.CONSUMER
