from django.apps import AppConfig # يقوم باستيراد الفئة (Class) الأساسية المسؤولة عن إعدادات التطبيقات في جانغو.


class AccountsConfig(AppConfig):#هذا الكلاس يرث خصائصه من AppConfig
    name = 'accounts'# للبحث عن المجلد الخاص بالتطبيق