#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import gobject
import dbus
import dbus.mainloop.glib
import Skype4Py

# ----------------------------------------------------------------------------------------------------
# Fired on attachment status change. Here used to re-attach this script to Skype in case attachment is lost. Just in case.
def OnAttach(status):
    print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(status)
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach();

    if status == Skype4Py.apiAttachSuccess:
       print('******************************************************************************');


# ----------------------------------------------------------------------------------------------------
# Fired on chat message status change. 
# Statuses can be: 'UNKNOWN' 'SENDING' 'SENT' 'RECEIVED' 'READ'        

def OnMessageStatus(Message, Status):
    if Status == 'RECEIVED':
        print(Message.FromDisplayName + ': ' + Message.Body)
        body = "<html><b>" + Message.FromDisplayName + ":</b> " + Message.Body.replace("\n", "<br/>") + "</html>"

        notifications.Notify('skype-visual-notifications', 0, '/usr/share/pixmaps/skype.png', Message.Chat.FriendlyName, body, ai, dbus.Dictionary, 10000)

    if Status == 'SENT':
        print('Myself: ' + Message.Body);

	notifications.Notify('skype-visual-notifications', 0, '/usr/share/pixmaps/skype.png', 'Myself', Message.Body, ai, dbus.Dictionary, 10000)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

sessionBus = dbus.SessionBus()
notifications = sessionBus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')

# ----------------------------------------------------------------------------------------------------
# Creating instance of Skype object, assigning handler functions and attaching to Skype.
skype = Skype4Py.Skype();
skype.OnAttachmentStatus = OnAttach;
skype.OnMessageStatus = OnMessageStatus;

print('******************************************************************************');
print 'Connecting to Skype..'
skype.Attach();

loop = gobject.MainLoop()
loop.run()

