from ....responses import ct_response
def _login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser) or not request.user.is_authenticated():
            return ct_response(content="用户未登录", state=2)
        return func(request, *args, **kwargs)
    return wrapper