from collections.abc import Sequence
from typing import Any

import factory
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


@register
class EmailAddressFactory(DjangoModelFactory):
    email = Faker("email")
    verified = True
    primary = True

    class Meta:
        model = EmailAddress
        django_get_or_create = ["email"]


@register
class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    name = Faker("name")

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

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


register(UserFactory)
register(UserFactory, "user")  # second_author
