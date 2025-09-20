from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from .evaluation import run_evaluation
import json
from django.http import JsonResponse

def home(request):
    allproduct = Product.objects.all()
    product_per_page = 3
    paginator = Paginator(allproduct, product_per_page)
    page = request.GET.get('page')
    allproduct = paginator.get_page(page)

    context = {'allproduct': allproduct}
    # 1 row 3 cols
    allrow = []
    row = []
    for i, p in enumerate(allproduct):
        if i % 3 == 0:
            if i != 0:
                allrow.append(row)
                row = []
            row.append(p)
        else:
            row.append(p)
    allrow.append(row)
    context['allrow'] = allrow

    return render(request, 'myapp/home.html', context)

def aboutUs(request):
    return render(request, "myapp/aboutus.html")

def contact(request):
    context = {}
    if request.method == "POST":
        data = request.POST.copy()
        topic = data.get("topic")
        email = data.get("email")
        detail = data.get("detail")
        print(topic)
        print(email)
        print(detail)
        print("------------------")

        if topic == "" or email == "" or detail == "":
            context["message"] = "Please, fill in all contact informations"
            return render(request, "myapp/contact.html", context)

        newRecord = ContactList()
        newRecord.topic = topic

        newRecord.email = email
        newRecord.detail = detail
        newRecord.save()

        context["message"] = "The message has been received"
    return render(request, "myapp/contact.html", context)

def userLogin(request):
    context = {}
    if request.method == "POST":
        data = request.POST.copy()
        username = data.get("username")
        password = data.get("password")

        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home-page')
        except:
            context["message"] = "username or password is incorrect"

    return render(request, "myapp/login.html", context)

@login_required(login_url='/login')
def showContact(request):
    allcontact = ContactList.objects.all()

    context = {'contact': allcontact}
    return render(request, 'myapp/showcontact.html', context)

def userRegist(request):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        repassword = data.get('repassword')

        try: 
            User.objects.get(username=username)
            context['message'] = "Username duplicate"
        except:
            newuser = User()
            newuser.username = username
            newuser.first_name = firstname
            newuser.last_name = lastname
            newuser.email = email
            
            if(password == repassword):
                newuser.set_password(password)
                newuser.save()
                newprofile = Profile()
                newprofile.user = User.objects.get(username=username)
                newprofile.save()
                context['message'] = "register complete."
            else:
                context['message'] = "password or re-password is incorrect"
    return render(request, 'myapp/register.html', context)

def userProfile(request):
    context = {}
    userprofile = Profile.objects.get(user=request.user)
    context['profile'] = userprofile
    return render(request, 'myapp/profile.html', context)

def editProfile(request):
    
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        current_user = User.objects.get(id=request.user.id)
        current_user.first_name = firstname
        current_user.last_name = lastname
        current_user.username = username
        current_user.email = email
        current_user.set_password(password)
        current_user.save()

        try:
            user = authenticate(username=current_user.username,
                    password=password)
            login(request, user)
            return redirect('home-page')
        except:
            context['message'] = "edit profile fail"

    return render(request, 'myapp/editprofile.html', context)


def actionPage(request, cid):
    
    context = {}
    contact = ContactList.objects.get(id=cid)
    context['contact'] = contact

    try:
        action = Action.objects.get(ContactList=contact)
        context['action'] = action
    except:
        pass

    if request.method == 'POST':
        data = request.POST.copy()
        actiondetail = data.get('actiondetail')

        if 'save' in data:
            try:
                check = Action.objects.get(ContactList=contact)
                check.actionDetail = actiondetail
                check.save()
                context['action'] =check
            except:
                new = Action()
                new.contactList = contact
                new.actionDetail = actiondetail
                new.save()
        elif 'delete' in data:
            try:
                contact.delete()
                return redirect('showcontact-page')
            except:
                pass
        elif 'complete' in data:
            contact.complete = True
            contact.save()
            return redirect('showcontact-page')

    return render(request, 'myapp/action.html', context)

def addProduct(request):
    if request.method == 'POST':
        data = request.POST.copy()
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        quantity = data.get('quantity')
        instock = data.get('instock')

        new = Product()
        new.title = title
        new.description = description
        new.price = price
        new.quantity = quantity
        
        if instock == 'instock':
            new.instock = True
        else:
            new.instock = False

        if 'picture' in request.FILES:
            file_image = request.FILES['picture']
            file_image_name = file_image.name.replace(' ', '_')  # delete space in file name
            # File system: from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage(location='media/product')
            filename = fs.save(file_image_name, file_image)
            upload_file_url = fs.url(filename)
            print('Picture url:', upload_file_url)
            new.picture = 'product' + upload_file_url[6:]

        if 'specfile' in request.FILES:
            file_specfile = request.FILES['specfile']
            file_specfile_name = file_specfile.name.replace(' ', '_')  # delete space in file name
            # FileSystemStorage: from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage(location='media/specfile')
            filename = fs.save(file_specfile_name, file_specfile)
            upload_file_url = fs.url(filename)
            print('Specfile url:', upload_file_url)
            new.specfile = 'specfile' + upload_file_url[6:]

        new.save()
            
    return render(request, 'myapp/addproduct.html')

def handler404(request, exception):
    return render(request, 'myapp/404errorPage.html')

def prompt_eval(request):
    context = {
        'recent_prompts': Prompt.objects.all()[:10],
        'evaluation_result': None
    }

    if request.method == 'POST':
        data = request.POST.copy()
        prompt_text = data.get('prompt_text', '').strip()
        description = data.get('description', '').strip()

        if prompt_text:
            try:
                evaluation_result = run_evaluation(
                    prompt_text=prompt_text,
                    description=description
                )
                context['evaluation_result'] = evaluation_result
                context['recent_prompts'] = Prompt.objects.all()[:10]
            except Exception as e:
                context['error'] = f"Evaluation failed: {str(e)}"
        else:
            context['error'] = "Please enter a prompt to evaluate"

    return render(request, 'myapp/prompt_eval.html', context)

def prompt_api(request):
    if request.method == 'GET':
        prompts = Prompt.objects.all().order_by('-created_at')
        prompts_data = []
        for prompt in prompts:
            test_cases = TestCase.objects.filter(prompt=prompt)
            results = Result.objects.filter(prompt=prompt)
            avg_score = sum(r.score for r in results) / len(results) if results else 0

            prompts_data.append({
                'id': prompt.id,
                'text': prompt.text,
                'description': prompt.description,
                'version': prompt.version,
                'created_at': prompt.created_at.isoformat(),
                'test_cases_count': test_cases.count(),
                'avg_score': round(avg_score, 2)
            })

        return JsonResponse({'prompts': prompts_data})

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            prompt_id = data.get('id')
            prompt = Prompt.objects.get(id=prompt_id)
            prompt.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def test_case_api(request, prompt_id):
    try:
        prompt = Prompt.objects.get(id=prompt_id)
    except Prompt.DoesNotExist:
        return JsonResponse({'error': 'Prompt not found'}, status=404)

    if request.method == 'GET':
        test_cases = TestCase.objects.filter(prompt=prompt)
        test_cases_data = []

        for tc in test_cases:
            try:
                result = Result.objects.get(test_case=tc)
                score = result.score
                output = result.output
                reasoning = result.reasoning
            except Result.DoesNotExist:
                score = None
                output = ""
                reasoning = ""

            test_cases_data.append({
                'id': tc.id,
                'input': tc.input,
                'expected_type': tc.expected_type,
                'score': score,
                'output': output,
                'reasoning': reasoning
            })

        return JsonResponse({'test_cases': test_cases_data})

    return JsonResponse({'error': 'Method not allowed'}, status=405)