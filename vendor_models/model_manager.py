from django.contrib.auth.models import BaseUserManager




class VendorBaseUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an Email Address')

        user = self.model(
            email=self.normalize_email(email),
            is_active=False,
        )
        print("VendorBaseUserManager  Normal----",password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        print("VendorBaseUserManager- super---",password)
        
        user.save(using=self._db)
        return user