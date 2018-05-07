#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from announcement import Announcements
from librus import Librus
from time import strftime, sleep
#import xmpp
import config
from os.path import exists
from json import loads, dumps
from cgi import escape

'''def send_xmpp(message_text):
    print("Connecting to XMPP server.")
    jid=xmpp.protocol.JID(config.xmpp_from_jid)
    client=xmpp.Client(jid.getDomain(), debug=[])
    client.connect()
    client.auth(jid.getNode(), config.xmpp_password)

    for receiver in config.xmpp_receivers:
        xmpp_message = xmpp.protocol.Message(receiver, message_text)
        xmpp_message.setAttr('type', 'chat')
        client.send(xmpp_message)'''

def on_new_announcement(announcement):
    global sent_announcements
    events = []
    was_updated = announcement.id in sent_announcements and announcement.checksum not in sent_announcements

    if was_updated or announcement.id not in sent_announcements and "Zmiany w planie Gimnazjum" not in announcement.title:
        if announcement.content:
            for event in announcement.content.split("\n"):
                events.append(event)
        else:
            events.append("\nBrak zmian dla naszej klasy na ten dzień (Jak na razie)")
        message_text = announcement.title+"\n"+"\n".join(events)
        if(not config.disable_messages):
            print(message_text)
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