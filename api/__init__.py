"""
Here be awesome code!
"""
from fastapi import FastAPI

# pylint: disable=invalid-name
app = FastAPI()


@app.get("/")
def read_root():
    """
    Welcome home!
    """
    return {"Hello": "World"}
