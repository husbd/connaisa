from django.shortcuts import render, get_object_or_404
from connaisaV0.models import user, post, history, review

#global
clist = ['Art', 'Sports', 'Language', 'Academic', 'Living', 'Other']
llist = ['Beginner', 'Amateur', 'Intermediate', 'Proficient', 'Expert']

def index(request):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
    search_content = request.GET
    if len(search_content) > 0:
        search_content = search_content["search"]
        search_posts = post.objects.filter(name__icontains=search_content) |\
                    post.objects.filter(description__icontains=search_content)
        #filter out deleted posts
        search_posts = search_posts.filter(visible=True)
        post_count = len(search_posts)
        return render(request, "search.html", {'message': 'Search page', 'user':user_,
               'search_content': search_content, "search_posts": search_posts, 'post_count':post_count})
    content = {'message': 'this is the index page.(Under construction)', 'user':user_}
    return render(request, "index.html", content)

def signup(request):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
    if request.method == 'POST':
        info = request.POST
        username = info['username']
        email = info['email']
        pw = info['password']
        secureQA = info['secureQ'] + '@@' + info['secureA']
        if username == "" or email=="" or pw=="" or info['secureA']=="":
            return render(request, "signup.html", {'message': 'You have incompleted fields!', 'user':user_})
        try:
            user.objects.create(username=username, email=email, pw=pw, secure_qa=secureQA)
        except:
            return render(request, "index.html", {'message': 'Sign up failed! Try again or contact us.', 'user':user_})
        return render(request, "index.html", {'message':'Sign up successfully!', 'user':user_})
    else:
        return render(request, "signup.html", {})

def login(request):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
    if request.method == 'POST':
        info = request.POST
        email = info['email']
        pw = info['password']
        if email == '' or pw == '':
            return render(request, "login.html", {'message': 'You have incompleted fields!'})
        else:
            try:
                user_ = user.objects.get(email=email)
            except:
                return render(request, "login.html", {'message': 'Email address not exist! Try again or sign up.', 'user':user_})
            pw_ = user_.pw
            if pw_ != pw:
                return render(request, "login.html", {'message': 'Incorrect password!', 'user':user_})
            else:
                logedin = {'userid': user_.id, 'username': user_.username}
                request.session['logedin'] = logedin
                return render(request, "index.html", {'message': 'login successfully!', 'user':logedin})
    return render(request, "login.html", {})

def logout(request):
    request.session['logedin'] = None
    return render(request, "index.html", {'message': 'log out successfully!', 'user': None})

def accounthome(request):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
        return render(request, "index.html", {'message': 'You need to log in first!', 'user': user_})
    try:
        user_instance = user.objects.get(id=user_['userid'])
    except:
        return render(request, "index.html", {'message': 'User does not exist! Contact us asap!', 'user': user_})

    message_ = ''
    is_profile_complete = True
    has_description = True

    # updata description
    if request.method == 'POST':
        description_ = request.POST['description']
        if description_:
            if description_.strip()!='':
                user_instance.description = description_
                user_instance.save()
                message_ = "Description updated."
    # get profile and put in a dict
    user_profile = {}
    user_profile['username'] = user_instance.username
    user_profile['email'] = user_instance.email
    user_profile['photo'] = user_instance.photo
    user_profile['description'] = user_instance.description
    if user_instance.description == '':
        has_description = False
    else:
        user_profile['description'] = user_instance.description
    if not isProfileComplete(user_instance):
        is_profile_complete = False
    # get user's posts
    posts_ = post.objects.filter(poster=user_instance, visible=True)
    #posts_ = posts_[:3]
    posts_dict_list = []
    for p in posts_:
        post_dict={}
        post_dict['id'] = p.id
        post_dict['name'] = p.name
        post_dict['category'] = clist[p.category]
        post_dict['level'] = llist[p.level]
        posts_dict_list.append(post_dict)
    return render(request, "account.html", {'message': message_, 'user': user_, 'user_profile': user_profile,
                                            "is_profile_complete":is_profile_complete, "has_description":has_description,
                                            "posts":posts_dict_list})

def editProfile(request):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
        return render(request, "index.html", {'message': 'You need to log in first!', 'user': user_})
    message = ''
    try:
        user_instance = user.objects.get(id=user_['userid'])
    except:
        return render(request, "index.html", {'message': 'User does not exist! Contact us asap!', 'user': user_})
    # if new profile is submitted
    if request.method == "POST":
        new_profile = request.POST
        # check & save new profile
        if new_profile['name'] and new_profile['name'] != user_instance.name:
            user_instance.name = new_profile['name']
        if new_profile['gender'] and int(new_profile['gender']) != user_instance.gender:
            user_instance.gender = int(new_profile['gender'])
        if new_profile['date_of_birth'] and new_profile['date_of_birth'] != user_instance.date_of_birth:
            user_instance.date_of_birth = new_profile['date_of_birth']
        if new_profile['address'] and new_profile['address'] != user_instance.address:
            user_instance.address = new_profile['address']
        if new_profile['number'] and new_profile['number'] != user_instance.number:
            user_instance.number = new_profile['number']
        # photo processing
        if request.FILES.get('photo'):
            user_instance.photo = request.FILES.get('photo')
        user_instance.save()
        message = 'Profile saved successfully!'

    user_profile = {}
    user_profile['username'] = user_instance.username
    user_profile['email'] = user_instance.email
    user_profile['name'] = user_instance.name
    user_profile['gender'] = user_instance.gender
    user_profile['dateofbirth'] = user_instance.date_of_birth
    user_profile['address'] = user_instance.address
    user_profile['number'] = user_instance.number
    user_profile['photo'] = user_instance.photo
    return render(request, "editProfile.html", {'message': message, 'user': user_, 'user_profile':user_profile})

def newPost(request):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
        return render(request, "index.html", {'message': 'You need to log in first!', 'user': user_})
    try:
        user_instance = user.objects.get(id=user_['userid'])
    except:
        return render(request, "index.html", {'message': 'User does not exist! Contact us asap!', 'user': user_})
    message = ''
    if request.method == "POST":
        post_info = request.POST
        post_name_ = post_info['postname']
        category_ = int(post_info['category'])
        level_ = int(post_info['level'])
        description_ = post_info['description']
        post.objects.create(name=post_name_, category=category_, level=level_, poster=user_instance, description=description_)
        message = 'Post created successfully!'
    user_profile = {}
    user_profile['username'] = user_instance.username
    user_profile['email'] = user_instance.email
    user_profile['photo'] = user_instance.photo
    post_info = {}
    post_info['postname'] = ''
    post_info['category'] = 0
    post_info['level'] = 0
    post_info['description'] = ''
    post_info['newpost'] = True
    return render(request, "editPost.html", {'message': message, 'user': user_, 'user_profile': user_profile,
                                             'post_info': post_info})

def viewPost(request, post_id):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
    # post_ = post.objects.get(id=post_id)
    post_ = get_object_or_404(post, id=post_id)
    editable = False
    if user_:
        try:
            user_instance = user.objects.get(id=user_['userid'])
        except:
            return render(request, "index.html", {'message': 'User does not exist! Contact us asap!', 'user': user_})
        if user_instance.id == post_.poster.id:
            editable = True
    post_info = {}
    post_info['id'] = post_id
    post_info['postname'] = post_.name
    post_info['category'] = clist[post_.category]
    post_info['poster_id'] = post_.poster.id
    post_info['poster_name'] = post_.poster.username
    post_info['poster_photo'] = post_.poster.photo
    post_info['level'] = llist[post_.level]
    post_info['active'] = post_.active
    if post_.description=='':
        post_info['description'] = 'The poster does not have any description yet.'
    else:
        post_info['description'] = post_.description
    return render(request, "post.html", {'message': '', 'user': user_, 'post_info': post_info,
                                            "editable":editable})

def editPost(request, post_id):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
        return render(request, "index.html", {'message': 'You need to log in first!', 'user': user_})
    try:
        user_instance = user.objects.get(id=user_['userid'])
    except:
        return render(request, "index.html", {'message': 'User does not exist! Contact us asap!', 'user': user_})
    post_ = get_object_or_404(post, id=post_id)
    if user_instance != post_.poster:
        return render(request, "index.html", {'message': "You are not allowed to edit other's post!", 'user': user_})
    message = ''
    if request.method == "POST":
        new_post_info = request.POST
        print(new_post_info)
        # deletion
        if 'delete' in new_post_info.keys():
            post_.visible = False
            post_.save()
            return render(request, "index.html", {'message': 'Post deleted!', 'user':user_})

        post_.name = new_post_info['postname']
        post_.category = int(new_post_info['category'])
        post_.level = int(new_post_info['level'])
        post_.description = new_post_info['description']
        if 'active' in new_post_info.keys():
            post_.active = True
        else:
            post_.active = False
        post_.save()
        message = 'Post updated successfully!'
    user_profile = {}
    user_profile['username'] = user_instance.username
    user_profile['email'] = user_instance.email
    user_profile['photo'] = user_instance.photo
    post_info = {}
    post_info['id'] = post_id
    post_info['postname'] = post_.name
    post_info['category'] = post_.category
    post_info['level'] = post_.level
    post_info['description'] = post_.description
    post_info['active'] = post_.active
    post_info['newpost'] = False
    return render(request, "editPost.html", {'message': message, 'user': user_, 'user_profile': user_profile,
                                             'post_info': post_info})

def search(request):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
    content = {'message': 'SEARCH PAGE', 'user':user_}
    return render(request, "search.html", content)

def userPage(request, user_id):
    try:
        user_ = request.session['logedin']
    except:
        user_ = None
    try:
        user_instance = get_object_or_404(user, id=user_id)
    except:
        return render(request, "index.html", {'message': 'User does not exist!', 'user': user_})

    message_ = ''
    has_description = True
    print(user_instance.time_created)
    print(type(user_instance.time_created))
    if user_instance.description == '':
        has_description = False

    # get user's posts
    posts_ = post.objects.filter(poster=user_instance, visible=True)
    #posts_ = posts_[:3]
    posts_dict_list = []
    for p in posts_:
        post_dict={}
        post_dict['id'] = p.id
        post_dict['name'] = p.name
        post_dict['category'] = clist[p.category]
        post_dict['level'] = llist[p.level]
        posts_dict_list.append(post_dict)
    return render(request, "userPage.html", {'message': message_, 'user': user_, 'user_profile': user_instance,
                                            "has_description":has_description, "posts":posts_dict_list})

# helper functions
def isProfileComplete(user_instance):
    name_ = user_instance.name
    gender_ = user_instance.gender
    date_of_birth_ = user_instance.date_of_birth
    address_ = user_instance.address
    number_ = user_instance.number
    return name_ and gender_!=0 and date_of_birth_ and address_ and number_

# test
def clean(request):
    cleanDB()
    return render(request, "index.html", {})

def populateDB():
    # add 3 test users
    user.objects.create(username='jack', email='jack@conn.com', pw='jack123', secure_qa='1@@jack')
    user.objects.create(username='tom', email='tom@conn.com', pw='tom123', secure_qa='1@@tom')
    user.objects.create(username='amy', email='amy@conn.com', pw='amy123', secure_qa='1@@amy')
    # add 3 test posts
    post.objects.create(name='japanese study', category=1, level=5, poster=user.objects.get(username='jack'))
    post.objects.create(name='guitar study', category=2, level=1, poster=user.objects.get(username='amy'))
    post.objects.create(name='basketball class', category=3, level=3, poster=user.objects.get(username='tom'))
    # register some classes
    history.objects.create(student=user.objects.get(username='amy'), post=post.objects.get(name='japanese study'))
    history.objects.create(student=user.objects.get(username='tom'), post=post.objects.get(name='japanese study'))
    history.objects.create(student=user.objects.get(username='tom'), post=post.objects.get(name='guitar study'))
    history.objects.create(student=user.objects.get(username='jack'), post=post.objects.get(name='guitar study'))
    history.objects.create(student=user.objects.get(username='jack'), post=post.objects.get(name='basketball class'))
    history.objects.create(student=user.objects.get(username='amy'), post=post.objects.get(name='basketball class'))
    # add some reviews
    review.objects.create(history=history.objects.all()[0], rate=5, content='great teacher')
    review.objects.create(history=history.objects.all()[3], rate=4, content='nice teacher')
    review.objects.create(history=history.objects.all()[5], rate=3, content='good teacher')

def cleanDB():
    user.objects.all().delete()

def main(request):
    populateDB()
    return render(request, "index.html", {})