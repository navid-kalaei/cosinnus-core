# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
import locale

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
import six

from cosinnus.conf import settings
from cosinnus.core import signals
from cosinnus.models.group import CosinnusPortal
from cosinnus.models.tagged import LikeObject
from cosinnus.utils.files import get_idea_image_filename, image_thumbnail_url, \
    image_thumbnail
from cosinnus.utils.functions import clean_single_line_text, \
    unique_aware_slugify
from cosinnus.utils.urls import get_domain_for_portal
from cosinnus.models.mixins.indexes import IndexingUtilsMixin
from django.contrib.contenttypes.generic import GenericRelation

# this reads the environment and inits the right locale
try:
    locale.setlocale(locale.LC_ALL, ("de_DE", "utf8"))
except:
    locale.setlocale(locale.LC_ALL, "")



class CosinnusIdeaQS(models.query.QuerySet):

    def annotate_likes(self):
        """ Annotates the number of likes as `like_count` """
        ann = self.annotate(
                like_count=models.Count(
                    models.Case(
                        models.When(likes__liked=True, then=1),
                            default=0, output_field=models.IntegerField()
                    )
                )
            )
        return ann

class IdeaManager(models.Manager):
    
    # main slug to object key
    _IDEAS_SLUG_CACHE_KEY = 'cosinnus/core/portal/%d/idea/slug/%s' # portal_id, slug -> idea
    # (pk -> slug) dict
    _IDEAS_PK_TO_SLUG_CACHE_KEY = 'cosinnus/core/portal/%d/idea/pks' # portal_id -> {(pk, slug), ...} 
    
    def get_cached(self, slugs=None, pks=None, select_related_media_tag=True, portal_id=None):
        """
        Gets all ideas defined by either `slugs` or `pks`.

        `slugs` and `pks` may be a list or tuple of identifiers to use for
        request where the elements are of type string / unicode or int,
        respectively. You may provide a single string / unicode or int directly
        to query only one object.

        :returns: An instance or a list of instances of :class:`CosinnusGroup`.
        :raises: If a single object is defined a `CosinnusGroup.DoesNotExist`
            will be raised in case the requested object does not exist.
        """
        if portal_id is None:
            portal_id = CosinnusPortal.get_current().id
            
        # Check that at most one of slugs and pks is set
        assert not (slugs and pks)
        assert not (slugs or pks)
            
        if slugs is not None:
            if isinstance(slugs, six.string_types):
                # We request a single idea
                slugs = [slugs]
                
            # We request multiple ideas by slugs
            keys = [self._IDEAS_SLUG_CACHE_KEY % (portal_id, s) for s in slugs]
            ideas = cache.get_many(keys)
            missing = [key.split('/')[-1] for key in keys if key not in ideas]
            if missing:
                # we can only find ideas via this function that are in the same portal we run in
                query = self.get_queryset().filter(portal__id=portal_id, is_active=True, slug__in=missing)
                if select_related_media_tag:
                    query = query.select_related('media_tag')
                
                for idea in query:
                    ideas[self._IDEAS_SLUG_CACHE_KEY % (portal_id, idea.slug)] = idea
                cache.set_many(ideas, settings.COSINNUS_IDEA_CACHE_TIMEOUT)
            
            # sort by a good sorting function that acknowldges umlauts, etc, case insensitive
            idea_list = ideas.values()
            idea_list.sort(cmp=locale.strcoll, key=lambda x: x.name)
            return idea_list
            
        elif pks is not None:
            if isinstance(pks, int):
                pks = [pks]
            else:
                # We request multiple ideas
                cached_pks = self.get_pks(portal_id=portal_id)
                slugs = filter(None, (cached_pks.get(pk, []) for pk in pks))
                if slugs:
                    return self.get_cached(slugs=slugs, portal_id=portal_id)
                return []  # We rely on the slug and id maps being up to date
        return []
    
    
    def get_pks(self, portal_id=None, force=True):
        """
        Gets the (pks -> slug) :class:`OrderedDict` from the cache or, if the can has not been filled,
        gets the pks and slugs from the database and fills the cache.
        
        @param force: if True, forces a rebuild of the pk and slug cache for this group type
        :returns: A :class:`OrderedDict` with a `pk => slug` mapping of all
            groups
        """
        if portal_id is None:
            portal_id = CosinnusPortal.get_current().id
            
        pks = cache.get(self._IDEAS_PK_TO_SLUG_CACHE_KEY % (portal_id))
        if force or pks is None:
            # we can only find groups via this function that are in the same portal we run in
            pks = OrderedDict(self.filter(portal__id=portal_id, is_active=True).values_list('id', 'slug').all())
            cache.set(self._IDEAS_PK_TO_SLUG_CACHE_KEY % (portal_id), pks,
                settings.COSINNUS_IDEA_CACHE_TIMEOUT)
        return pks

    
    def all_in_portal(self):
        """ Returns all groups within the current portal only """
        return self.active().filter(portal=CosinnusPortal.get_current())
    
    def public(self):
        """ Returns active, public Ideas """
        qs = self.active()
        return qs.filter(public=True)
    
    def active(self):
        """ Returns active Ideas """
        qs = qs = self.get_queryset()
        return qs.filter(is_active=True)
    
    def get_by_shortid(self, shortid):
        """ Gets an idea from a string id in the form of `"%(portal)d.%(type)s.%(slug)s"`. 
            Returns None if not found. """
        portal, __, slug = shortid.split('.')
        portal = int(portal)
        try:
            qs = self.get_queryset().filter(portal_id=portal, slug=slug)
            return qs[0]
        except self.model.DoesNotExist:
            return None
        
    
    def get_queryset(self):
        return CosinnusIdeaQS(self.model, using=self._db).select_related('portal')
    


@python_2_unicode_compatible
class CosinnusIdea(IndexingUtilsMixin, models.Model):
    # don't worry, the default Portal with id 1 is created in a datamigration
    # there was no other way to generate completely runnable migrations 
    # (with a get_default function, or any other way)
    portal = models.ForeignKey(CosinnusPortal, verbose_name=_('Portal'), related_name='ideas', 
        null=False, blank=False, default=1) # port_id 1 is created in a datamigration!
    
    title = models.CharField(_('Title'), max_length=250) # removed validators=[group_name_validator])
    slug = models.SlugField(_('Slug'), 
        help_text=_('Be extremely careful when changing this slug manually! There can be many side-effects (redirects breaking e.g.)!'), 
        max_length=50)
    created = models.DateTimeField(verbose_name=_('Created'), editable=False, auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=_('Creator'),
        on_delete=models.CASCADE,
        null=True,
        related_name='ideas')
    
    description = models.TextField(verbose_name=_('Short Description'),
         help_text=_('Short Description. Internal, will not be shown publicly.'), blank=True)
    
    image = models.ImageField(_("Image"), 
        help_text='Shown as large banner image',
        null=True, blank=True,
        upload_to=get_idea_image_filename,
        max_length=250)
    
    public = models.BooleanField(_('Public'), default=False)
    media_tag = models.OneToOneField(settings.COSINNUS_TAG_OBJECT_MODEL,
        blank=True, null=True, editable=False, on_delete=models.SET_NULL)
    is_active = models.BooleanField(_('Is active'),
        help_text='If an idea is not active, it counts as non-existent for all purposes and views on the website.',
        default=True)
    
    created_groups = models.ManyToManyField(settings.COSINNUS_GROUP_OBJECT_MODEL, 
        verbose_name=_('Created Projects'),
        blank=True, null=True, related_name='+')
    
    
    likes = GenericRelation(LikeObject)
    
    objects = IdeaManager()
    
    
    class Meta:
        ordering = ('created',)
        verbose_name = _('Cosinnus Idea')
        verbose_name_plural = _('Cosinnus Ideas')
        unique_together = ('slug', 'portal', )

    def __init__(self, *args, **kwargs):
        super(CosinnusIdea, self).__init__(*args, **kwargs)
        self._portal_id = self.portal_id
        self._slug = self.slug

    def __str__(self):
        return '%s (Portal %d)' % (self.title, self.portal_id)
    
    def save(self, *args, **kwargs):
        created = bool(self.pk is None)
        slugs = [self.slug] if self.slug else []
        self.title = clean_single_line_text(self.title)
        
        current_portal = self.portal or CosinnusPortal.get_current()
        unique_aware_slugify(self, 'title', 'slug', portal_id=current_portal)
        
        if not self.slug:
            raise ValidationError(_('Slug must not be empty.'))
        slugs.append(self.slug)
        # sanity check for missing media_tag:
        if not self.media_tag:
            from cosinnus.models.tagged import get_tag_object_model
            media_tag = get_tag_object_model()._default_manager.create()
            self.media_tag = media_tag
        
        if created and not self.portal:
            # set portal to current
            self.portal = CosinnusPortal.get_current()
        
        super(CosinnusIdea, self).save(*args, **kwargs)
        
        self._clear_cache(slugs=slugs)
        # force rebuild the pk --> slug cache. otherwise when we query that, this group might not be in it
        self.__class__.objects.get_pks(force=True)
        
        self._portal_id = self.portal_id
        self._slug = self.slug
        
        if created:
            # send creation signal
            signals.idea_object_ceated.send(sender=self, group=self)
    
    def delete(self, *args, **kwargs):
        self._clear_cache(slug=self.slug)
        super(CosinnusIdea, self).delete(*args, **kwargs)

    @classmethod
    def _clear_cache(self, slug=None, slugs=None):
        slugs = set([s for s in slugs]) if slugs else set()
        if slug: slugs.add(slug)
        keys = [
            self.objects._IDEAS_PK_TO_SLUG_CACHE_KEY % (CosinnusPortal.get_current().id),
        ]
        if slugs:
            keys.extend([self.objects._IDEAS_SLUG_CACHE_KEY % (CosinnusPortal.get_current().id, s) for s in slugs])
        cache.delete_many(keys)
        
    def clear_cache(self):
        self._clear_cache(slug=self.slug)
        
    @property
    def image_url(self):
        return self.image.url if self.image else None
    
    def get_image_thumbnail(self, size=(500, 275)):
        return image_thumbnail(self.image, size)

    def get_image_thumbnail_url(self, size=(500, 275)):
        return image_thumbnail_url(self.image, size)
    
    def get_image_field_for_background(self):
        return self.image
    
    def is_foreign_portal(self):
        return CosinnusPortal.get_current().id != self.portal_id
    
    def media_tag_object(self):
        key = '_media_tag_cache'
        if not hasattr(self, key):
            setattr(self, key, self.media_tag)
        return getattr(self, key)
    
    def get_absolute_url(self):
        item_id = '%d.ideas.%s' % (self.portal_id, self.slug)
        return get_domain_for_portal(self.portal) + reverse('cosinnus:map') + '?item=' + item_id

    