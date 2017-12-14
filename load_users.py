import os,sys
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE","winerama.settings")

import django
django.setup()

from django.contrib.auth.models import User

def save_user(user_row):
  userin = User()
  userin.id = user_row[0]
  userin.username = user_row[1]
  userin.save()

if __name__ == "__main__":

  if len(sys.argv) == 2:
    print("Reading from the file "+str(sys.argv[1]))
    users_df = pd.read_csv(sys.argv[1])
    print(users_df)

    users_df.apply(save_user,axis=1)
    print("There are {} users".format(User.objects.count()))

  else:
    print("Theres an error in the input ")

