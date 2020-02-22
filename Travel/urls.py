from django.conf.urls import url

from Travel import views

app_name='Travel'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    # url(r'^test/$', views.test, name='index'),
    # url(r'^test2/$', views.test2, name='test2'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^foreign/$', views.foreign, name='foreign'),
    url(r'^inland/$', views.inland, name='inland'),
    url(r'^detail(\d+)/', views.detail, name='detail'),
    url(r'^myorder/$', views.myorder, name='myorder'),
    url(r'^custom/$', views.custom, name='custom'),
    url(r'^custom_add/$', views.custom_add, name='custom_add'),
    url(r'^compile(\d+)/', views.compile, name='compile'),

    url(r'^add(\d+)/$', views.add, name='add'),
    url(r'^introduce/$', views.introduce, name='introduce'),
    url(r'^delete(\d+)/$', views.delete, name='delete'),

    url(r'^ask_guestbook/$', views.ask_guestbook, name='ask_guestbook'),
    url(r'^show_guestbook/$', views.show_guestbook, name='show_guestbook'),
    url(r'^answer_guestbook(\d+)/$', views.answer_guestbook, name='answer_guestbook'),

    url(r'^personal/$', views.personal, name='personal'),

    # 国内
    url(r'^city_yn/$', views.city_yn, name='city_yn'),
    url(r'^city_yn2/$', views.city_yn2, name='city_yn2'),
    url(r'^city_yn3/$', views.city_yn3, name='city_yn3'),

    url(r'^city_xzcy/$', views.city_xzcy, name='city_xzcy'),
    url(r'^city_gz/$', views.city_gz, name='city_gz'),
    url(r'^city_db/$', views.city_db, name='city_db'),
    url(r'^city_nmhn/$', views.city_nmhn, name='city_nmhn'),
    url(r'^city_xb/$', views.city_xb, name='city_xb'),
    url(r'^city_xa/$', views.city_xa, name='city_xa'),
    url(r'^city_jzhy/$', views.city_jzhy, name='city_jzhy'),
    url(r'^city_bj/$', views.city_bj, name='city_bj'),
    url(r'^city_sdsx/$', views.city_sdsx, name='city_sdsx'),
    url(r'^city_jxfj/$', views.city_jxfj, name='city_jxfj'),
    url(r'^city_sy/$', views.city_sy, name='city_sy'),
    url(r'^city_hnhb/$', views.city_hbhn, name='city_hnhb'),
    url(r'^city_gd/$', views.city_gd, name='city_gd'),
    url(r'^city_gx/$', views.city_gx, name='city_gx'),
    url(r'^city_xgam/$', views.city_xgam, name='city_xgam'),
    # 国外
    url(r'^country_uk$',views.country_uk,name='country_uk'),
    url(r'^country_france$', views.country_france, name='country_france'),
    url(r'^country_southafrican$', views.country_southafrican, name='country_southafrican'),
    url(r'^country_thai$', views.country_thai, name='country_thai'),
    url(r'^country_singapore$', views.country_singapore, name='country_singapore'),
    url(r'^country_roundtheworld$', views.country_roundtheworld, name='country_roundtheworld'),
    url(r'^country_usa$', views.country_usa, name='country_usa'),
    url(r'^country_hawaiyi$', views.country_hawaiyi, name='country_hawaiyi'),
    url(r'^country_dubai$', views.country_dubai, name='country_dubai'),
    url(r'^country_egypt$', views.country_egypt, name='country_egypt'),
    url(r'^country_dubai$', views.country_dubai, name='country_dubai'),
    url(r'^country_egypt$', views.country_egypt, name='country_egypt'),
    url(r'^country_tokyo$', views.country_tokyo, name='country_tokyo'),
    url(r'^country_japan$', views.country_japan, name='country_japan'),
    url(r'^country_south$', views.country_south, name='country_south'),
    url(r'^country_north$', views.country_north, name='country_north'),
    url(r'^country_australia$', views.country_australia, name='country_australia'),
    url(r'^country_newzealand$', views.country_newzealand, name='country_newzealand'),
    url(r'^country_maldivees$', views.country_maldivees, name='country_maldivees'),
    url(r'^country_fiji$', views.country_fiji, name='country_fiji'),

    # 后台管理
    url(r'^manage_base/$', views.manage_base, name='manage_base'),
    url(r'^manage_index/$', views.manage_index, name='manage_index'),
    url(r'^add_user/', views.add_user, name='add_user'),
    url(r'^show_user/', views.show_user, name='show_user'),
    url(r'^del_user(\d+)/', views.del_user, name='del_user'),
    url(r'^show_citys/', views.show_citys, name='show_citys'),
    url(r'^update(\d+)/', views.update, name='update'),
    url(r'^del_citys(\d+)/', views.del_citys, name='del_citys'),
    url(r'^look_user/', views.look_user, name='look_user'),
    url(r'^del_look(\d+)/', views.del_look, name='del_look'),
    url(r'^look_message/', views.look_message, name='look_message'),
    url(r'^del_message(\d+)/', views.del_message, name='del_message'),

]