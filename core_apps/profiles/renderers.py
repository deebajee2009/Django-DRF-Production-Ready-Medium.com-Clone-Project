"""
Profile app renderer.
"""

import json

from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    """
    renderer
    """

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renderer
        """
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profile": data})


class ProfilesJSONRenderer(JSONRenderer):
    """
    renderer
    """

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renderer
        """
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfilesJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profiles": data})
