from django.contrib import admin
from .models import Issue, IssueRelationship

# Register your models here.
class ParentIssuesInline (admin.TabularInline):
    model = IssueRelationship
    fk_name = 'child_issue'
    raw_id_fields = ['parent_issue']
    exclude = ['order']
    extra = 0

    verbose_name = 'parent'
    verbose_name_plural = 'parents'

class ChildIssuesInline (admin.TabularInline):
    model = IssueRelationship
    fk_name = 'parent_issue'
    raw_id_fields = ['child_issue']
    extra = 0

    verbose_name = 'child'
    verbose_name_plural = 'children'

class IssueAdmin (admin.ModelAdmin):
    list_display = ['label', 'default_parent', 'default_root']
    search_fields = ['label']

    inlines = [ParentIssuesInline, ChildIssuesInline]
    readonly_fields = ['default_root']

admin.site.register(Issue, IssueAdmin)