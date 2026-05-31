
from django.urls import re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'#يُسمى "Namespace". يُستخدم لتمييز روابط هذا التطبيق عن غيره. فبدلاً من كتابة الرابط يدوياً، تستخدم accounts:login.

urlpatterns = [ #هذه قائمة تحتوي على جميع المسارات المتاحة في هذا القسم من الموقع.

    re_path(r"^login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),# رابط تسجيل الدخول (login/
    re_path(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"), #رابط تسجيل الخروج (logout/
    re_path(r"^signup/$", views.SignUp.as_view(), name="signup"), # رابط إنشاء حساب جديد (signup/)
    re_path(r"^edit/$", views.EditProfile.as_view(), name="edit"),
    re_path(r"^delete/$", views.DeleteAccount.as_view(), name="delete"),
]
