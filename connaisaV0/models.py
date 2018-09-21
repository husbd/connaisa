from django.db import models
from django import forms

class user(models.Model):
    #register info
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    time_created = models.DateTimeField(auto_now_add=True)
    pw = models.CharField(max_length=20)
    secure_qa = models.CharField(max_length=53)
    # can be filled afterwards
    name = models.CharField(max_length=50, blank=True)
    gender = models.IntegerField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    number = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='user_photo', blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "User"
        db_table = "user"

    def __str__(self):
        return self.username


class post(models.Model):
    name = models.CharField(max_length=100)
    category = models.IntegerField()
    level = models.IntegerField()
    description = models.TextField(blank=True)
    poster = models.ForeignKey(user, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Post"
        db_table = "post"
        ordering = ('time_created',)

    def __str__(self):
        return self.name

class history(models.Model):
    student = models.ForeignKey(user, on_delete=models.DO_NOTHING, null=True)
    post = models.ForeignKey(post, on_delete=models.DO_NOTHING)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "History"
        db_table = "history"
        ordering = ('time_created',)

    def __str__(self):
        return str(self.id)

class review(models.Model):
    history = models.ForeignKey(history, on_delete=models.CASCADE)
    rate = models.IntegerField()
    content = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Review"
        db_table = "review"
        ordering = ('time_created',)

    def __str__(self):
        return str(self.id)
