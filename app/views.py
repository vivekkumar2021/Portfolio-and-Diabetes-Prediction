from django.contrib import auth, messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
import pandas as pd
#import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
#from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from django.utils.datastructures import MultiValueDictKeyError

from .models import predictions


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

# def login(request): #old
# return render(request, 'login.html')

def login(request):
    if request.method == 'POST':

        username = request.POST['your_name']
        password = request.POST['your_pass']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('predict')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


# def register(request): #old.to simply define register page
# return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        re_pass = request.POST['re_pass']

        if password == re_pass:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already available')
                # return redirect('register')
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already Taken')
                # return redirect('register')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'Invalid Password')
            return redirect('register')
            # return render(request, 'index.html')

    else:
        return render(request, 'register.html')


def predict(request):
    return render(request, 'predict.html')

def result(request):
    if(request.method == 'POST'):
        df = pd.read_csv('static/datasets/diabetes.csv')

        x=df.drop("Outcome", axis=1)
        y=df[["Outcome"]]
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)

        reg = LogisticRegression()
        reg.fit(x_train, y_train)

        val1 = float(request.POST['Pregnancies'])
        val2 = float(request.POST['Glucose'])
        val3 = float(request.POST['BloodPressure'])
        val4 = float(request.POST['SkinThickness'])
        val5 = float(request.POST['Insulin'])
        val6 = float(request.POST['BMI'])
        val7 = float(request.POST['DiabetesPedigreeFunction'])
        val8 = float(request.POST['Age'])

        pred = reg.predict([[val1, val2, val3, val4, val5, val6, val7, val8]])

        #target = pred[0]

        #hp = predictions(val1=val1, val2=val2, val3=val3,
                         #val4=val4, val5=val5, val6=val6, val7=val7,
                         #val8=val8)
        #hp.save()

        #if (target == 1):
            #r = "Positive"
        #else:
            #r = "Negative"
        #if (sex == 0):
            #g = "Female"
        #else:
            #g = "Male"
        #v = DoctorReg.objects.all()
        #for i in v:
            #return render(request, 'predict.html',
                          #{'predicted': r, 'age': age, 'gender': g, 'cp': cp, 'chol': chol, 'fbs': fbs,
                           #'thalach': thalach})

        result1 = "predict"
        if pred==[1]:
            result1 = "Positive"
        else:
            result1 = "Negative"

        return render(request, 'predict.html', {"result2":result1})

    return render(request, 'index.html')