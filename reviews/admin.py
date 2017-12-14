from django.contrib import admin

from .models import wine,review,Cluster

class ReviewAdmin(admin.ModelAdmin):
  model = review
  list_display = ('wine','rating','user_name','comment','pub_date')
  list_filter = ('pub_date','user_name')
  search_fields = ['comment']

class ClusterAdmin(admin.ModelAdmin):
  model = Cluster
  list_display = ['name','get_user']

admin.site.register(wine)
admin.site.register(review,ReviewAdmin)
admin.site.register(Cluster,ClusterAdmin)

