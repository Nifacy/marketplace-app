import pytest
from app.schemas import TokenData
from app.usecases.oauth2 import generate_token, decode_token

def test_token_encoding_and_decoding():
    data = TokenData(type='supplier', id=123)

    token = generate_token(data)
    decoded_data = decode_token(token)

    assert decoded_data == data
