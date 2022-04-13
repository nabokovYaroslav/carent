from utils.image import EXTENSIONS


extenstions = [ext[0].replace(".", "") for ext in EXTENSIONS]

format_to_http_accepts = {
    "webp": 'image/webp',
}

class ExtensionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META["extension_image"] = get_extenstion(extenstions=extenstions, http_accepts=request.META.get("HTTP_ACCEPT", None))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

def get_extenstion(extenstions, http_accepts):
    if http_accepts is None:
        return None
    formats = http_accepts.split(',')
    for extenstion in extenstions:
        if(format_to_http_accepts[extenstion] in formats):
            return extenstion
    return None
