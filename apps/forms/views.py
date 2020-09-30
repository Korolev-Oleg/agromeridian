from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'page': {
            'title': 'Вход в личный кабинет'
        },
        'bd': {}
    }
    return render(request, template_name='templates/index.html', context=context)
