from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question
import random


def home(request):
    return render(request, 'quiz/home.html')


def start_quiz(request):
    request.session['correct_answers'] = 0
    request.session['total_questions'] = 0
    request.session['question_index'] = 0
    request.session['asked_questions'] = []  
    question = get_next_question(request)
    return render(request, 'quiz/question.html', {'question': question})


def get_next_question(request):
    asked_questions = request.session.get('asked_questions', [])
    remaining_questions = Question.objects.exclude(id__in=asked_questions)

    if remaining_questions.count() == 0:
        return None

    next_question = random.choice(remaining_questions)
    asked_questions.append(next_question.id)
    request.session['asked_questions'] = asked_questions
    request.session['current_question'] = next_question.id
    
    return next_question


def question(request):
    if 'question_index' not in request.session:
        return redirect('quiz:start_quiz')

    question_index = request.session['question_index']
    questions = list(Question.objects.all())
    if question_index < len(questions):
        current_question = questions[question_index]
        return render(request, 'quiz/question.html', {'question': current_question})
    else:
        return redirect('quiz:results')

def submit_answer(request):
    if request.method == 'POST':
        selected_option = request.POST.get('option')
        current_question_id = request.session.get('current_question')
        
        if not current_question_id:
            return redirect('quiz:start_quiz')  
        
        try:
            question = Question.objects.get(id=current_question_id)
        except Question.DoesNotExist:
            return redirect('quiz:start_quiz')


        if selected_option == question.correct_answer:
            request.session['correct_answers'] += 1
        request.session['total_questions'] += 1
        request.session['question_index'] += 1

        next_question = get_next_question(request)

        if next_question:
            request.session['current_question'] = next_question.id
            return render(request, 'quiz/question.html', {'question': next_question})
        else:
            return redirect('quiz:results')


def show_results(request):
    total_questions = request.session.get('total_questions', 0)
    correct_answers = request.session.get('correct_answers', 0)
    return render(request, 'quiz/results.html', {'total_questions': total_questions, 'correct_answers': correct_answers})


def play_again(request):
    return redirect('quiz:start_quiz')

def exit_game(request):
    request.session.flush()  
    return redirect('quiz:home')  
