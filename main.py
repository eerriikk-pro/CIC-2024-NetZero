from fastapi import FastAPI

# Instantiate the class
app = FastAPI()


# Define a GET method on the specified endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
