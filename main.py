
from view import app,dbsession



if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app',reload=True)




