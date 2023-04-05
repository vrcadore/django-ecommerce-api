from typing import Any

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html


class CustomAdminFileWidget(AdminFileWidget):
    """
    Custom AdminFileWidget to display image preview
    """

    def render(
        self, name: str, value: Any, attrs: Any = None, renderer: Any = None
    ) -> str:
        """
        Render the widget as an HTML string.
        """
        result = []
        if hasattr(value, "url"):
            result.append(
                f"""<a href="{value.url}" target="_blank">
                      <img
                        src="{value.url}" alt="{value}"
                        width="100" height="100"
                        style="object-fit: cover;"
                      />
                    </a>"""
            )
        result.append(super().render(name, value, attrs, renderer))
        return format_html("".join(result))
