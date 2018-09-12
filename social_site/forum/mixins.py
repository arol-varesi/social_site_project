from django.contrib.auth.mixins import UserPassesTestMixin

class StaffMixin(UserPassesTestMixin):
    """ lo scopo di questo mixin è fare in modo che
    solo lo staff possa creare nuove sezioni """

    def test_func(self):
        return self.request.user.is_staff
