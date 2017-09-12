# -*- coding: utf-8 -*-
"""
Script to generate members from spreadsheet one off.


- Generate `User` (username is `number`, password is phone number (or email))
- Generate `rolodex.Email` and `rolodex.Phone` objects.

"""
import datetime
from .models import Member, Membership
from project.utils import convert_tsv, make_date


# Synchronising scrape from Revel to bookings system.
# To be automated daily.

def create_member(kwargs):

    obj, is_created = Member.objects.update_or_create(
        number=kwargs.pop('number'),
        defaults=kwargs)
    obj.save()
    return obj


def create_membership(kwargs):

    member, is_created = Member.objects.get_or_create(
        number=kwargs.pop('number'))
    obj, is_created = Membership.objects.update_or_create(
        member=member,
        member_type=kwargs.pop('member_type'),
        valid_from=kwargs.pop('valid_from'),
        defaults=kwargs)
    obj.save()
    return obj


def import_members(text):

    data = convert_tsv(text)
    success = []
    for kwargs in data:
        obj = create_member(kwargs=kwargs)
        success.append(obj)
    return success


def import_memberships(text):

    data = convert_tsv(text)
    success = []
    for kwargs in data:
        if kwargs.get('valid_from'):
            kwargs['valid_from'] = make_date(kwargs['valid_from'])
        if kwargs.get('valid_until'):
            kwargs['valid_until'] = make_date(kwargs.pop('valid_until'))
            if not type(kwargs['valid_until']) is datetime.datetime:
                kwargs.pop('valid_until')
            if kwargs['valid_until'] == '':
                kwargs.pop('valid_until')
        obj = create_membership(kwargs=kwargs)
        success.append(obj)
    return success
