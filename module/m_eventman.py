"""
Modul zum Verwalten von Ereignissen in einer Kivy-Anwendung.
Grundgerüst von AI als platzhalter für spezifische Implementierungen.
"""

from kivy.eventmanager import EventManager
from kivy.eventmanager import EventDispatcher
from kivy.eventmanager import EventHandler

class EventManager(EventManager):
    """
    Klasse, die Ereignisse verwaltet und Handler für verschiedene Ereignisse registriert.
    Diese Klasse erbt von EventManager und ermöglicht es, Ereignisse zu registrieren und auszulösen.
    """
    def __init__(self, **kwargs):
        super(EventManager, self).__init__(**kwargs)
        self._event_handlers = {}

    def register_event(self, event_name, handler):
        """Registriert einen Ereignis-Handler für ein bestimmtes Ereignis."""
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)

    def trigger_event(self, event_name, *args, **kwargs):
        """Löst ein Ereignis aus und ruft alle registrierten Handler auf."""
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                handler(*args, **kwargs)

    def unregister_event(self, event_name, handler):
        """Entfernt einen Ereignis-Handler für ein bestimmtes Ereignis."""
        if event_name in self._event_handlers:
            if handler in self._event_handlers[event_name]:
                self._event_handlers[event_name].remove(handler)
                if not self._event_handlers[event_name]:
                    del self._event_handlers[event_name]

    def clear_events(self):
        """Entfernt alle registrierten Ereignisse und deren Handler."""
        self._event_handlers.clear()
        super(EventManager, self).clear_events()