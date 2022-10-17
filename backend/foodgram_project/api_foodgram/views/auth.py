# from djoser.views import UserViewSet

# from django.contrib.auth import get_user_model

# from djoser.conf import settings
# # from serializers.auth import CustomUserSerializer
# # from users.models import User

# User = get_user_model()


# class CustomUserViewSet(UserViewSet):
#     def get_queryset(self):
#         user = self.request.user
#         queryset = super().get_queryset()
#         if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
#             queryset = User.objects.all()
#         return queryset
