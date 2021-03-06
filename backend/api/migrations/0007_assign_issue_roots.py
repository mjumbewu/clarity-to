# Generated by Django 2.1.4 on 2020-08-03 01:25

from django.db import migrations


def forwards_func(apps, schema_editor):
    Issue = apps.get_model("api", "Issue")

    unprocessed_issues = [(None, issue) for issue in Issue.objects.filter(parent_relationships=None)]
    processed_issues = []
    while unprocessed_issues:
        parent, issue = unprocessed_issues.pop(0)
        issue.root = parent.root if (parent and parent.root) else parent
        processed_issues.append(issue)

        unprocessed_issues.extend([
            (issue, relation.child_issue)
            for relation in issue.child_relationships.all().select_related('child_issue')
            if relation.is_default_parent
        ])

    Issue.objects.bulk_update(processed_issues, ['root'])

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_issue_root'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
