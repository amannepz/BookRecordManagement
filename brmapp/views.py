from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from brmapp.forms import NewBookForm,SearchForm
from brmapp import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book
from .serializers import BookSerializer
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
# Model Object - Single Book DATABASES
def Book_detail(request):
    boo=Book.objects.get(id = 2)
    #print(boo)
    serializer = BookSerializer(boo)
    #print(serializer)
    #print(serializer.data)
    #json_data = JSONRenderer().render(serializer.data)
    #print(json_data)
    #return HttpResponse(json_data, content_type='application/json')
    return JsonResponse(serializer.data)

# QuerySet
def Book_list(request):
    boo=Book.objects.all()
    #print(boo)
    serializer = BookSerializer(boo,many=True)
    #print(serializer)
    #print(serializer.data)
    json_data = JSONRenderer().render(serializer.data)
    #print(json_data)
    return HttpResponse(json_data, content_type='application/json')
    #return JsonResponse(serializer.data)

# Create your views here.
def userLogin(request):
    data={}
    if request.method=="POST":
        username=request.POST['username'];
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request, user)
            request.session['username']=username
            return HttpResponseRedirect('/brmapp/view-books/')
        else:
            data['error']="Username or password is incorrect"
            res=render(request,'brmapp/User_login.html',data)
            return res
    else:
        return render(request,'brmapp/User_login.html',data)
def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/brmapp/login/')
@login_required(login_url="/brmapp/login/")
def searchBook(request):
    form=SearchForm()
    res=render(request,'brmapp/search_book.html',{'form':form})
    return res
@login_required(login_url="/brmapp/login/")
def search(request):
    form=SearchForm(request.POST)
    books=models.Book.objects.filter(title=form.data['title'])
    res=render(request,'brmapp/search_book.html',{'form':form,'books':books})
    return res
@login_required(login_url="/brmapp/login/")
def deleteBook(request):
    bookid=request.GET['bookid']
    book=models.Book.objects.filter(id=bookid)
    book.delete()
    return HttpResponseRedirect('brmapp/view-books')
@login_required(login_url="/brmapp/login/")
def editBook(request):
    book=models.Book.objects.get(id=request.GET['bookid'])
    fields={'title':book.title,'price':book.price,'author':book.author,'publisher':book.publisher}
    form=NewBookForm(initial=fields)
    res=render(request,'brmapp/edit_book.html',{'form':form,'book':book})
    return res
@login_required(login_url="/brmapp/login/")
def edit(request):
    if request.method=='POST':
        form=NewBookForm(request.POST)
        book=models.Book()
        book.id=request.POST['bookid']
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()
    return HttpResponseRedirect('brmapp/view-books')
@login_required(login_url="/brmapp/login/")
def viewBooks(request):
    books=models.Book.objects.all()
    res=render(request,'brmapp/view_book.html',{'books':books})
    return res
@login_required(login_url="/brmapp/login/")
def newBook(request):
    form=NewBookForm()
    res=render(request,'brmapp/new_book.html',{'form':form})
    return res
@login_required(login_url="/brmapp/login/")
def add(request):
    if request.method=='POST':
        form=NewBookForm(request.POST)
        book=models.Book()
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()
    s="Record Saved<br><a href='/brmapp/view-books'>View all Books</a>"
    return HttpResponse(s)
@csrf_exempt
def addbook(request):
    if request.method=='POST':
        json_data=request.body
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        serializer = BookSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            res={'msg':'Data Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
            #return JsonResponse(serializer.data)
        else:
            json_data=JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')
            #return JsonResponse(serializer.data)
