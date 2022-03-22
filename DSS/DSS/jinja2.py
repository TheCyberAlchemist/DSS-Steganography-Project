from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from django.contrib import messages
def environment(**options):
	env = Environment(**options)
	env.globals.update({
		'static': staticfiles_storage.url,
		'url': reverse,
		'get_messages': messages.get_messages,
	})
	return env
