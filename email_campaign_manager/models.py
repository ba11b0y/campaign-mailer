from __future__ import unicode_literals

from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name


class Campaign(models.Model):
    subject = models.CharField(max_length=100)
    pre_text = models.CharField(max_length=100)
    article_url = models.URLField()
    html_content = models.TextField(max_length=1000)
    plain_text = models.TextField(max_length=1000)
    pub_date = models.DateField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
