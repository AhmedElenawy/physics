from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include the projectile app's URLs
    # This maps the root URL (http://localhost:8000/) directly to your app
    path('', include('projectile.urls')), 
]