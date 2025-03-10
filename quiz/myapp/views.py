from myapp.serializers import TryoutSerializer, QuestionSerializer
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Tryout, Question
from .forms import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
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
    
    #membuat id menjadi berdasarkan nomor urut
    questions = Question.objects.filter(tryout = tryoutViewed).order_by("questionNum")
    for i, value in enumerate(questions):
        value.id = i + 1
    
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

            #mengambil dan merapikan tanggal
            dateUnformatted = datetime.date.today().strftime("%d/%m/%Y")
            dateUnformatted = dateUnformatted.split("/")

            #membuat bulan menjadi bentuk string
            month = dateUnformatted[1]
            if (month[0] == 0):
                month = month[1]
            monthToStr = {"01":"January", "02":"Februari", "03":"March", "04":"April", "05":"May", "06":"June", 
                             "07":"July","08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
            monthStr = monthToStr[month]
            
            #mengambil tanggal
            date = dateUnformatted[0]
            if (date[0] == 0):
                date = date[1]
            
            #menyusun tanggal lengkap
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

#form pembuatan soal true-false
def createQuestionTF(request, tryoutId, questionId):
    if request.method == "POST":
        creationForm = QuestionCreationForm(request.POST)
        tryout = get_object_or_404(Tryout, pk = tryoutId)

        #mengambil soal dan jawaban
        txt = request.POST["question"]
        answer = request.POST["answer"]

        #membuat soal
        tryout.tryoutNums = Question.objects.filter(tryout = tryout).count()
        question = Question(tryout = tryout, questionTxt = txt, questionNum = (tryout.tryoutNums + 1), questionType = "TF", answer = answer)
        question.save()

        tryout.tryoutNums = Question.objects.filter(tryout = tryout).count()
        return render(request, "QuestionCreationTF.html", {"tryoutId": tryoutId, "questionId": (tryout.tryoutNums + 1), "creationForm": QuestionCreationForm()})
    else:
        creationForm = QuestionCreationForm()
    return render(request, "QuestionCreationTF.html", {"tryoutId": tryoutId, "questionId": questionId, "creationForm": creationForm})

#form pembuatan soal pilihan ganda
def createQuestionMC(request, tryoutId, questionId):
    if request.method == "POST":
        creationForm = QuestionCreationForm(request.POST)
        tryout = get_object_or_404(Tryout, pk = tryoutId)

        #mengambil soal dan pilihan
        txt = request.POST["question"]
        choice1 = request.POST["choice1"]
        choice2 = request.POST["choice2"]
        choice3 = request.POST["choice3"]
        choice4 = request.POST["choice4"]

        #mengambil dan menetapkan jawaban
        answer = request.POST["answer"]
        if (answer == "choice1"):
            answer = choice1
        elif (answer == "choice2"):
            answer = choice2
        elif (answer == "choice3"):
            answer = choice3
        else:
            answer = choice4

        #membuat soal
        tryout.tryoutNums = Question.objects.filter(tryout = tryout).count()
        question = Question(tryout = tryout, questionTxt = txt, questionNum = (tryout.tryoutNums + 1), questionType = "MC", answer = answer, choice1 = choice1, choice2 = choice2, choice3 = choice3, choice4 = choice4)
        question.save()

        tryout.tryoutNums = Question.objects.filter(tryout = tryout).count()
        return render(request, "QuestionCreationTF.html", {"tryoutId": tryoutId, "questionId": (tryout.tryoutNums + 1), "creationForm": QuestionCreationForm()})
    else:
        creationForm = QuestionCreationForm()
    return render(request, "QuestionCreationMC.html", {"tryoutId": tryoutId, "questionId": questionId, "creationForm": creationForm})

#form pembuatan soal esai
def createQuestionEssay(request, tryoutId, questionId):
    if request.method == "POST":
        creationForm = QuestionCreationForm(request.POST)
        tryout = get_object_or_404(Tryout, pk = tryoutId)

        #mengambil soal dan jawaban
        txt = request.POST["question"]
        answer = request.POST["answer"]

        #membuat soal
        tryout.tryoutNums = Question.objects.filter(tryout = tryout).count()
        question = Question(tryout = tryout, questionTxt = txt, questionNum = (tryout.tryoutNums + 1), questionType = "Essay", answer = answer)
        question.save()

        tryout.tryoutNums = Question.objects.filter(tryout = tryout).count()
        return render(request, "QuestionCreationTF.html", {"tryoutId": tryoutId, "questionId": (tryout.tryoutNums + 1), "creationForm": QuestionCreationForm()})
    else:
        creationForm = QuestionCreationForm()
    return render(request, "QuestionCreationEssay.html", {"tryoutId": tryoutId, "questionId": questionId, "creationForm": creationForm})

#form edit soal true-false
def editQuestionTF(request, tryoutId, questionId):
    if request.method == "POST":
        creationForm = QuestionCreationForm(request.POST)
        tryout = get_object_or_404(Tryout, pk = tryoutId)
        questions = Question.objects.filter(tryout = tryout)
        question = get_object_or_404(questions, pk = questionId)

        #mengambil soal dan jawaban
        txt = request.POST["question"]
        answer = request.POST["answer"]

        question.questionTxt = txt
        question.answer = answer
        question.save()

        index = Question.objects.filter(tryout = tryout).count() + 1
        return render(request, "QuestionDetails.html", {"tryout": tryout, "questions": questions, "questionIndex": index})
    else:
        creationForm = QuestionCreationForm()
    return render(request, "QuestionCreationTF.html", {"tryoutId": tryoutId, "questionId": questionId, "creationForm": creationForm})

#form pembuatan soal pilihan ganda
def editQuestionMC(request, tryoutId, questionId):
    if request.method == "POST":
        creationForm = QuestionCreationForm(request.POST)
        tryout = get_object_or_404(Tryout, pk = tryoutId)
        questions = Question.objects.filter(tryout = tryout)
        question = get_object_or_404(questions, pk = questionId)

        #mengambil soal dan pilihan
        txt = request.POST["question"]
        choice1 = request.POST["choice1"]
        choice2 = request.POST["choice2"]
        choice3 = request.POST["choice3"]
        choice4 = request.POST["choice4"]

        #mengambil dan menetapkan jawaban
        answer = request.POST["answer"]
        if (answer == "choice1"):
            answer = choice1
        elif (answer == "choice2"):
            answer = choice2
        elif (answer == "choice3"):
            answer = choice3
        else:
            answer = choice4

        question.questionTxt = txt
        question.choice1 = choice1
        question.choice2 = choice2
        question.choice3 = choice3
        question.choice4 = choice4
        question.answer = answer
        question.save()

        index = Question.objects.filter(tryout = tryout).count() + 1
        return render(request, "QuestionDetails.html", {"tryout": tryout, "questions": questions, "questionIndex": index})
    else:
        creationForm = QuestionCreationForm()
    return render(request, "QuestionCreationMC.html", {"tryoutId": tryoutId, "questionId": questionId, "creationForm": creationForm})

#form pembuatan soal esai
def editQuestionEssay(request, tryoutId, questionId):
    if request.method == "POST":
        creationForm = QuestionCreationForm(request.POST)
        tryout = get_object_or_404(Tryout, pk = tryoutId)
        questions = Question.objects.filter(tryout = tryout)
        question = get_object_or_404(questions, pk = questionId)

        #mengambil soal dan jawaban
        txt = request.POST["question"]
        answer = request.POST["answer"]

        question.questionTxt = txt
        question.answer = answer
        question.save()

        index = Question.objects.filter(tryout = tryout).count() + 1
        return render(request, "QuestionDetails.html", {"tryout": tryout, "questions": questions, "questionIndex": index})
    else:
        creationForm = QuestionCreationForm()
    return render(request, "QuestionCreationEssay.html", {"tryoutId": tryoutId, "questionId": questionId, "creationForm": creationForm})

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

        #mengambil jawaban user
        userAnswers = []
        for question in questions:
            userAnswer = request.POST[str(question.questionNum)]
            userAnswers.append(userAnswer)
    
        #menilai hasil pengerjaan user
        points = 0
        for i in range(len(userAnswers)):
            if userAnswers[i] == correctAnswers[i]:
                points += 1

        score = (points / Question.objects.filter(tryout = tryout).count()) * 100
        score = round(score, 2)

        #menyimpan hasil pengerjaan dan menentukan nilai tertinggi
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
class TryoutListAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all Tryout instances", 
        responses={200: TryoutSerializer(many=True)} 
    )
    def get(self, request):
        models = Tryout.objects.all()  
        serializer = TryoutSerializer(models, many=True)  
        return Response(serializer.data)  

    @swagger_auto_schema(
        operation_description="Create a new Tryout instance",  
        request_body=TryoutSerializer,  
        responses={201: TryoutSerializer, 400: 'Bad Request'}  
    )
    def post(self, request):
        serializer = TryoutSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    @swagger_auto_schema(
        operation_description="Update an existing Question instance", 
        request_body=TryoutSerializer,  
        responses={200: TryoutSerializer, 400: 'Bad Request', 404: 'Not Found'}  
    )
    def put(self, request, pk=None):
        if pk and Tryout.objects.filter(id=int(pk)).exists(): 
            qs = Tryout.objects.get(id=int(pk)) 
            serializer = TryoutSerializer(qs, data=request.data, partial=True) 
            if serializer.is_valid():  
                serializer.save()  
                return Response({
                    'message': 'Successfully updated',  
                    'error': None,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        return Response({
            'message': 'Provide a valid pk',  
            'error': 'Not Found', 
            'data': None
        }, status=status.HTTP_404_NOT_FOUND) 
    
    @swagger_auto_schema(
        operation_description="Delete an existing Question instance", 
        responses={200: 'Deleted successfully', 404: 'Not Found'} 
    )
    def delete(self, request, pk=None):
        if pk and Tryout.objects.filter(id=int(pk)).exists(): 
            qs = Tryout.objects.get(id=int(pk))
            qs.delete()  
            return Response({
                'message': 'Deleted successfully',  
                'error': None,
                'data': None
            }, status=status.HTTP_200_OK) 

        return Response({
            'message': 'Provide a valid pk',  
            'error': 'Not Found', 
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)  
    
class QuestionListAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all Question instances", 
        responses={200: QuestionSerializer(many=True)} 
    )
    def get(self, request):
        models = Question.objects.all()  
        serializer = QuestionSerializer(models, many=True)  
        return Response(serializer.data)  

    @swagger_auto_schema(
        operation_description="Create a new Question instance",  
        request_body=QuestionSerializer,  
        responses={201: QuestionSerializer, 400: 'Bad Request'}  
    )
    def post(self, request):
        serializer = QuestionSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    @swagger_auto_schema(
        operation_description="Update an existing Question instance", 
        request_body=QuestionSerializer,  
        responses={200: QuestionSerializer, 400: 'Bad Request', 404: 'Not Found'}  
    )
    def put(self, request, pk=None):
        if pk and Question.objects.filter(id=int(pk)).exists(): 
            qs = Question.objects.get(id=int(pk)) 
            serializer = QuestionSerializer(qs, data=request.data, partial=True) 
            if serializer.is_valid():  
                serializer.save()  
                return Response({
                    'message': 'Successfully updated',  
                    'error': None,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        return Response({
            'message': 'Provide a valid pk',  
            'error': 'Not Found', 
            'data': None
        }, status=status.HTTP_404_NOT_FOUND) 
    
    @swagger_auto_schema(
        operation_description="Delete an existing Question instance", 
        responses={200: 'Deleted successfully', 404: 'Not Found'} 
    )
    def delete(self, request, pk=None):
        if pk and Question.objects.filter(id=int(pk)).exists(): 
            qs = Question.objects.get(id=int(pk))
            qs.delete()  
            return Response({
                'message': 'Deleted successfully',  
                'error': None,
                'data': None
            }, status=status.HTTP_200_OK) 

        return Response({
            'message': 'Provide a valid pk',  
            'error': 'Not Found', 
            'data': None
        }, status=status.HTTP_404_NOT_FOUND) 