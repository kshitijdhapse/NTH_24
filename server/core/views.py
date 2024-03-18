from django.shortcuts import render, get_object_or_404
from .serializers import *
from .models import *
import json
import random
from datetime import datetime
import pytz
from difflib import SequenceMatcher

# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# class UserView(APIView):
#     def get(self,request, *args, **kwargs):
#         print(args,"args")
#         print(kwargs,"kwargs")
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

# class UserViewSet(viewsets.ViewSet):

#     # List All Users -- get method
#     def list(self, request):
#         users = User.objects.filter(hidden_on_leaderboard=False).order_by('-current_level','last_level_updated_time')
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     # Retrieve Particular User -- get method
#     def retrieve(self, request, pk = None):
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, pk = pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

#     # Create a new User -- post method
#     def create(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
    # Scheduler 
    # def addKey():
    #     queryset = User.objects.all()
    #     print("scheduler called")
    #     for user in queryset:
    #         user.keys += 1
    #         user.save()
    
class QuestionDetail(generics.RetrieveAPIView):
    
    def get(self, request, user_ans = None):
        print(user_ans)
        if request.user.is_authenticated:
            user = request.user
            queryset = Question.objects.all()
            que = get_object_or_404(queryset, level = user.current_level)
            isCorrect = False
            match = SequenceMatcher(None, user_ans, que.answer).ratio()
            promocode = Timer.objects.all().first()

            if user_ans and user_ans != "put_your_ans_here":
                try:
                    answer_history, created = AnswerHistory.objects.get_or_create(user=user, question=que)
                    if created:
                        answer_history.answers = []
                    answer_history.answers.append([user_ans, datetime.now().strftime('%Y-%m-%d %H:%M')])
                    answer_history.save()
                except Exception as e:
                    print("History Error: ", e)


            # Check for promocode
            if promocode.promo_code_active and not user.promo_used:
                if user_ans == promocode.promocode or que.answer == user_ans:
                    user.current_level += 1
                    user.paidHintTaken = False
                    user.is_rigged=False
                    user.machine_used=0
                    user.promo_used = True
                    user.save()
                    isCorrect = True
                if(que.answer == user_ans):
                    user.is_rigged=False
                    user.machine_used=0
                    user.keys += user.current_level - 1
                    user.save()
                que = get_object_or_404(queryset, level = user.current_level)

            # Evaluate The Answer
            elif que.answer == user_ans:
                user.keys += que.level
                user.current_level += 1
                user.is_rigged=False
                user.machine_used=0
                user.paidHintTaken = False
                print(user.current_level,"level")
                user.save(update_fields=['keys','paidHintTaken','current_level','is_rigged','machine_used','last_level_updated_time'])
                isCorrect = True
                que = get_object_or_404(queryset, level = user.current_level)
            # Evaluate Rigword
            elif que.rigword == user_ans:
                user.is_rigged = True
                user.save()
            # Keyword Check for prompts
            elif match >= 0.7:
                responses = ["You are close.", "Almost There!"]
                serializer = QuestionSerializer(que)
                print(serializer.data)
                data = serializer.data
                data["promts"] = random.choice(responses)
                if user.paidHintTaken:
                    data["paidHint"] = que.paidHint
                return Response(data)

            serializer = QuestionSerializer(que)
            data = serializer.data
            if isCorrect:
                data["promts"] = f"Congratulations!! Advancing to level {user.current_level}."
                # if que.level == 3:
                #     data["promts"] = f"You're Goddamn Right!" # change this in next NTH
            else:
                data["promts"] = f"Wrong Answer!"
            if user.paidHintTaken:
                data["paidHint"] = que.paidHint
            return Response(data)
        error_dict = {"status":"Not Authenticated"}
        return Response(json.dumps(error_dict))


class LeaderboardView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(hidden_on_leaderboard=False, is_active=True).order_by('-current_level','last_level_updated_time')[:100]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class ExtraHintView(APIView):
    def post(self, request):    
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        # username = request.data["username"]
        res_dict = {"status":"You Don't Have Enough Keys"}
        user = request.user
        print("HI",user.current_level)
        que = get_object_or_404(Question, level = user.current_level)
        print("bye",que)
        if(user.paidHintTaken):
            # res_dict = {"status":"You have already taken a hint!"}
            res_dict = {"extraHint":que.paidHint}
            return Response(res_dict)
        if user.keys >= que.hintCost:
            user.keys -= que.hintCost
            user.paidHintTaken = True
            user.save(update_fields=['keys','paidHintTaken'])
            res_dict = {"extraHint":que.paidHint}
            return Response(res_dict)
        return Response(res_dict)


class TimerView(APIView):
    def get(request,*args, **kwargs):
        timer = Timer.objects.all().first()
        serializer = TimerSerializer(timer)
        return Response(serializer.data)

class SlotMachine(APIView):
    def post(self, request):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        user = request.user
        chance = [random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)]
        res_dict = {'slotmachine': chance}
        que = get_object_or_404(Question, level=user.current_level)
        if user.is_rigged and user.machine_used < 3:
            res_dict = {'slotmachine': [7, 7, 7]}
            user.machine_used += 1
            user.keys += 15
            user.save()
            return Response(res_dict)
        elif user.machine_used < 3:
            user.machine_used += 1
            user.keys += chance.count(7) * 5
            user.save()
        else:
            res_dict = {"status": "Chances Exhausted"}
        return Response(res_dict)
        # error_dict = {"status":"Not Authenticated"}
        # return Response(json.dumps(error_dict))



class FeedbackView(APIView):
    def post(self,request, *args, **kwargs):
        user = request.user
        print(request.data)
        # if user != None:
        #     print("if")
        #     username = user.username
        # else:
        username = request.data['name']

        feedback = request.data['feedback']

        Feedback.objects.create(name = username, feedback=feedback)
        return Response({'status':'opie'})
