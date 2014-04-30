# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six

from collections import defaultdict

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_select2 import (HeavyModelSelect2MultipleChoiceField)
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.db.models import get_model

from cosinnus.models.group import CosinnusGroup
from cosinnus.models.tagged import AttachedObject
from cosinnus.conf import settings
from cosinnus.views.attached_object import AttachableObjectSelect2View
from cosinnus.core.registries import attached_object_registry
from django.core.urlresolvers import reverse

class FormAttachable(forms.ModelForm):
    """
    Used together with AttachableViewMixin.

    Extending this form will automatically add fields for all attachable
    cosinnus models (as configured in `settings.COSINNUS_ATTACHABLE_OBJECTS`)
    to a form. Even though there is a different field for each attachable
    model, this form handles saving all selected objects to the object's
    `attached_objects` M2M field.
    """
    def __init__(self, *args, **kwargs):
        super(FormAttachable, self).__init__(*args, **kwargs)
        
        # retrieve the attached objects ids to select them in the update view
        preresults = []
        if self.instance and self.instance.pk:
            for attached in self.instance.attached_objects.all():
                if attached and attached.target_object:
                    obj = attached.target_object
                    preresults.append( (attached.model_name+":"+str(obj.id), "%s %s" % (attached.model_name, obj.title),)  )
        
        # add a field for each model type of attachable file provided by cosinnus apps
        # each field's name is something like 'attached:cosinnus_file.FileEntry'
        # and fill the field with all available objects for that type (this is passed from our view)
        source_model_id = self._meta.model._meta.app_label + '.' + self._meta.model._meta.object_name
        
        """ Add attachable objects field if this model is configured in settings.py to have objects that can be attached to it """
        if attached_object_registry.get_attachable_to(source_model_id):
            self.fields['attached_objects'] = AttachableObjectSelect2MultipleChoiceField(
                label=_("Attachments"), 
                help_text=_("Type the title and/or type of attachment"), 
                data_url=reverse('cosinnus:attached_object_select2_view', kwargs={'group': self.group.slug, 'model':source_model_id}),
                required=False
            )
            # we need to cheat our way around select2's annoying way of clearing initial data fields
            self.fields['attached_objects'].choices = preresults #((1, 'hi'),)
            self.fields['attached_objects'].initial = [key for key,val in preresults] #[1]
            

    def save_attachable(self):
        """ Called by `AttachableViewMixin.form_valid()`
            For some reason, this field is not being saved automatically,
            even though field and model field are named the same. """
        self.instance.attached_objects.clear()
        for attached_obj in self.cleaned_data.get('attached_objects', []):
            self.instance.attached_objects.add(attached_obj)
        
                    

class AttachableObjectSelect2MultipleChoiceField(HeavyModelSelect2MultipleChoiceField):
    queryset = AttachedObject
    data_view = AttachableObjectSelect2View
    
    def clean(self, value):
        """ We organize the ids gotten back from the recipient select2 field.
            This is a list of mixed ids which could either be groups or users.
            See cosinnus_messages.views.UserSelect2View for how these ids are built.
            
            Example for <value>: [u'cosinnus_event.Event:1', u'cosinnus_file.FileEntry:1'] 
        """
                
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])
        
        #import ipdb; ipdb.set_trace();
        
        attached_objects = []        
        for attached_obj_str in value:
            """ TODO: expand id and model type to real AO """
            obj_type, _, object_id = str(attached_obj_str).partition(':')
            app_label, _, model = obj_type.rpartition('.')
            print ">> app_label, model", app_label, model
            content_type = ContentType.objects.get_for_model(get_model(app_label, model))
            (ao, _) = AttachedObject.objects.get_or_create(content_type=content_type, object_id=object_id)
            attached_objects.append(ao)
            print ">> added attached obj:", ao
        
        print ">> saving attached object field, saving attachments:", attached_objects
        return attached_objects
