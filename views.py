"""Views for the OnlineCourse app: details, exam submit and results."""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Course, Learner, Question, Submission


def course_details(request, course_id):
    """Show the course name and all related lessons."""
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lesson_set.order_by('order')
    questions = course.question_set.all()
    enrolled = False
    if request.user.is_authenticated:
        enrolled = Learner.objects.filter(
            user=request.user
        ).exists()
    context = {
        'course': course,
        'lessons': lessons,
        'questions': questions,
        'enrolled': enrolled,
    }
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)


def enroll(request, course_id):
    """Register the logged-in user as a learner and go back to details."""
    course = get_object_or_404(Course, pk=course_id)
    if request.user.is_authenticated:
        Learner.objects.get_or_create(user=request.user)
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


@login_required
def submit(request, course_id):
    """Create a Submission from the selected exam choices."""
    course = get_object_or_404(Course, pk=course_id)
    learner = get_object_or_404(Learner, user=request.user)
    submission = Submission.objects.create(learner=learner)
    selected_ids = []
    for question in course.question_set.all():
        key = f'choice_{question.id}'
        selected_ids.extend(request.POST.getlist(key))
    for choice_id in selected_ids:
        submission.choices.add(get_object_or_404(Choice, pk=int(choice_id)))
    submission.save()
    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course.id, submission.id))
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    """Grade the submission and render the exam result page."""
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = set(submission.choices.values_list('id', flat=True))
    total_score = 0
    max_score = 0
    results = []
    for question in course.question_set.all():
        max_score += question.question_grade
        chosen = [
            str(cid) for cid in selected_ids
            if submission.choices.filter(pk=cid, question=question).exists()
        ]
        correct = question.is_get_score(chosen)
        if correct:
            total_score += question.question_grade
        results.append({
            'question': question,
            'choices': question.choice_set.all(),
            'selected_ids': {int(i) for i in chosen},
            'correct': correct,
        })
    grade = round(100 * total_score / max_score) if max_score else 0
    context = {
        'course': course,
        'submission': submission,
        'results': results,
        'grade': grade,
        'total_score': total_score,
        'max_score': max_score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
