from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from blog.models import Post
import requests
import json

def serving_half_plus_two(request):
    if request.method == 'POST':
        x_pred1 = request.POST['x_pred1']
        x_pred2 = request.POST['x_pred2']
        x_pred3 = request.POST['x_pred3']

        if x_pred1 == '' or x_pred2 == '' or x_pred3 == '' :
            return render(request, 'blog/serving_half_plus_two.html')

        load = {"instances": [float(x_pred1), float(x_pred2), float(x_pred3)]} #[1.0, 2.0, 5.0]
        r = requests.post(' http://localhost:8501/v1/models/half_plus_two:predict', json=load)
        y_pred = json.loads(r.content.decode('utf-8'))
        y_pred = y_pred['predictions']

        context = {
            'result': y_pred,
        }

        return render(request, 'blog/serving_half_plus_two.html', context)

    elif request.method == 'GET':
        return render(request, 'blog/serving_half_plus_two.html')


def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)

def post_add(request):
    if request.method == 'POST':
        User = get_user_model()
        author = User.objects.get(username='joban')
        title = request.POST['title']
        content = request.POST['content']

        if title == '' or content == '':
            context = {
                'title': title,
                'content': content,
            }
            return render(request, 'blog/post_add.html', context)

        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
        )

        try:
            if request.POST['publish'] == 'True':
                post.publish()
        except MultiValueDictKeyError:
            pass

        post_pk = post.pk
        return redirect(post_detail, pk=post_pk)

    elif request.method == 'GET':
        return render(request, 'blog/post_add.html')


def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return render(request, 'blog/post_delete.html')

    elif request.method == 'GET':
        return HttpResponse('잘못된 접근 입니다.')