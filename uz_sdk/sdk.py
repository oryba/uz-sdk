from datetime import date, time, datetime
from urllib.parse import urljoin

import requests

from utils import compose


class BookingSession:
    SESSION_COOKIE = "_gv_sessid"

    def __init__(self, session=None, base_url="https://booking.uz.gov.ua/en/"):
        self.cookies = {}
        self.base_url = base_url
        if session:
            self.set_session(session)

    def set_session(self, session):
        self.cookies[BookingSession.SESSION_COOKIE] = session

    def get_session(self):
        return self.cookies.get(BookingSession.SESSION_COOKIE)

    def post(self, url, data, *args, update_session=True, **kwargs):
        response = requests.post(urljoin(self.base_url, url), *args, cookies=self.cookies,
                                 data=data, **kwargs)

        session = response.cookies.get(BookingSession.SESSION_COOKIE)
        if update_session and session != self.get_session():
            self.set_session(session)

        return response.json()

    def get(self, url, update_session=True, *args, **kwargs):
        response = requests.get(urljoin(self.base_url, url), *args, cookies=self.cookies, **kwargs)

        session = response.cookies.get(BookingSession.SESSION_COOKIE)
        if update_session and session != self.get_session():
            self.set_session(session)

        return response.json()


class WType:
    def __init__(self, t_id: str, title: str, letter: str, places: int):
        self.t_id, self.title, self.letter, self.places = t_id, title, letter, places

    @classmethod
    def from_json(cls, data):
        return cls(
            t_id=data.get('id'),
            title=data.get('title'),
            letter=data.get('letter'),
            places=data.get('places')
        )

    def __repr__(self):
        return f"{self.t_id} - {self.places}"


class Train:
    def __init__(self, code: str, tr_time: time, types: list):
        self.code = code
        self.types = types
        self.tr_time = tr_time

    @classmethod
    def from_json(cls, data: dict, types_filters: tuple):
        return cls(
            code=data.get('num'),
            tr_time=datetime.strptime(data.get('tr_time', '0:00'), '%H:%M').time(),
            types=compose(
                [WType.from_json(t) for t in data.get('types')],
                types_filters
            )
        )

    def __repr__(self):
        return f"{self.code} ({', '.join(repr(s) for s in self.types)})"


class TicketFinder:
    def __init__(self, src: int, dst: int, src_date: date, src_time: time, bs: BookingSession = None):
        self.bs = bs or BookingSession()
        self.src, self.dst, self.src_date, self.src_time = src, dst, src_date, src_time
        self.train_filters, self.types_filters = (), ()

    def find(self):
        data = self.bs.post('train_search/', data={
            'from': str(self.src),
            'to': str(self.dst),
            'date': self.src_date.strftime("%Y-%m-%d"),
            'time': self.src_time.strftime("%H:%M")
        })

        if data.get('error') == 1:
            if data.get('captcha'):
                raise RuntimeError('Captcha needed')
            raise Exception(f'Unknown error: {data}')

        return compose(
            [Train.from_json(t, self.types_filters) for t in data['data']['list']],
            self.train_filters
        )

    def set_filters(self, train_filters: tuple, types_filters: tuple):
        self.train_filters = train_filters
        self.types_filters = types_filters

    def basic_filters(self, allowed_types: tuple):
        self.set_filters(
            train_filters=(
                lambda trains: [t for t in trains if t.types],
            ),
            types_filters=(
                lambda types: [t for t in types if t.t_id in allowed_types],
            )
        )
