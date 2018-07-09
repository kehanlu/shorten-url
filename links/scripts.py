import hashlib
import base64
from links.models import Shortcut


for shortcut in Shortcut.objects.all():
    permanent_url = base64.b64encode(
                    hashlib.md5( (str(shortcut.id) + 'meow').encode('utf-8')).digest(), altchars=b"-_")[:4].decode("utf-8")
    shortcut.permanent_url = permanent_url
    shortcut.save()
