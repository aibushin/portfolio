from arepl_dump import dump  # type: ignore  # noqa: F401
from time import sleep
from datetime import datetime, timezone, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=3)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "mysecret")


if __name__ == "__main__":
    token = create_access_token({"some": "data"})
    print(token)
    sleep(5)
    try:
        print(jwt.decode(token, algorithms=["HS256"], key="mysecret"))
    except ExpiredSignatureError:
        print("Caught ExpiredSignatureError. Now decoding with verify_exp=False.")
        try:
            # Decode with expiration check disabled
            decoded_payload = jwt.decode(
                token, "mysecret", algorithms=["HS256"], options={"verify_exp": False}
            )
            print("Expired token successfully decoded with verify_exp=False:", decoded_payload)
        except InvalidTokenError as e:
            print(f"Error decoding token even with verify_exp=False: {e}")
    except InvalidTokenError as e:
        print(f"Invalid token error: {e}")

    print(jwt.decode(token, algorithms=["HS256"], key="mysecret"))
