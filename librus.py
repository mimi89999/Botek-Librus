# -*- coding: utf-8 -*-

import requests
import re
import urllib.request
import urllib.error


class WrongPasswordError(Exception):
    pass


class SessionExpiredError(Exception):
    pass


class Librus:
    """Klasa odpowiadająca za odbieranie danych z librusa"""

    PATTERN_CSRF = re.compile(
        '<meta name=\\"csrf-token\\" content=\\"(\w+)\\">')

    BASE_URL = "https://api.librus.pl/2.0/"
    URL_ME = BASE_URL + "Me"
    URL_ANNOUNCEMENT = BASE_URL + "SchoolNotices"

    def __init__(self, login, password):
        self.__username = login
        self.__password = password
        self.__client = requests.session()
        self.login()

    def login(self):
        """Funkcja wykonująca logowanie do librusa"""
        # Odebranie ciasteczek
        res = self.__client.get('https://portal.librus.pl/rodzina')
        csrf = self.PATTERN_CSRF.findall(res.content.decode('utf-8'))[0]

        # Należy pamiętać, że to Xml-Http-Request i wysyłany jest JSON,
        # zwykły POST nie działa
        self.__client.post('https://portal.librus.pl/rodzina/login/action',
                           json={'email': self.__username,
                                 'password': self.__password},
                           headers={'X-CSRF-TOKEN': csrf})

        synergia_account = self.__client.get(
            'https://portal.librus.pl/api/v2/SynergiaAccounts').json()[
            'accounts'][0]

        user_token = synergia_account['accessToken']
        synergia_login = synergia_account['login']

        self.__client.headers.update({'Authorization': 'Bearer {}'.format(user_token)})

        if self.__client.get(self.URL_ME).status_code == 401:
            self.__client.headers.update({'Authorization': 'Bearer {}'.format(librus_token)})

            user_token = self.__client.get(
                'https://portal.librus.pl/api/v2/SynergiaAccounts/fresh/' + synergia_login).json()[
                'accounts'][0]['accessToken']

            self.__client.headers.update({'Authorization': 'Bearer {}'.format(user_token)})

    def get_announcements(self):
        """
        Funkcja pobierająca dane ze strony https://librus.synergia.pl/ogloszenia
        :returns: :return: lista [{"author": autor,
                         "title": tytuł,
                         "time": czas,
                         "content": zawartość}]
        """
        # Załadowanie ogłoszeń
        try:
            data = self.__client.get(self.URL_ANNOUNCEMENT).json()
        except urllib.error.HTTPError:
            raise SessionExpiredError
        print(data)
        return [{'author': notice[u'AddedBy'][u'Id'],
                 'title': notice[u'Subject'],
                 'content': notice[u'Content'],
                 'time': notice[u'StartDate']
                 } for notice in data[u'SchoolNotices']]
