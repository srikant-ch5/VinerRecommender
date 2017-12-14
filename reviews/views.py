from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import review,wine,Cluster
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from .suggestions import update_clusters

import datetime

def review_list(request):
  latest_review_list = review.objects.order_by('-pub_date')[:9]
  context = {'latest_review_list':latest_review_list}

  return render(request,'reviews/review_list.html',context)

def review_detail(request,review_id):
  review_details = get_object_or_404(review,pk=review_id)

  return render(request,'reviews/review_detail.html',{'review':review_details})

def wine_list(request):
  wine_list = wine.objects.order_by('-name')
  context = {'wine_list':wine_list}

  return render(request,'reviews/wine_list.html',context)

def wine_detail(request,wine_id):
  selected_wine = get_object_or_404(wine,pk=wine_id)
  form = ReviewForm()
  return render(request,'reviews/wine_detail.html',{"wine":selected_wine,'form':form})

@login_required
def add_review(request,wine_id):
  selectWine = get_object_or_404(wine,pk=wine_id)
  form = ReviewForm(request.POST)

  #store in the database
  if form.is_valid():
    rating = form.cleaned_data['rating']
    comment= form.cleaned_data['comment']
    user_name = request.user.username
    selected_review = review()# create a review object and then assign the values then save to db
    selected_review.wine = selectWine
    selected_review.user_name = user_name
    selected_review.comment = comment
    selected_review.rating= rating
    selected_review.pub_date = datetime.datetime.now()
    selected_review.save()
    update_clusters()

    return HttpResponseRedirect(reverse('reviews:wine_detail',args=(selectWine.id,)))#to not able to send same review multiple times

  return render(request,'reviews/wine_detail.html',{'wine':selectWine,'form':form})

def user_review_list(request,username=None):
  if not username:
    username = request.user.username
  latest_review_list = review.objects.filter(user_name=username).order_by('-pub_date')
  context = {'latest_review_list':latest_review_list,'username':username}

  return render(request,'reviews/user_review_list.html',context)

# to return wines list not reviewd by the user
@login_required
def user_recommendation_list(request):
  user_reviews = review.objects.filter(user_name=request.user.username).prefetch_related('wine')#prefetch to reduce the number of queries
  user_reviewed_wines_ids = set(map(lambda x: x.wine.id ,user_reviews))#apply lambda function to get wine ids
  #get usernames for other cluster members
  try:
    user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
  except:#if no clusters have been assigned to user then assign a cluster to user
    update_clusters()
    user_cluster_name = User.objects.get(userername=request.user.username).cluster_set.first().name

  user_cluster_other_users = Cluster.objects.get(name=user_cluster_name).users.exclude(username=request.user.username).all()
  other_users_usernames = set(map(lambda x:x.username ,user_cluster_other_users))

  #get reviews by these selected users exluding those by the requested user
  other_user_reviews = review.objects.filter(user_name__in=other_users_usernames).exclude(wine__id__in=user_reviewed_wines_ids)
  other_user_reviews_wine_id = set(map(lambda x:x.wine.id ,other_user_reviews))
  
  #get wine list by sorted order of rating
  wine_list = list(wine.objects.filter(id__in=other_user_reviews_wine_id))
  #wines_list = wine.objects.exclude(id__in = user_wines_list)# __in to implement sql IN function

  return render(request,'reviews/user_recommendation_list.html',{'username':request.user.username,'wine_list':wine_list})
