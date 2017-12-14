import os,sys
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE","winerama.settings")

import django
django.setup()

from reviews.models import wine

def save_wines(wine_row):
  winein = wine()
  winein.id = wine_row[0]
  winein.name = wine_row[1]
  winein.save()

if __name__ == "__main__":
  if len(sys.argv) == 2:
    print("reading the wines file ")

    wines_df = pd.read_csv(sys.argv[1])
    print(wines_df)

    wines_df.apply(save_wines,axis=1)

    print("There are {} wines ".format(wine.objects.count()))

  else:
    print("The input is incorrect ")
