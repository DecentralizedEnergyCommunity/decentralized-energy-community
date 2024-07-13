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
