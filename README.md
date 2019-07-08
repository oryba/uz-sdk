# Unofficial UZ API SDK

This project is a light-weight wrapper around some API endpoints 
from [UZ booking system](https://booking.uz.gov.ua). It uses the 
same interface as the frontend of the booking system, so you can
use a session from browser's cookies and work on behalf of your 
account.

## Quick start

```python
from datetime import time, datetime, timedelta

from uz_sdk import TicketFinder, BookingSession

# search tickets from Ternopil to Kyiv for 4 days ahead
tf = TicketFinder(
    2218300,  # from id
    2200001,  # to id
    datetime.now() + timedelta(3),
    time(hour=0, minute=0),
    bs=BookingSession("92o8bh2ok5i51svcmecou51794")
)

# add a filter from preset, skip this to search every type of places
tf.basic_filters(allowed_types=('П', 'К', 'С1'))

# get available trains
data = tf.find()

print(data)
```