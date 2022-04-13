import jwt

from fastapi import Request
from fastapi.security import HTTPBearer

from . import const

ALGORITHMS = ["RS256"]
token_auth_scheme = HTTPBearer()


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class JWTBearer(HTTPBearer):
    def __init__(self, required_scope=None, any_scope=[], auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

        self.token = None
        self.required_scope = required_scope
        self.any_scope = any_scope

    async def __call__(self, request: Request):
        self.token = await super(JWTBearer, self).__call__(request=request)

        await self.check_auth()
        await self.check_scope(required_scope=self.required_scope, any_scope=self.any_scope)

    async def check_auth(self):
        jwks_url = "https://{}/.well-known/jwks.json".format(const.AUTH0_DOMAIN)
        jwks_client = jwt.PyJWKClient(jwks_url)

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(
                self.token.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise AuthError({"code": "jwk_client_error",
                             "description": "bad jwk client"}, 401)
        except jwt.exceptions.DecodeError as error:
            raise AuthError({"code": "jwt_decode_error",
                             "description": error.__str__()}, 401)

        if signing_key:
            try:
                jwt.decode(
                    self.token.credentials,
                    signing_key,
                    algorithms=ALGORITHMS,
                    audience=const.AUTH0_AUDIENCE,
                    issuer="https://{}/".format(const.AUTH0_DOMAIN)
                )
            except jwt.exceptions.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401)
            except jwt.exceptions.MissingRequiredClaimError:
                raise AuthError({"code": "invalid_claims",
                                 "description":
                                     "incorrect claims,"
                                     " please check the audience and issuer"}, 401)
            except Exception as e:
                print(e)
                raise AuthError({"code": "invalid_header",
                                 "description":
                                     "Unable to parse authentication"
                                     " token."}, 401)

        else:
            raise AuthError({"code": "invalid_header",
                             "description": "Unable to find appropriate key"}, 401)

    async def check_scope(self, required_scope=None, any_scope=[]):
        unverified_claims = jwt.decode(self.token.credentials, options={"verify_signature": False})

        if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if required_scope is not None:
                    if token_scope == required_scope:
                        return
                if isinstance(any_scope, list):
                    for scope in any_scope:
                        if token_scope == scope:
                            return
        raise AuthError({
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403)
