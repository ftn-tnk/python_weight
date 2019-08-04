from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views import generic

import pytz
import datetime
import calendar
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('tkagg')

from django.views.generic import CreateView, TemplateView
from chartjs.views.lines import BaseLineChartView

from .models import Weightapp
from .forms import RecordingForm, LoginForm

# Create your views here.
class Index(generic.TemplateView):
    template_name = 'weightapp/index.html'

class Login(LoginView):
    form_class = LoginForm
    template_name = 'weightapp/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'weightapp/index.html'

TODAY = str(timezone.now()).split('-')

def index(request, year=TODAY[0], month=TODAY[1]):
    weight = Weightapp.objects.filter(use_date__month=month).order_by('use_date')
    for w in weight:
        date = str(w.use_date).split(' ')[0]
        w.use_date = '/'.join(date.split('-')[1:3])

    form = RecordingForm()
    context = {
        'year' : year,
        'month' : month,
        'weight' : weight,
        'form' : form,
    }

    draw_graph(year, month)

    if request.method == 'POST':
        data = request.POST
        use_date = data['use_date']
        weight = data['weight']
        bodyfat = data['bodyfat']
        detail = data['detail']
        category = data['category']

        use_date = timezone.datetime.strptime(use_date, "%Y/%m/%d")
        sydney_timezone = pytz.timezone('Australia/Sydney')
        use_date = sydney_timezone.localize(use_date)
        use_date += datetime.timedelta(hours=10)

        Weightapp.objects.create(
                    use_date = use_date,
                    weight = int(weight),
                    bodyfat = int(bodyfat),
                    detail = detail,
        )
        return redirect(to='/weightapp/{}/{}'.format(year, month))

    return render(request, 'weightapp/index.html', context)

def draw_graph(year, month):
    weight = Weightapp.objects.filter(use_date__year=year, use_date__month=month).order_by('use_date')

    last_day = calendar.monthrange(int(year), int(month))[1] + 1
    day = [i for i in range(1, last_day)]
    Myweight = [0 for i in range(len(day))]
    for w in weight:
        key = str(w.use_date).split('-')[2]
        Myweight[int(str(key).split(' ')[0])-1] += int(w.weight)
        #Myweight[int(14)-1] += int(w.weight)
        Myweight = [float('nan') if x == 0 else x for x in Myweight]
    plt.figure()
    plt.plot(day, Myweight, color='#00bfff')
    plt.grid(True)
    plt.xlim([0, 31])
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Weight', fontsize=16)
    plt.savefig('weightapp/static/images/bar_{}_{}.svg'.format(year, month), transparent=True)

    return None

class CreateView(CreateView):
    model = Weightapp
    fields = ('use_date', 'weight', 'bodyfat', 'category', 'detail')

class LineChartJSONView(BaseLineChartView):
    def get_data(self):
        weight = Weightapp.objects.filter(use_date__year=year, use_date__month=month).order_by('use_date')
        return weight

    def get_labels(self):
        last_day = calendar.monthrange(int(2019), int(7))[1] + 1
        day = [i for i in range(1, last_day)]
        return day

line_chart = TemplateView.as_view(template_name='weightapp/line_chart.html')
line_chart_json = LineChartJSONView.as_view()
