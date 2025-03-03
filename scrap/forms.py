from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class URLListField(forms.Field):
    """Custom field to validate a list of URLs"""

    def to_python(self, value):
        if not isinstance(value, list):
            raise ValidationError("URLs must be provided as a list.")
        return value

    def validate(self, value):
        super().validate(value)
        url_validator = URLValidator()
        for url in value:
            url_validator(url)  # Validate each URL


class TagListField(forms.Field):
    """Custom field to validate a list of tags"""

    def to_python(self, value):
        if not isinstance(value, list):
            raise ValidationError("Tags must be provided as a list.")
        return value

    def validate(self, value):
        super().validate(value)
        if not all(isinstance(tag, str) for tag in value):
            raise ValidationError("Each tag must be a string.")


class ExtractTagListField(forms.Field):
    """Custom field to validate extract_tags list"""

    ALLOWED_TAGS = {"product_name", "product_description"}

    def to_python(self, value):
        if not isinstance(value, list):
            raise ValidationError("Extract tags must be a list.")
        return value

    def validate(self, value):
        super().validate(value)
        invalid_tags = [tag for tag in value if tag not in self.ALLOWED_TAGS]
        if invalid_tags:
            raise ValidationError(
                f"Invalid extract tags: {', '.join(invalid_tags)}. Allowed: {', '.join(self.ALLOWED_TAGS)}"
            )


class ScrapRequestForm(forms.Form):
    user = forms.IntegerField(required=True)
    urls = URLListField(required=True)
    search_keywords = TagListField(required=True)
    metadata_fields = ExtractTagListField(required=True)


LANGUAGE_CHOICES = [
    ("spanish", "Spanish"),
    ("japanese", "Japanese"),
    ("french", "French"),
    ("german", "German"),
    ("english", "English"),
]


class TranslateContentForm(forms.Form):
    content_id = forms.IntegerField(required=True)
    languages = forms.MultipleChoiceField(
        choices=LANGUAGE_CHOICES,
        required=True,
        error_messages={"required": "At least one language must be selected."},
    )
