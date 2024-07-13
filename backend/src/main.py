from datetime import datetime, timezone

from backend.src.domain.meterdata import Granularity
from backend.src.fluvius.meterdata_fetcher import MeterDataFetcher


if __name__ == '__main__':
    start = datetime(2024, 7, 7, 22, 00, tzinfo=timezone.utc)
    end = datetime(2024, 7, 11, 22, 00, tzinfo=timezone.utc)

    MeterDataFetcher().fetch_meter_data('541448860010420847', start, end, Granularity.QUARTER_H)

