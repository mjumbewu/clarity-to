import random, string
from django.db import models
from rest_framework import serializers


class OrderedThroughModel (models.Model):
    order = models.IntegerField(blank=True)

    class Meta:
        abstract = True
        ordering = ['order']

    def siblings(self, min_order=0):
        SelfModel = self._meta.model
        parent_field = self.order_parent_field
        return SelfModel.objects \
            .filter(**{parent_field: getattr(self, parent_field)}) \
            .exclude(id=self.id) \
            .filter(order__gte=min_order)

    def siblings_with_same_order(self):
        return self.siblings() \
            .filter(order=self.order)

    def max_order_within_parent(self):
        SelfModel = self._meta.model
        parent_field = self.order_parent_field
        summary = SelfModel.objects \
            .filter(**{parent_field: getattr(self, parent_field)}) \
            .aggregate(max_order=models.Max('order'))
        return summary.get('max_order') or 0

    def save(self, *a, **k):
        if self.order is None:
            self.order = self.max_order_within_parent() + 1
        elif self.siblings_with_same_order().exists():
            self.siblings(min_order=self.order) \
                .update(order=models.F('order') + 1)
        super().save(*a, **k)


class Issue (models.Model):
    label = models.CharField(max_length=200)
    icon = models.CharField('Path or URL of the icon', max_length=200, blank=True, default='')
    children = models.ManyToManyField('Issue', symmetrical=False, through='IssueRelationship', through_fields=('parent_issue', 'child_issue'), related_name='parents')
    default_root = models.ForeignKey('Issue', related_name='descendants', null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def default_parent(self):
        default_relationship = self.parent_relationships.filter(is_default_parent=True).first()
        return default_relationship.parent_issue if default_relationship else None

    def __str__(self):
        return self.label

    def save(self, *a, **k):
        parent = self.default_parent
        self.default_root = (parent.default_root
                             if (parent and parent.default_root)
                             else parent)
        return super().save(*a, **k)


class IssueRelationship (OrderedThroughModel):
    child_issue = models.ForeignKey('Issue', on_delete=models.CASCADE, related_name='parent_relationships')
    parent_issue = models.ForeignKey('Issue', on_delete=models.CASCADE, related_name='child_relationships')
    is_default_parent = models.BooleanField()

    order_parent_field = 'parent_issue'

    class Meta:
        unique_together = [('parent_issue', 'child_issue'), ('parent_issue', 'order')]

    def save(self, *a, **k):
        # If this relationship is set to default, unset any other default relations
        # for this child issue.
        if self.is_default_parent:
            IssueRelationship.objects \
                .filter(child_issue=self.child_issue) \
                .exclude(id=self.id) \
                .filter(is_default_parent=True) \
                .update(is_default_parent=False)

        # If this is not a default relationship but there are no other defaults for
        # this child, then make this relationship default.
        elif not IssueRelationship.objects.filter(child_issue=self.child_issue,
                                                  is_default_parent=True).exists():
            self.is_default_parent = True

        return super().save(*a, **k)


class IssueSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ('url', 'label', 'icon', 'pk')


class IssueSerializerWithChildren (serializers.HyperlinkedModelSerializer):
    children = IssueSerializer(many=True)
    default_parent = IssueSerializer()
    default_root = IssueSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ('url', 'label', 'icon', 'pk', 'children', 'default_parent', 'default_root')


class Platform (models.Model):
    key = models.CharField(max_length=100, blank=True)
    overview = models.TextField(blank=True)
    issues = models.ManyToManyField('Issue', through='PlatformIssue', related_name='+')

    def save(self, *a, **k):
        while not self.key:
            self.key = ''.join([
                random.choice(string.ascii_letters + string.digits)
                for _ in range(PLATFORM_KEY_LENGTH)
            ])
            if Platform.objects.filter(key=self.key).exists():
                self.key = None
        super().save(*a, **k)


class IssueLineageField (models.TextField):
    "Implements comma-separated storage of lists"

    def from_db_value(self, value, expression, connection):
        return Issue.obejcts.filter(id__in=value.split(','))

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if value is None:
            return value

        ids = value.split(',')
        issues = Issue.obejcts.filter(id__in=ids)
        if len(ids) > len(issues):
            raise models.ValidationError(f'Unable to find all issues in {values!r}')

        return issues

class PlatformIssue (OrderedThroughModel):
    platform = models.ForeignKey('Platform', on_delete=models.CASCADE)
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE)
    lineage = IssueLineageField(null=True)
    note = models.TextField(blank=True)

    order_parent_field = 'platform'

    class Meta:
        unique_together = [('platform', 'issue'),('platform', 'order')]
