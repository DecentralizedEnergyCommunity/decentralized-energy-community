from models.timeperiod import TimePeriod, genesis, frequency


def test_timeperiod_genesis():
    timeperiod = TimePeriod.from_id(0)

    assert timeperiod.start == genesis
    assert timeperiod.end == genesis + frequency
