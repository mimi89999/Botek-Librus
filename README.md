# Botek-Librus
Program fetching announcements from `Librus Synergia` and sending them as XMPP messages.
We recommend running `LibrusOgloszenia.py` from cron every 5 minutes.

Program ściągający ogłoszenia z `Librus Synergia` w wysyłający je w wiadomościach XMPP.
Zaleca się uruchamianie `LibrusOgloszenia.py` z cron co 5 minut.

## Usage
1. Rename `config.example.py` to `config.py` and complete it with your credentials.
2. Add `LibrusOgloszenia.py` to crontab to be executed every 5 minutes. You use this line:
`*/5 * * * * /path/to/LibrusOgloszenia.py`
