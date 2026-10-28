"""Data models for the OnlineCourse app: courses, lessons, exam and submissions."""

from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Course(models.Model):
    """An online course with lessons and an exam."""
    name = models.CharField(max_length=100, default='Online Course')
    description = models.CharField(max_length=500, default='Course description')
    pub_date = models.DateField(default=now)
    total_enrollment = models.IntegerField(default=0)

    def __str__(self):
        return f"Course: {self.name}"


class Lesson(models.Model):
    """A lesson belonging to a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Lesson')
    content = models.TextField(default='Lesson content')
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Lesson: {self.title}"


class Instructor(models.Model):
    """An instructor teaching courses on the platform."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        status = 'full-time' if self.full_time else 'part-time'
        return f"Instructor: {self.user.username} ({status})"


class Learner(models.Model):
    """A learner enrolled in courses and taking exams."""
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(
        max_length=20, choices=OCCUPATION_CHOICES, default=STUDENT
    )
    social_link = models.URLField(max_length=200, default='')

    def __str__(self):
        return f"Learner: {self.user.username} ({self.occupation})"


class Question(models.Model):
    """An exam question attached to a course, worth a grade."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, default='Question')
    question_grade = models.IntegerField(default=1)

    def __str__(self):
        return f"Question: {self.content}"

    def is_get_score(self, selected_ids):
        """Return True when the selected choice ids exactly match the correct ones."""
        correct_ids = set(
            self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        )
        return correct_ids == set(int(i) for i in selected_ids)


class Choice(models.Model):
    """A possible answer choice for a question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, default='Choice')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.content}"


class Submission(models.Model):
    """A learner's exam attempt: chosen choices per question."""
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission: {self.learner.user.username}"
