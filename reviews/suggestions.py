from .models import wine,review,Cluster
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix,csr_matrix
import numpy as np

def update_clusters():
  num_reviews = review.objects.count()
  update_step = ((num_reviews/100)+1)*5

  if num_reviews % update_step == 0:
    # Create a sparse matrix from user reviews
    print("Updating clusters")
    all_user_names = map(lambda x:x.username,User.objects.only('username'))
    all_wine_ids = set(map(lambda x:x.wine.id,review.objects.only('wine')))
    num_users = len(all_user_names)
    ratings_matrix = dok_matrix((num_users,max(all_wine_ids)+1) ,dtype=np.float32)
    for i in range(num_users):
      user_reviews = review.objects.filter(user_name = all_user_names[i])

      for user_review in user_reviews:
        ratings_matrix[i,user_review.wine.id] = user_review.rating

    k = int(num_users/100)+2#dividing into 3 clusters
    kmeans = KMeans(n_clusters+k)
    clustering = kmeans.fit(ratings_m.tocsr())

    #Update the clusters
    Cluster.objects.all().delete()
    new_clusters = {i : Cluster(name=i) for i in range(k)}
    for cluster in new_clusters.values():
      cluster.save()
    for i,cluster_label in enumerate(clustering.labels_):
      new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))

