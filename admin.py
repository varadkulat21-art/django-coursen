"""Admin configuration for the OnlineCourse app."""

from django.contrib import admin

from .models import Choice, Course, Instructor, Learner, Lesson, Question, Submission


class ChoiceInline(admin.StackedInline):
    """Edit choices inline on the question page."""
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    """Edit questions inline on the course page."""
    model = Question
    extra = 3


class LessonInline(admin.StackedInline):
    """Edit lessons inline on the course page."""
    model = Lesson
    extra = 3


class CourseAdmin(admin.ModelAdmin):
    """Course editing with lessons and exam questions inline."""
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date', 'total_enrollment')
    list_filter = ['pub_date']
    search_fields = ('name',)


class LessonAdmin(admin.ModelAdmin):
    """Lesson overview in the admin."""
    list_display = ('title', 'course', 'order')


class QuestionAdmin(admin.ModelAdmin):
    """Question editing with answer choices inline."""
    inlines = [ChoiceInline]
    list_display = ('content', 'question_grade', 'course')
    search_fields = ('content',)


class SubmissionAdmin(admin.ModelAdmin):
    """Read-only overview of exam submissions."""
    list_display = ('learner',)
    readonly_fields = ('learner',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
