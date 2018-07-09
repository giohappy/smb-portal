#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# TODO: do we need to add the `status` attribute?
class SmbUser(AbstractUser):
    """Default user model for smb-portal.

    This model's schema cannot be changed at-will since the underlying DB table
    is shared with other smb apps

    """

    nickname = models.CharField(
        _("nickname"),
        max_length=100,
        blank=True,
    )
    language_preference = models.CharField(
        _("language preference"),
        max_length=20,
        choices=((k, v) for k, v in settings.LANGUAGES),
        default="en",
    )

    @property
    def profile(self):
        attibute_names = (
            "enduserprofile",
            "privilegeduserprofile",
            # add more profiles for analysts, prize managers, etc
        )
        for attr in attibute_names:
            try:
                profile = getattr(self, attr)
                break
            except AttributeError:
                pass
        else:
            profile = None
        return profile

    def get_absolute_url(self):
        return reverse("profile:update")


# TODO: Integrate data sharing policies
class EndUserProfile(models.Model):
    MALE_GENDER = "male"
    FEMALE_GENDER = "female"

    AGE_YOUNGER_THAN_NINETEEN = "< 19"
    AGE_BETWEEN_NINETEEN_AND_THIRTY = "19 - 30"
    AGE_BETWEEN_THIRTY_AND_SIXTY_FIVE = "30 - 65"
    AGE_OLDER_THAN_SIXTY_FIVE = "65+"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user")
    )
    date_updated = models.DateTimeField(
        _("date updated"),
        auto_now=True
    )
    gender = models.CharField(
        _("gender"),
        max_length=20,
        blank=False,
        choices=(
            (FEMALE_GENDER, _("female")),
            (MALE_GENDER, _("male")),
        ),
        default=FEMALE_GENDER,
    )
    age = models.CharField(
        _("age"),
        max_length=20,
        blank=False,
        choices=(
            (AGE_YOUNGER_THAN_NINETEEN, _("< 19")),
            (AGE_BETWEEN_NINETEEN_AND_THIRTY, _("19 - 30")),
            (AGE_BETWEEN_THIRTY_AND_SIXTY_FIVE, _("30 - 65")),
            (AGE_OLDER_THAN_SIXTY_FIVE, _("65+")),
        ),
        default=AGE_BETWEEN_NINETEEN_AND_THIRTY
    )
    PHONE_NUMBER_REGEX_VALIDATOR = RegexValidator(
        r"^\+\d{8,15}$",
        message="Use the format +99999999. From 8 to 15 digits allowed"
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=16,
        blank=True,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR]
    )
    bio = models.TextField(
        _("bio"),
        help_text=_("Short user biography"),
        blank=True
    )

    def get_absolute_url(self):
        return self.user.get_absolute_url()


class PrivilegedUserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user")
    )

    def get_absolute_url(self):
        return self.user.get_absolute_url()


class MobilityHabitsSurvey(models.Model):
    FREQUENT_PUBLIC_TRANSPORT_USER = "frequent"
    OCCASIONAL_PUBLIC_TRANSPORT_USER = "occasional"
    RARE_PUBLIC_TRANSPORT_USER = "rare"
    NOT_A_PUBLIC_TRANSPORT_USER = "never"

    FREQUENT_BICYCLE_USER = "frequent"
    OCCASIONAL_BICYCLE_USER = "occasional"
    SEASONAL_BICYCLE_USER = "seasonal"
    RARE_BICYCLE_USER = "rare"
    NOT_A_BICYCLE_USER = "never"

    end_user = models.ForeignKey(
        "EndUserProfile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="mobility_habits_surveys",
        verbose_name=_("end user")
    )
    date_answered = models.DateTimeField(
        _("date answered"),
        auto_now_add=True
    )
    public_transport_usage = models.CharField(
        _("public transport usage"),
        max_length=100,
        choices=(
            (
                FREQUENT_PUBLIC_TRANSPORT_USER,
                _("Habitual (more than 10 travels per month)")
            ),
            (
                OCCASIONAL_PUBLIC_TRANSPORT_USER,
                _("Occasional (once per month)")
            ),
            (
                RARE_PUBLIC_TRANSPORT_USER,
                _("Rare (less than 10 travels per year)")
            ),
            (
                NOT_A_PUBLIC_TRANSPORT_USER,
                _("Never")
            ),
        ),
        default=RARE_PUBLIC_TRANSPORT_USER,
    )
    uses_bike_sharing_services = models.BooleanField(
        _("uses bike sharing services"),
        default=False
    )
    uses_electrical_car_sharing_services = models.BooleanField(
        _("uses electrical car sharing services"),
        default=False
    )
    uses_fuel_car_sharing_services = models.BooleanField(
        _("uses fuel car sharing services"),
        default=False
    )
    bicycle_usage = models.CharField(
        _("bicycle usage"),
        max_length=100,
        choices=(
            (
                FREQUENT_BICYCLE_USER,
                _("Habitual (at least once a week on average)")
            ),
            (
                OCCASIONAL_BICYCLE_USER,
                _("Habitual (at least once a month)")
            ),
            (
                SEASONAL_BICYCLE_USER,
                _("Seasonal (mainly used in the Summer)")
            ),
            (
                RARE_BICYCLE_USER,
                _("Rare (less than once a month)")
            ),
            (
                NOT_A_BICYCLE_USER,
                _("Never use a bicycle to move around in the city")
            ),
        ),
        default=RARE_BICYCLE_USER,
    )

    def get_absolute_url(self):
        return reverse("profile:survey", kwargs={"pk": self.pk})
