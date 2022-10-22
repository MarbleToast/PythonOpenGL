import pygame
from event import EventHandler
from weakref import WeakKeyDictionary

MouseListenerRegistry = WeakKeyDictionary()

def add_mouse_listener(listener):
    MouseListenerRegistry[listener] = 1

@EventHandler(pygame.MOUSEMOTION)
def mouse_callback(event, dt):
    for listener in MouseListenerRegistry.keys():
        listener.update(event)