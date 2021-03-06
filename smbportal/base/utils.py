#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.template.loader import render_to_string

from vehicles import models

logger = logging.getLogger(__name__)


def get_current_bike(view_kwargs, pk_attr_name="pk"):
    try:
        bike = models.Bike.objects.get(pk=view_kwargs.get(pk_attr_name))
    except models.Bike.DoesNotExist:
        bike = None
    return bike


def send_email_to_admins(subject_template, message_template, context=None):
    """Send email to admins

    Admins are all users that have the ``is_superuser`` attribute set to True
    plus all email addresses declared in ``settings.ADMINS`` (if any)

    """

    logger.debug("context: {}".format(context))

    superusers = get_user_model().objects.filter(is_superuser=True)
    destination_addresses = set(superusers.values_list("email", flat=True))
    logger.debug("destination_addresses: {}".format(destination_addresses))
    unique_recipients = set(settings.ADMINS).union(destination_addresses)
    logger.debug("unique_recipients: {}".format(unique_recipients))
    ctx = dict(context) if context is not None else {}
    mail.send_mail(
        subject=render_to_string(subject_template, context=ctx),
        message=render_to_string(message_template, context=ctx),
        from_email=settings.MAIL_SENDER_ADDRESS,
        recipient_list=list(unique_recipients)
    )
