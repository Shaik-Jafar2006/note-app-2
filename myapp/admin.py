from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponseForbidden

# Unregister the default User admin first
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):  # Inherit from Django's built-in UserAdmin
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_active')

    change_list_template = "admin/user_changelist.html"

    def changelist_view(self, request, extra_context=None):
        # ✅ Allow only superusers to view this page
        if not request.user.is_superuser:
            return HttpResponseForbidden("🚫 You are not authorized to view this page.")

        # Total registered users
        total_users = User.objects.count()

        # Find all active sessions (users currently logged in)
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_ids = []
        for session in sessions:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id')
            if user_id:
                user_ids.append(user_id)

        logged_in_users = User.objects.filter(id__in=user_ids)
        logged_in_count = logged_in_users.count()

        extra_context = extra_context or {}
        extra_context['total_users'] = total_users
        extra_context['logged_in_count'] = logged_in_count
        extra_context['logged_in_users'] = logged_in_users

        return super().changelist_view(request, extra_context=extra_context)
