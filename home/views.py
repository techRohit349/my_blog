from django.shortcuts import render , HttpResponse , redirect
from home.models import Contact
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout

# Create your views here.
def home(request):
    return render(request , 'home/index.html')
    #return HttpResponse("Welcome to our home page")

def about(request):
    return render(request , 'home/about.html')
    #return HttpResponse("Welcome to our about page")

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name' , default='')
        phone=request.POST.get('mobile' , default='')
        gmail=request.POST.get('gmail' , default='')
        content=request.POST.get('desc' , default='')
        #print(name , phone , gmail , content )
        if len(name)<3 or len(phone)<10 or len(gmail)<5 or len(content)<5 :
            messages.error(request , "Please fill contact form correctly!")
        else :   
            contact = Contact(name=name , phone=phone , gmail=gmail , content=content)
            contact.save()
            messages.success(request , "Message sent successfully ! We will shortly contact you !")

    return render(request , 'home/contact.html')
    #return HttpResponse("Welcome to our contact page")

def search(request):
    query = request.GET['search_item']
    print(query)
    if(query == ""):
        messages.warning(request , "Enter some characters !")
        result = Post.objects.none()
        
    elif(len(query)> 80 ):
        result = Post.objects.none()
        messages.warning(request , "Query must be less than 80 characters!")
        query = "Your query is too long..."
    
    else:
        result1 = Post.objects.filter(title__icontains=query)
        result2 = Post.objects.filter(content__icontains=query)
        result = result1.union(result2)
        if(result.count() == 0):
            messages.warning(request , "Please refine your query!")
    #result = Post.objects.all()
    
    return render(request , "home/search.html" , {"result":result , "query":query})
#    return HttpResponse("This is search page")

def handlesignup(request):
    if request.method == 'POST' :
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        user = request.POST['user']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print(lname ,fname , email , user , pass1 , pass2)

        # validation for signup
        if len(user) > 25:
            messages.warning(request , "Username must be less than 25 character!")
            return redirect('Home')
        if not user.isalnum():
            messages.warning(request , "Username must be alphanumeric!")
            return redirect('Home')
        if pass1 != pass2 :
            messages.warning(request , "Password do not match each other!")
            return redirect('Home')
        if len(pass1) < 6 :
            messages.warning(request , "Password is too sort . Password should be grater than 6 character!")
            return redirect('Home')
        # create user
        myuser = User.objects.create_user(user , email , pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request , "You have sign up successfully to our blog!")
        return redirect('Home')
    else:
        return HttpResponse(" Error - 404")


def handlelogin(request):
    if request.method == 'POST' :
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(username = username , password=password)
        if user is not None :
            login(request , user)
            messages.success(request , "You have login successfully!")
            return redirect("Home")
        else :
            messages.warning(request , "Invalid credentials . Please make sure fill correct information!")
            return redirect("Home")
    
    return HttpResponse("Page not found")

def handlelogout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request , "You have logout successfully")
        return redirect("Home")
    else:
        return HttpResponse("Error - 404 page not found")

def handlePass(request):
    return render(request , 'home/reset_password.html')

def handleUpdatePass(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # print(username , email , pass1 , pass2)
        # form validation
        if pass1 != pass2 :
            messages.warning(request , "Password do not match each other!")
            return redirect('Home')
        if len(pass1) < 6 :
            messages.warning(request , "Password is too sort . Password should be grater than 6 character!")
            return redirect('Home')
        
        try:
            user = User.objects.get(username = username , email = email)
            if user is not None:
                user.set_password(pass1)
                user.save()
                messages.success(request , "Possward reset succcessfully")
            else:
                messages.error(request , "Username or Email does not exists!")
        except User.DoesNotExist as e :
            messages.error(request , "Username or Email does not exists!")
            print(e)
        return redirect("Home")
    else:
        return HttpResponse("Error 404 page not found")