# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six

from collections import defaultdict, OrderedDict

from django.utils.importlib import import_module

from cosinnus.core.registries.base import DictBaseRegistry


class WidgetRegistry(DictBaseRegistry):

    _unresolved = defaultdict(set)

    def register(self, app_name, widget):
        from cosinnus.utils.dashboard import DashboardWidget
        if isinstance(widget, six.string_types):
            self._unresolved[app_name].add(widget)
        elif issubclass(widget, DashboardWidget):
            widget_name = widget.get_widget_name()
            if app_name in self:
                self[app_name][widget_name] = widget
            else:
                d = OrderedDict()
                d[widget_name] = widget
                self[app_name] = d

    def get(self, app_name, widget, default=None):
        if app_name in self._unresolved:
            self._resolve(app_name)
        if app_name in self and widget in self[app_name]:
            return self[app_name][widget]
        return default

    def _resolve(self, app_name):
        for widget in list(self._unresolved[app_name]):
            self._unresolved[app_name].remove(widget)
            modulename, _, klass = widget.rpartition('.')
            module = import_module(modulename)
            cls = getattr(module, klass, None)
            if cls is None:
                del self._unresolved[app_name]
                raise ImportError("Cannot import cosinnus widget %s from %s" % (
                    klass, widget))
            else:
                self.register(app_name, cls)
                return cls

    def __iter__(self):
        if self._unresolved:
            for app_name in self._unresolved:
                self._resolve(app_name)
        for app_name, widgets in six.iteritems(self._storage):
            yield (app_name, widgets.keys())

widget_registry = WidgetRegistry()


__all__ = ('widget_registry', )
