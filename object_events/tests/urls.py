"""
This ``urls.py`` is only used when running the tests via ``runtests.py``.
As you know, every app must be hooked into yout main ``urls.py`` so that
you can actually reach the app's views (provided it has any views, of course).

"""
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^notifications/', include('object_events.urls')),
    url(r'^test/$', TemplateView.as_view(template_name='test_app/tag.html')),
)
