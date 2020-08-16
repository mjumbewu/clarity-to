from django.test import TestCase

class PlatformIssueOrderTest (TestCase):
    def test_assigns_order_correctly(self):
        other_platform = Platform.objects.create()
        platform = Platform.objects.create()

        issues = [
            Issue.objects.create(label='A'),
            Issue.objects.create(label='B'),
            Issue.objects.create(label='C'),
            Issue.objects.create(label='D'),
            Issue.objects.create(label='E'),
        ]

        for issue in issues:
            other_platform.issues.add(issue)

        platform.issues.add(issues[0])
        self.assertEqual(PlatformIssue.objects.filter(platform=platform).count(), 1)
        self.assertEqual(PlatformIssue.objects.get(platform=platform).order, 1)

        platform.issues.add(issues[1])
        self.assertEqual(PlatformIssue.objects.filter(platform=platform).count(), 2)
        self.assertEqual({pi.order for pi in PlatformIssue.objects.filter(platform=platform)}, {1, 2})

        platform.issues.add(issues[2], through_defaults={'order': 1})
        self.assertEqual(PlatformIssue.objects.filter(platform=platform).count(), 3)
        self.assertEqual({pi.order for pi in PlatformIssue.objects.filter(platform=platform)}, {1, 2, 3})
        self.assertEqual(PlatformIssue.objects.get(platform=platform, issue=issues[2]).order, 1)
