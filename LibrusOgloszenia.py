#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from announcement import Announcements
from librus import Librus
import slixmpp
import config
from os.path import exists
from json import loads, dumps


class SendMsgBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipients, msg):
        super().__init__(jid, password)

        self.recipients = recipients
        self.msg = msg

        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()

        for recipient in self.recipients:
            self.send_message(mto=recipient, mbody=self.msg, mtype='chat')

        self.disconnect(wait=True)


def on_new_announcement(announcement):
    global sent_announcements
    events = []
    was_updated = announcement.id in sent_announcements and announcement.checksum not in sent_announcements

    if was_updated or announcement.id not in sent_announcements and "Zmiany w planie Gimnazjum".lower() not in announcement.title.lower():
        if announcement.content:
            for event in announcement.content.split("\n"):
                events.append(event)
        else:
            events.append("\nBrak zmian dla naszej klasy na ten dzień (Jak na razie)")
        message_text = announcement.title+"\n"+"\n".join(events)
        if not config.disable_messages:
            xmpp = SendMsgBot(config.xmpp_from_jid, config.xmpp_password, config.xmpp_receivers, message_text.strip('\t'))
            xmpp.connect()
            xmpp.process(forever=False)
        sent_announcements.append(announcement.id)
        sent_announcements.append(announcement.checksum)
        with open(".sent_announcements", "w+") as fo:
            fo.write(dumps(sent_announcements))


if __name__ == "__main__":
    if exists(".sent_announcements"):
        with open(".sent_announcements", "r+") as fo:
            sent_announcements = loads(fo.read())
    else:
        sent_announcements = []

    a_post_ids = []

    announcements = Announcements(Librus(config.login, config.password), on_new_announcement, config.filter_class)

    print("Updating...")
    announcements.update()
    print("Updated!")