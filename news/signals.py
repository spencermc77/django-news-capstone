from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    """Create user groups and assign permissions after migrations."""
    if sender.name != 'news':
        return

    reader_group, _ = Group.objects.get_or_create(name='Reader')
    editor_group, _ = Group.objects.get_or_create(name='Editor')
    journalist_group, _ = Group.objects.get_or_create(name='Journalist')

    permissions = Permission.objects.filter(
        codename__in=[
            'view_article',
            'add_article',
            'change_article',
            'delete_article',
            'can_approve_article',
            'view_newsletter',
            'add_newsletter',
            'change_newsletter',
            'delete_newsletter',
            'view_publisher',
            'add_publisher',
            'change_publisher',
            'delete_publisher',
        ]
    )

    permission_dict = {
        permission.codename: permission for permission in permissions
    }

    reader_group.permissions.set([
        permission_dict['view_article'],
        permission_dict['view_newsletter'],
        permission_dict['view_publisher'],
    ])

    editor_group.permissions.set([
        permission_dict['view_article'],
        permission_dict['change_article'],
        permission_dict['delete_article'],
        permission_dict['can_approve_article'],
        permission_dict['view_newsletter'],
        permission_dict['change_newsletter'],
        permission_dict['delete_newsletter'],
        permission_dict['view_publisher'],
        permission_dict['add_publisher'],
        permission_dict['change_publisher'],
        permission_dict['delete_publisher'],
    ])

    journalist_group.permissions.set([
        permission_dict['view_article'],
        permission_dict['add_article'],
        permission_dict['change_article'],
        permission_dict['delete_article'],
        permission_dict['view_newsletter'],
        permission_dict['add_newsletter'],
        permission_dict['change_newsletter'],
        permission_dict['delete_newsletter'],
        permission_dict['view_publisher'],
    ])