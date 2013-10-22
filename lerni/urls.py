from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'lerni.core.views.index', name='core_index'),

    url(r'^login/$', 'lerni.login.views.login', name='login_login'),
    url(r'^logout/$', 'lerni.login.views.logout', name='login_logout'),

    url(r'^administrator/$', 'lerni.core.views.administrator', name='core_administrator'),
    url(r'^teacher/$', 'lerni.core.views.teacher', name='core_teacher'),

    url(r'^chooseUser/$', 'lerni.core.views.choose_user', name='core_choose_user'),

    url(r'^managerTeacher/$', 'lerni.core.views.manager_teacher', name='core_manager_teacher'),
    url(r'^managerTeacher/add/$', 'lerni.core.views.add_teacher', name='core_add_teacher'),
    url(r'^managerTeacher/detail/(?P<teacher_id>\d+)/$', 'lerni.core.views.detail_teacher', name='core_detail_teacher'),
    url(r'^managerTeacher/change/(?P<teacher_id>\d+)/$', 'lerni.core.views.change_teacher', name='core_change_teacher'),
    url(r'^managerTeacher/delete/(?P<teacher_id>\d+)/$', 'lerni.core.views.delete_teacher', name='core_delete_teacher'),

    url(r'^managerStudent/$', 'lerni.core.views.manager_student', name='core_manager_student'),
    url(r'^managerStudent/add/$', 'lerni.core.views.add_student', name='core_add_student'),
    url(r'^managerStudent/detail/(?P<student_id>\d+)/$', 'lerni.core.views.detail_student', name='core_detail_student'),
    url(r'^managerStudent/change/(?P<student_id>\d+)/$', 'lerni.core.views.change_student', name='core_change_student'),
    url(r'^managerStudent/delete/(?P<student_id>\d+)/$', 'lerni.core.views.delete_student', name='core_delete_student'),

    url(r'^domain/$', 'lerni.domain.views.index', name='domain_index'),
    url(r'^domain/topic/$', 'lerni.domain.views.topic', name='domain_topic'),
    url(r'^domain/topic/add/$', 'lerni.domain.views.add_topic', name='domain_add_topic'),
    url(r'^domain/topic/change/(?P<topic_id>\d+)/$', 'lerni.domain.views.change_topic', name='domain_change_topic'),
    url(r'^domain/topic/delete/(?P<topic_id>\d+)/$', 'lerni.domain.views.delete_topic', name='domain_delete_topic'),
    url(r'^domain/topic/(?P<topic_id>\d+)/page/$', 'lerni.domain.views.page', name='domain_page'),
    url(r'^domain/topic/(?P<topic_id>\d+)/page/add/$', 'lerni.domain.views.add_page', name='doamin_add_page'),
    url(r'^domain/topic/page/delete/(?P<page_id>\d+)/$', 'lerni.domain.views.delete_page', name='domain_delete_page'),
    url(r'^domain/topic/page/change/(?P<page_id>\d+)/$', 'lerni.domain.views.change_page', name='doamin_change_page'),

    url(r'^domain/exercise/$', 'lerni.domain.views.exercise', name='domain_exercise'),
    url(r'^domain/exercise/add/$', 'lerni.domain.views.add_exercise', name='domain_add_exercise'),
    url(r'^domain/exercise/detail/(?P<exercise_id>\d+)/$', 'lerni.domain.views.detail_exercise', name='domain_detail_exercise'),
    url(r'^domain/exercise/change/(?P<exercise_id>\d+)/$', 'lerni.domain.views.change_exercise', name='domain_change_exercise'),
    url(r'^domain/exercise/delete/(?P<exercise_id>\d+)/$', 'lerni.domain.views.delete_exercise', name='doamin_delete_exercise'),

    url(r'^student/$', 'lerni.core.views.student', name='core_student'),

    url(r'^classRoom/$', 'lerni.classRoom.views.index', name='classRoom_index'),
    url(r'^classRoom/getPage/(?P<student_id>\d+)/$', 'lerni.classRoom.views.get_page', name='classRoom_get_page'),
    url(r'^classRoom/exercise/$', 'lerni.classRoom.views.exercise', name='classRoom_exercise'),
    url(r'^classRoom/getExercise/$', 'lerni.classRoom.views.get_exercise', name='classRoom_get_exercise'),
    url(r'^classRoom/endExercise/$', 'lerni.classRoom.views.end_exercise', name='classRoom_end_exercise'),

    url(r'^reportCard/$', 'lerni.core.views.report_card', name='core_report_card'),

    url(r'^ckeditor/', include('ckeditor.urls')),

)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
    # staticfiles
    urlpatterns += staticfiles_urlpatterns()