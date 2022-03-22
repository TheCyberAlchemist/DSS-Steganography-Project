from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class keys(models.Model):
	user_id = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
	public_key = models.BinaryField(editable=True)
	private_key = models.BinaryField(editable=True)
	def __str__(self):
		return self.user_id.username + " -- " + self.public_key.__str__()