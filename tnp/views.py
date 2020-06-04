from django.shortcuts import render

def error_404(request,exception):
    t=exception
    k = type(t)
    if k.__name__ == 'Resolver404':
        exception='Requested page not found.'
    print(k.__name__)
    return render(request,'404.html',{'exception':exception})

def error_500(request):
    return render(request,'500.html')