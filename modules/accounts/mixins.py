# -*- coding: utf-8 -*-

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

class AllowedGroupsMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        user_groups = self.request.user.groups.values_list('name',flat=True)
        allowed_groups = self.allowed_groups
        
        if self.allowed_groups == '__all__' or [i for i in user_groups if i in allowed_groups]:
            return super(AllowedGroupsMixin, self).dispatch(*args, **kwargs)
        else:
            raise PermissionDenied
            