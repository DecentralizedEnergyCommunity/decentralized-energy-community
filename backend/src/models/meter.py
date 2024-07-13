from dataclasses import dataclass
from typing import NewType

EAN = NewType('EAN', str)


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

