import os,sys
import pandas as pnd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE","winerama.settings")

import django 
django.setup()

from reviews.models import review,wine

def save_review(review_row):
  reviewin = review()
  reviewin.id = review_row[0]
  reviewin.user_name = review_row[1]
  reviewin.wine = wine.objects.get(id = review_row[2])
  reviewin.rating = review_row[3]
  reviewin.pub_date = datetime.datetime.now()
  reviewin.comment = review_row[4]

  reviewin.save()

if __name__ == "__main__":
  if len(sys.argv) == 2:
    reviews_df = pnd.read_csv(sys.argv[1])
    print(reviews_df) 

    reviews_df.apply( save_review , axis = 1)#axis=1 indicates that its row wise

    print("There are {} reviews in DataBase".format(review.objects.count()))
  else:
    print("Please provide appropriate reviews input unable to read")


