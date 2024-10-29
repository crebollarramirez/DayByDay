from channels.db import database_sync_to_async
from urllib.parse import parse_qs

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
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Print for debugging
        print("WE DO GET HERE!!")
        
        # Create an instance of TokenAuthMiddlewareInstance
        instance = TokenAuthMiddlewareInstance(scope, self.inner)
        
        # Call the instance with receive and send
        await instance(receive, send)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = dict(scope)
        self.inner = inner

    async def __call__(self, receive, send):
        self.scope["user"] = await get_user(self.scope)
        # Call the inner application with the updated scope
        await self.inner(self.scope, receive, send)  # No need to return anything

