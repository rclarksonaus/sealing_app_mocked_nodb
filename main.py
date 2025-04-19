from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse  # ✅ 加上这个

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sealing Material Recommendation API")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recommend/score", response_model=schemas.RecommendResponse)
def recommend_score(input_data: schemas.InputData, db: Session = Depends(get_db)):
    return crud.score_recommendation(input_data, db)

@app.get("/", response_class=HTMLResponse)
def root():
    # return {"message": "Sealing Material Recommendation API is running"}
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()