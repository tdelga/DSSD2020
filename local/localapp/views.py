from django.shortcuts import render

def index(request):
	form = PostForm()
    return render(request, 'localapp/index.html', {form:form})
