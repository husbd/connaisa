from django.db import models
from .models import user,post,history,review

def populateDB():
    # add 3 test users
    models.user.objects.create(username='jack', email='jack@conn.com', pw='jack123', secure_qa='1@@jack')
    models.user.objects.create(username='tom', email='tom@conn.com', pw='tom123', secure_qa='1@@tom')
    models.user.objects.create(username='amy', email='amy@conn.com', pw='amy123', secure_qa='1@@amy')
    # add 3 test posts
    # models.post.objects.create(username='jack', email='jack@conn.com', pw='jack123', secure_qa = '1@@jack')


def cleanDB():
    models.user.objects.all().delete()


if '__name__' == '__main__':
    print(1)