from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from wagtailpolls.views.vote import vote
from birdsong import urls as birdsong_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # Pages
    path('profile/', include('profiles.urls')),
    path('quiz/', include('core.urls')),
    path('run/', include('core.urls')),

    # Wagtail
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    # Wiki
    path('notifications/', include('django_nyt.urls')),
    path('wiki/', include('wiki.urls')),

    # Newsletter
    path('mail/', include(birdsong_urls)),

    # Chat
    #path('chat/', include('django_chatter.urls')),

    # Comments
    path('comments/', include('django_comments_xtd.urls')),

    # Vote
    re_path(r'^vote/(?P<poll_pk>.*)/$', vote, name='wagtailpolls_vote'),

    path('', include(wagtail_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if False and settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
