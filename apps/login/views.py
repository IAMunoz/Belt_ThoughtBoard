from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')
    
def register_user(request):
    if request.method == 'GET':
        #Si funciona, debe mostrar mensaje de registro existoso, y puede ir a la App
        if request.session['logged_id']:
            user = request.session['logged_user']
            return render(request, 'index.html', {'user_reg': user})
        else: return redirect("/") 
    else:
        errors = User.objects.basic_validator(request.POST)
        if len(errors) >0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print (pw_hash)
        
        user = User.objects.create(
            name = request.POST['name'], 
            email = request.POST['email'], 
            password = pw_hash.decode(), 
            lastname = request.POST['lastname']
            )
        request.session['logged_user'] = user.name, user.lastname
        request.session['logged_id'] = user.id
        # request.session['logged_user'] = 'Michelle'
        # request.session['logged_id'] = 1
        return redirect("/register") 

def login_user(request):
    if request.method == 'GET':
        return redirect('/thoughts')
    else:
        #para un request post realiza validación de datos de usuario registrado y lo registra en el session
        pw = request.POST['password']
        results = User.objects.filter(email=request.POST['email'])
        print('user: ' , results)
        # Revisa si el usuario existe results es true
        if results:
            username = results[0].email
            print('logged_email: ', username)
            #Revisa si el pw corresponde al usuario
            if bcrypt.checkpw(pw.encode(), results[0].password.encode()):
                request.session['logged_user'] = results[0].name, results[0].lastname
                request.session['logged_id'] = results[0].id    
                return redirect("/login")
            else:
                messages.error(request, f"Contraseña no corresponde al usuario: {username}")
                return redirect('/')
        else:
            print('Usuario no encontrado')
            messages.error(request, 'Usuario no encontrado')
            return redirect('/')

        # request.session['logged_user'] = 'Michelle'
        # request.session['logged_id'] = 1
        # return redirect('/login')

def success(request):
    return render(request, 'success.html')

def logout(request):
    try:
        del request.session['logged_user']
        del request.session['logged_id']
        messages.error(request, '')
    except:
        print('Error')
    return redirect("/")   