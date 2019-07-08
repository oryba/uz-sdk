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

tf.basic_filters(allowed_types=('П', 'К', 'С1'))

data = tf.find()

print(data)
