from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm): #مخصص لتسجيل المستخدمين، وهو يرث خصائصه من نموذج جاهز في جانغو اسمه
    class Meta:#يحدد الإعدادات الأساسية للنموذج
        fields = ("username", "email", "password1", "password2")
        model = get_user_model() #"المستخدم" (User) يخبر جانغو أن هذا النموذج مرتبط بموديل

    def __init__(self, *args, **kwargs): #تقوم بتعديل النموذج عند تشغيله
        super().__init__(*args, **kwargs) # هنا قمنا بتغيير النص الذي يظهر فوق خانة اسم المستخدم ليكون "Display name" بدلاً من الاسم الافتراضي.
        self.fields["username"].label = "Display name" #وبالمثل، غيرنا النص الظاهر فوق خانة البريد الإلكتروني.

        self.fields["email"].label = "Email address"


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"
