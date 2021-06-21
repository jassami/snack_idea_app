from django.db import models

class SnackManager(models.Manager):
    def snack_validator(self, post_data):
        errors={}
        if len(post_data['title'])< 5 or len(post_data['title'])> 100:
            errors['title_input']= "Snack title should be btween 5 and 100 characters."
        if len(post_data['desc'])< 10:
            errors['desc_input']= "Snack description should be at least 10 characters."
        return errors

class Snack(models.Model):
    title= models.CharField(max_length=100)
    desc= models.TextField()
    creator= models.ForeignKey('login_app.User', related_name="snacks", on_delete=models.CASCADE)
    liked_by= models.ManyToManyField('login_app.User', related_name="liked_snacks")
    disliked_by= models.ManyToManyField('login_app.User', related_name="disliked_snacks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects= SnackManager()



