from collections.abc import Sequence
from typing import Any

import factory
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory, ImageField
from pytest_factoryboy import register

from ecommerce.users.models import UserProfile


@register
class EmailAddressFactory(DjangoModelFactory):
    email = Faker("email")
    verified = True
    primary = True

    class Meta:
        model = EmailAddress
        django_get_or_create = ["email"]


@register
class UserProfileFactory(DjangoModelFactory):
    full_name = Faker("name")
    birth_date = Faker("date")
    avatar = ImageField(color=factory.Faker("hexify", text="#^^^^^^"))
    website = Faker("url")
    phone = Faker("phone_number")
    contact_email = Faker("email")
    country = Faker("country")
    language = Faker("language_code")
    allow_email_contact = Faker("pybool")
    allow_phone_contact = Faker("pybool")
    allow_marketing = Faker("pybool")

    class Meta:
        model = UserProfile
        django_get_or_create = ["user"]


@register
class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    emails = factory.RelatedFactory(
        EmailAddressFactory,
        "user",
        email=factory.SelfAttribute("..email"),
    )

    profile = factory.RelatedFactory(UserProfileFactory, factory_related_name="user")

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


register(UserFactory)
