from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('ota.views',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^your_uploads/', include('multiuploader.urls')),

    url(r'^$', 'login'),
    url(r'^hello/', 'hello'),
    url(r'^staff/control/', 'admin_control'),
    url(r'^operator/control/', 'operator_control'),

    url(r'^staff/server/', 'admin_set_server'),
    url(r'^staff/pdg/set/', 'admin_set_pdg'),
    url(r'^staff/pdg/edit/', 'admin_edit_pdg'),
    url(r'^staff/pdg/download/', 'download_pdg_file'),
    url(r'^staff/user/add/', 'admin_add_user'),
    url(r'^staff/user/del/', 'admin_del_user'),

    url(r'^operator/files/set/', 'operator_set_files'),
    url(r'^operator/files/del/', 'operator_del_files'),
    url(r'^operator/broadcast/create/', 'operator_create_ts'),
    url(r'^operator/broadcast/init/', 'operator_broadcast'),
    url(r'^operator/broadcast/first/', 'operator_broadcast_first'),

    url(r'^accounts/logout/$', 'logout'),
    url(r'^accounts/login/$', 'login'),
)

