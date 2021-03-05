from django.shortcuts import render , HttpResponse , redirect
from blog.models import Post, Blogcomment
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def blogHome(request):
    allpost = Post.objects.all()
    return render(request , "blog/blogHome.html" ,{"allpost":allpost})
    # return HttpResponse("Welcome to our blog home page")



# sendind comment and replies to the templates
def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments= Blogcomment.objects.filter(post = post , parent = None)
    replies= Blogcomment.objects.filter(post = post).exclude(parent = None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    #print(replyDict)
    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)

# managing comment and replies
def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=Blogcomment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= Blogcomment.objects.get(sno=parentSno)
            comment=Blogcomment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")
