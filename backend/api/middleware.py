from channels.db import database_sync_to_async
from urllib.parse import parse_qs


"""
Gets the user from the given scope.

Given a scope (from ASGI), it will return the user associated with the scope.
If there is no user, it will return AnonymousUser.
"""
@database_sync_to_async
def get_user(scope):
    # Need to import here so when program starts, this can load after all apps are loaded.
    from django.contrib.auth.models import AnonymousUser
    from rest_framework_simplejwt.authentication import JWTAuthentication

    query_string = scope["query_string"].decode("utf-8")
    query_params = parse_qs(query_string)
    token_key = query_params.get("token", [None])[0]

    if token_key:
        try:
            # Decode the token to get the user
            validated_token = JWTAuthentication().get_validated_token(token_key)
            return JWTAuthentication().get_user(validated_token)
        except Exception:
            return AnonymousUser()

    return AnonymousUser()


class TokenAuthMiddleware:
    """
    Initialize the middleware with the given inner application.

    This is the constructor for TokenAuthMiddleware. It takes an inner ASGI application and stores it in the instance variable `self.inner`. This is needed for compatibility with ASGI.

    Parameters
    ----------
    inner : ASGI application
        The inner ASGI application to use with the middleware.

    Notes
    -----
    The inner application is the application that the middleware will wrap. This is the application that will be called by the middleware when a request is received.
    """
    def __init__(self, inner):
        self.inner = inner
    
    """
    This is the call function for TokenAuthMiddleware. It is needed for compatibility with ASGI.

    It will create an instance of TokenAuthMiddlewareInstance and call it with the given scope, receive, and send.
    """
    async def __call__(self, scope, receive, send):
        # Print for debugging

        print("WE DO GET HERE!!")
        
        # Create an instance of TokenAuthMiddlewareInstance
        instance = TokenAuthMiddlewareInstance(scope, self.inner)
        
        # Call the instance with receive and send
        await instance(receive, send)


class TokenAuthMiddlewareInstance:
    
    """
    Initialize the TokenAuthMiddlewareInstance with the given scope and inner application.

    This is the constructor for TokenAuthMiddlewareInstance. It takes a scope and an inner ASGI application and stores them in the instance variables `self.scope` and `self.inner`. This is needed for compatibility with ASGI.

    Parameters
    ----------
    scope : dict
        The scope of the incoming request. This is a dictionary that contains information about the request, such as the path, method, headers, and query parameters.
    inner : ASGI application
        The inner ASGI application to use with the middleware.

    Notes
    -----
    The scope is a dictionary that contains information about the request. It is used by the middleware to determine how to handle the request.
    """
    def __init__(self, scope, inner):

        self.scope = dict(scope)
        self.inner = inner
    
    """
    Call the middleware with the given receive and send functions.

    This is the call function for TokenAuthMiddlewareInstance. It is needed for compatibility with ASGI.

    Parameters
    ----------
    receive : callable
        A callable that can be used to receive incoming message from the client.
    send : callable
        A callable that can be used to send messages to the client.

    Notes
    -----
    This function will call the inner application with the updated scope.
    """
    async def __call__(self, receive, send):
        self.scope["user"] = await get_user(self.scope)
        # Call the inner application with the updated scope
        await self.inner(self.scope, receive, send)  # No need to return anything