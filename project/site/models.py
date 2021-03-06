# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import querysets
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass


@python_2_unicode_compatible
class Homepage(models.Model):

    title = models.CharField(max_length=200)

    heading = models.CharField(max_length=200, blank=True, default='')

    featured_content = models.TextField(blank=True, default='')

    content = models.TextField(blank=True, default='')

    meta_description = models.CharField(max_length=200, blank=True, default='')

    is_enabled = models.BooleanField('enabled', db_index=True, default=True)

    site = models.OneToOneField('sites.Site', default=get_current_site,
                                on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = querysets.HomepageQuerySet.as_manager()

    class Meta(object):
        ordering = ['title']

    def __str__(self):
        return self.site.name

    def get_absolute_url(self):
        return reverse('site:homepage_detail')

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'
