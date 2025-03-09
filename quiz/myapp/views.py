from myapp.serializers import Serializer
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Tryout, Question
from .forms import TryoutCreationForm, TryoutEditingForm, QuestionCreationForm, DoTryoutForm
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
import datetime

#main menu
def home(request):
    tryoutList = Tryout.objects.all()

    for tryout in tryoutList:
        tryout.tryoutNums = Question.objects.filter(tryout = tryout).count()
        questions = Question.objects.filter(tryout = tryout).order_by("questionNum")
        for i, value in enumerate(questions):
            value.id = i + 1
    
    if request.method == "GET":
        tryoutSearch = request.GET.get("searchBy")
        if (tryoutSearch):
            return render(request, "SearchByName.html", {"tryoutList": tryoutList, "name": tryoutSearch})
    
    return render(request, "Main.html", {"tryoutList": tryoutList})

#display untuk masing-masing tryout
def tryoutDetails(request, tryoutId):
    tryoutViewed = get_object_or_404(Tryout, pk = tryoutId)
    tryoutViewed.tryoutNums = Question.objects.filter(tryout = tryoutViewed).count()
    return render(request, "TryoutDetails.html", {"tryoutViewed": tryoutViewed})

#form pembuatan tryout
def createTryout(request):
    if request.method == "POST":
        creationForm = TryoutCreationForm(request.POST)

        if (creationForm.is_valid()):
            name = creationForm.cleaned_data["tryoutName"]
            desc = creationForm.cleaned_data["tryoutDesc"]
            category = creationForm.cleaned_data["tryoutCategory"]

            #membuat tanggal pembuatan menjadi bentuk string
            dateUnformatted = datetime.date.today().strftime("%d/%m/%Y")
            dateUnformatted = dateUnformatted.split("/")

            month = dateUnformatted[1]
            if (month[0] == 0):
                month = month[1]
            monthToStr = {"01":"January", "02":"Februari", "03":"March", "04":"April", "05":"May", "06":"June", 
                             "07":"July","08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
            monthStr = monthToStr[month]
            
            date = dateUnformatted[0]
            if (date[0] == 0):
                date = date[1]
            
            newDate = str(date) + " " + monthStr + " " + str(dateUnformatted[2])

            newTryout = Tryout(tryoutName = name, tryoutNums = 0, tryoutDesc = desc, tryoutCategory = category, creationDate = newDate, workedOn = False)
            newTryout.save()
            return render(request, "TryoutDetails.html", {"tryoutViewed": newTryout})
    else:
        creationForm = TryoutCreationForm()
    return render(request, "TryoutCreation.html", {"creationForm": creationForm})

#form edit tryout
def editTryout(request, tryoutId):
    if request.method == "POST":
        editorForm = TryoutEditingForm(request.POST)
        tryoutChanged = get_object_or_404(Tryout, pk = tryoutId)

        if (editorForm.is_valid()):
            name = editorForm.cleaned_data["tryoutName"]
            desc = editorForm.cleaned_data["tryoutDesc"]
            category = editorForm.cleaned_data["tryoutCategory"]

            if (name != ""):
                tryoutChanged.tryoutName = name

            if (desc != ""):
                tryoutChanged.tryoutDesc = desc

            if (category != ""):
                tryoutChanged.tryoutCategory = category
            
            tryoutChanged.save()
            return render(request, "TryoutDetails.html", {"tryoutViewed": tryoutChanged})
    else:
        editorForm = TryoutCreationForm()
    return render(request, "TryoutEditor.html", {"editorForm": editorForm})

#menghapus tryout
def deleteTryout(request, tryoutId):
    tryout = get_object_or_404(Tryout, pk = tryoutId)
    tryout.delete()
    tryoutList = Tryout.objects.all()
    return render(request, "Main.html", {"tryoutList": tryoutList})

#display tryout berdasarkan nama
def searchByName(request, name):
    tryoutList = Tryout.objects.all()
    if request.method == "GET":
        tryoutSearch = request.GET.get("searchBy")
        if (tryoutSearch):
            return render(request, "SearchByName.html", {"tryoutList": tryoutList, "name": tryoutSearch})
    return render(request, "SearchByName.html", {"tryoutList": tryoutList, "name": name})

#display tryout berdasarkan kategori
def searchByCategory(request, category):
    tryoutList = Tryout.objects.all()
    if request.method == "GET":
        tryoutSearch = request.GET.get("searchBy")
        if (tryoutSearch):
            return render(request, "SearchByName.html", {"tryoutList": tryoutList, "name": tryoutSearch})
    return render(request, "SearchByCategory.html", {"tryoutList": tryoutList, "category": category})

#display tryout berdasarkan tanggal pembuatan
def searchByDate(request, date):
    tryoutList = Tryout.objects.all()
    if request.method == "GET":
        tryoutSearch = request.GET.get("searchBy")
        if (tryoutSearch):
            return render(request, "SearchByName.html", {"tryoutList": tryoutList, "name": tryoutSearch})
    return render(request, "SearchByDate.html", {"tryoutList": tryoutList, "date": date})

#menampilkan semua soal dari suatu tryout
def questionDetails(request, tryoutId):
    tryout = get_object_or_404(Tryout, pk = tryoutId)
    questions = Question.objects.filter(tryout = tryout).order_by("questionNum")

    #membuat id menjadi berdasarkan nomor urut
    for i, value in enumerate(questions):
        value.id = i + 1

    index = Question.objects.filter(tryout = tryout).count() + 1
    return render(request, "QuestionDetails.html", {"tryout": tryout, "questions": questions, "questionIndex": index})

#form pembuatan soal
def createQuestion(request, tryoutId, questionId):
    if request.method == "POST":
        creationForm = QuestionCreationForm(request.POST)
        tryout = get_object_or_404(Tryout, pk = tryoutId)

        if (creationForm.is_valid()):
            txt = creationForm.cleaned_data["questionTxt"]
            answer = creationForm.cleaned_data["answer"]

            tryout.tryoutNums = Question.objects.filter(tryout = tryout).count()

            question = Question(tryout = tryout, questionTxt = txt, questionNum = (tryout.tryoutNums + 1), answer = answer)
            question.save()

            tryout.tryoutNums = Question.objects.filter(tryout = tryout).count()

            return render(request, "QuestionCreation.html", {"tryoutId": tryoutId, "questionId": (tryout.tryoutNums + 1), "creationForm": QuestionCreationForm()})
    else:
        creationForm = QuestionCreationForm()
    return render(request, "QuestionCreation.html", {"tryoutId": tryoutId, "questionId": questionId, "creationForm": creationForm})

#form edit soal
def editQuestion(request, tryoutId, questionId):
    if request.method == "POST":
        editorForm = QuestionCreationForm(request.POST)
        tryout = get_object_or_404(Tryout, pk = tryoutId)
        question = get_object_or_404(Question, pk = questionId)

        if (editorForm.is_valid()):
            txt = editorForm.cleaned_data["questionTxt"]
            answer = editorForm.cleaned_data["answer"]

            question.questionTxt = txt
            question.answer = answer
            question.save()

            questions = Question.objects.filter(tryout = tryout)
            index = Question.objects.filter(tryout = tryout).count() + 1
            return render(request, "QuestionDetails.html", {"tryout": tryout, "questions": questions, "questionIndex": index})
    else:
        editorForm = QuestionCreationForm()
    return render(request, "QuestionEditor.html", {"tryoutId": tryoutId, "questionId": questionId, "editorForm": editorForm })

#menghapus tryout
def deleteQuestion(request, tryoutId, questionId):
    tryout = get_object_or_404(Tryout, pk = tryoutId)
    questions = Question.objects.filter(tryout = tryout).order_by("questionNum")

    question = get_object_or_404(questions, pk = questionId)
    question.delete()

    #membuat id menjadi berdasarkan nomor urut
    for i, value in enumerate(questions):
        value.id = i + 1

    index = Question.objects.filter(tryout = tryout).count() + 1
    return render(request, "QuestionDetails.html", {"tryout": tryout, "questions": questions, "questionIndex": index})

def doTryout(request, tryoutId):
    tryout = get_object_or_404(Tryout, pk = tryoutId)
    questions = Question.objects.filter(tryout = tryout).order_by("questionNum")
    
    correctAnswers = []
    for question in questions:
        correctAnswers.append(question.answer)

    if request.method == "POST":
        tryoutForm = DoTryoutForm(request.POST)
        userAnswers = []
        for question in questions:
            userAnswer = request.POST.get(str(question.questionNum))
            userAnswers.append(userAnswer)
    
        points = 0
        for i in range(len(userAnswers)):
            if userAnswers[i] == correctAnswers[i]:
                points += 1

        score = (points / Question.objects.filter(tryout = tryout).count()) * 100

        tryout.workedOn = True
        tryout.latestResult = score
        if score > tryout.bestResult:
            tryout.bestResult = score

        tryout.save()

        return render(request, "TryoutDetails.html", {"tryoutViewed": tryout})

    else:
        tryoutForm = DoTryoutForm()
    return render(request, "DoTryout.html", {"tryoutId": tryoutId, "tryoutForm": tryoutForm, "questions": questions})

#untuk Swagger API documentation
class GetMethod(viewsets.ModelViewSet):
    for model in [Tryout, Question]:
        queryset = model.objects.all()
        serializer_class = Serializer

        def list(self, request, model=model, *args, **kwargs):
            data = list(model.objects.all().values())
            return Response(data)

        def retrieve(self, request, model=model, *args, **kwargs):
            data = list(model.objects.filter(id=kwargs['pk']).values())
            return Response(data)

        def create(self, request, *args, **kwargs):
            product_serializer_data = Serializer(data=request.data)
            if product_serializer_data.is_valid():
                product_serializer_data.save()
                status_code = status.HTTP_201_CREATED
                return Response({"message": "Product Added Sucessfully", "status": status_code})
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({"message": "please fill the datails", "status": status_code})

        def destroy(self, request, model=model, *args, **kwargs):
            product_data = model.objects.filter(id=kwargs['pk'])
            if product_data:
                product_data.delete()
                status_code = status.HTTP_201_CREATED
                return Response({"message": "Product delete Sucessfully", "status": status_code})
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({"message": "Product data not found", "status": status_code})

        def update(self, request, model=model, *args, **kwargs):
            product_details = model.objects.get(id=kwargs['pk'])
            product_serializer_data = Serializer(
                product_details, data=request.data, partial=True)
            if product_serializer_data.is_valid():
                product_serializer_data.save()
                status_code = status.HTTP_201_CREATED
                return Response({"message": "Product Update Sucessfully", "status": status_code})
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({"message": "Product data Not found", "status": status_code})