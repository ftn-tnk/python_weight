from django.urls import path
from . import views

app_name = 'weightapp'
urlpatterns = [
        path('', views.index, name='index'),
        path('<int:year>/<int:month>', views.index, name='index'),
        path('login/', views.Login.as_view(), name='login'),
        path('logout/', views.Logout.as_view(), name='logout'),
        path('line_chart_json/', views.LineChartJSONView.as_view(), name='line_chart_json'),
]
