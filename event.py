import pygame
from weakref import WeakValueDictionary, WeakKeyDictionary

HandlerRegistry = WeakValueDictionary()
            
def EventHandler(event):
    def decorator(func):
        HandlerRegistry[event] = func
        return func
    return decorator

def handle_events(dt):
    pygame.event.post(TickEvent)
    
    for event in pygame.event.get():
        handler = HandlerRegistry.get(event.type)
        if handler:
            handler(event, dt)

TickEvent = pygame.event.Event(pygame.USEREVENT + 1)
TickListenerRegistry = WeakKeyDictionary()

def add_tick_listener(listener):
    TickListenerRegistry[listener] = 1

@EventHandler(TickEvent.type)
def tick_callback(event, dt):
    for listener in TickListenerRegistry.keys():
        listener.update(event, dt)