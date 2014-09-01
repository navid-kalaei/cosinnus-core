# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, reverse_lazy, NoReverseMatch
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView,
    ListView, UpdateView, TemplateView)
from cosinnus.views.mixins.group import RequireReadMixin, RequireWriteMixin
from cosinnus.models.widget import WidgetConfig
from cosinnus.models.group import CosinnusGroup
from django.http.response import HttpResponseNotFound
from cosinnus.models.cms import CosinnusMicropage
from cosinnus.core.registries import widget_registry
from cosinnus.core.decorators.views import redirect_to_403
from cosinnus.utils.permissions import check_object_write_access
from cosinnus.core.registries.attached_objects import attached_object_registry
from cosinnus.utils.functions import get_cosinnus_app_from_class

class GroupMicrosite(TemplateView):
    """ TODO: Refactor-merge and unify this view to a mixin with DashboardMixin for groups,
        after this view has been generalized to allow Organisations instead of Groups.
    """
    template_name = 'cosinnus/cms/microsite.html'
    group_url_kwarg = 'group'
    
    
    def dispatch(self, request, *args, **kwargs):
        nothing = CosinnusMicropage.objects.none()
        
        group_name = kwargs.get(self.group_url_kwarg, None)
        try:
            group = CosinnusGroup.objects.get(slug=group_name)
        except CosinnusGroup.DoesNotExist:
            return HttpResponseNotFound(_("No group found with this name"))
        self.group = group
        return super(GroupMicrosite, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        widget_filter = self.get_filter()
        widgets = WidgetConfig.objects.filter(**widget_filter).order_by('sort_field')
        ids = widgets.values_list('id', flat=True).all()
        
        widget_configs = []
        """ We also sort each unique widget into the context to be accessed hard-coded"""
        for wc in widgets:
            widget_class = widget_registry.get(wc.app_name, wc.widget_name)
            widget_handle = wc.app_name + '__' + wc.widget_name.replace(" ", "_")
            kwargs.update({widget_handle : wc.id})
            widget = widget_class(self.request, wc)
            widget_configs.append(widget)
            
        
        """ Item list inline views """
        item_inlines = []
        item_limit = 5
        for model_name in ['cosinnus_note.Note', 'cosinnus_etherpad.Etherpad']:
            Renderer = attached_object_registry.get(model_name)
            if Renderer:
                qs_filter = {'group__slug': self.group.slug}
                app_name = get_cosinnus_app_from_class(Renderer)
                item_inlines.append({
                    'model': model_name,
                    'app_name': app_name,
                    'content': Renderer.render_list_for_user(self.request.user, self.request, qs_filter, limit=item_limit, standalone_app=app_name)
                })
        
        kwargs.update({
            'widgets': ids,
            'group': self.group,
            'widget_configs': widget_configs,
            'edit_mode': False,
            'item_inlines': item_inlines,
        })
        return super(GroupMicrosite, self).get_context_data(**kwargs)

    def get_filter(self):
        return {'group_id': self.group.pk, 'type': WidgetConfig.TYPE_MICROSITE}
    
group_microsite = GroupMicrosite.as_view()

        
class GroupMicrositeEdit(GroupMicrosite, RequireWriteMixin):
    
    def dispatch(self, request, *args, **kwargs):
        """ Assure write access to group """
        group_name = kwargs.get(self.group_url_kwarg, None)
        try:
            group = CosinnusGroup.objects.get(slug=group_name)
        except CosinnusGroup.DoesNotExist:
            return HttpResponseNotFound(_("No group found with this name"))
        self.group = group
        if (check_object_write_access(self.group, request.user)):
            return super(GroupMicrosite, self).dispatch(request, *args, **kwargs)
        # Access denied, redirect to 403 page and and display an error message
        return redirect_to_403(request)
            
    def get_context_data(self, **kwargs):
        context = super(GroupMicrositeEdit, self).get_context_data(**kwargs)
        context.update({
            'edit_mode':True
        })
        return context
    
group_microsite_edit = GroupMicrositeEdit.as_view()
