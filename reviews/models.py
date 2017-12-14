from django.db import models
from django.contrib.auth.models import User
import numpy as np

class wine(models.Model):
  name = models.CharField(max_length = 200)

  def average_rating(self):
    all_ratings = list(map(lambda x:x.rating,self.review_set.all()))
    return np.mean(all_ratings)

  def __unicode__(self):
    return self.name

class review(models.Model):
  rating_choices = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

  wine = models.ForeignKey(wine)
  pub_date = models.DateTimeField('date published')
  comment = models.CharField(max_length=200)
  user_name = models.CharField(max_length = 200)
  rating = models.IntegerField(choices = rating_choices)

class Cluster(models.Model):
  name = models.CharField(max_length=250)
  users = models.ManyToManyField(User)

  def get_user(self):
    return "\n".join([u.username for u in self.users.all()])