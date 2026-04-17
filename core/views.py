from django.shortcuts import render

from django.views.generic import TemplateView

from django.shortcuts import render


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    return render(request, 'errors/500.html', status=500)


class HomeView(TemplateView):
    template_name = 'core/home.html'
