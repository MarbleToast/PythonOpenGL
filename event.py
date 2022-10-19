import pygame

HandlerRegistry = {}

def register_handler(event):
    def decorator(func):
        HandlerRegistry[event] = func
        return func
    return decorator

def handle_events():
    for event in pygame.event.get():
        handler = HandlerRegistry.get(event.type)
        if handler:
            handler(event)
        else:
            print(f"No handler for {event}")
