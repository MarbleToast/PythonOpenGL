import pygame
from event import EventHandler
from weakref import WeakKeyDictionary

KeyListenerRegistry = WeakKeyDictionary()

def add_key_listener(listener):
    KeyListenerRegistry[listener] = 1

@EventHandler(pygame.KEYDOWN)
def key_callback(event, dt):
    for listener in KeyListenerRegistry.keys():
        listener.update(event, dt)

