# Online Course App – Final Project

Django online course application with an exam assessment feature, built by
Vedant Divate for the Coursera final project (Add a New Assessment Feature
to an Online Course App).

## Features

- `onlinecourse/models.py` – Course, Lesson, Enrollment, **Question**, **Choice**, **Submission**
- `onlinecourse/admin.py` – QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin
- Course detail page (`course_details_bootstrap.html`) with Bootstrap styling
- Exam submit (`submit`) and grading (`show_exam_result`) with `urls.py` paths
- Exam result page with Congratulations message and score

## Run locally

```bash
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Admin: http://localhost:8000/admin/
- Course: http://localhost:8000/onlinecourse/course/1/
