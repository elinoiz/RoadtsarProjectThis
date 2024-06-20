# main.py
from fastapi import FastAPI, Depends, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import User, Advertisement, Base, Bid
from pydantic import BaseModel
from typing import List, Optional
import base64  # Импортируем модуль base64

app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:avzad220604@localhost/roadstar"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserResponse(BaseModel):
    user_id: int
    user_name: str

    class Config:
        orm_mode = True

class AdvertisementResponse(BaseModel):
    ad_id: int
    user_id: int
    city: str
    description: str
    start_price: int
    title: str
    category: str
    photo: Optional[str]
    user_name: Optional[str]  # Добавляем поле user_name

    @staticmethod
    def from_orm(advertisement, user_name=None):
        return AdvertisementResponse(
            ad_id=advertisement.ad_id,
            user_id=advertisement.user_id,
            city=advertisement.city,
            description=advertisement.description,
            start_price=advertisement.start_price,
            title=advertisement.title,
            category=advertisement.category,
            photo=base64.b64encode(advertisement.photo).decode('utf-8') if advertisement.photo else None,
            user_name=user_name  # Устанавливаем user_name
        )

    class Config:
        orm_mode = True


class BidRequest(BaseModel):
    ad_id: int
    user_id: int
    bid_amount: int


class BidResponse(BaseModel):
    bid_id: int
    ad_id: int
    user_id: int
    bid_amount: int
    user_name: str

    class Config:
        orm_mode = True


@app.post("/register/")
async def register_user(user_name: str = Form(...), user_pass: str = Form(...), db: Session = Depends(get_db)):
    user = User(user_name=user_name, user_pass=user_pass)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully", "id": user.user_id}

@app.post("/login/")
async def login_user(user_name: str = Form(...), user_pass: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_name).first()
    if not user or user.user_pass != user_pass:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"success": True, "user_id": user.user_id, "user_name": user.user_name}

@app.get("/get-all/", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
    
@app.get("/get_ad", response_model=List[AdvertisementResponse])
async def get_all_ads(db: Session = Depends(get_db)):
    ads = db.query(Advertisement).all()
    print(f"Ads: {ads}")  # Отладочный вывод
    return [AdvertisementResponse.from_orm(ad) for ad in ads]

# main.py
@app.get("/get_ad/{ad_id}", response_model=AdvertisementResponse)
async def get_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(Advertisement).filter(Advertisement.ad_id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    user = db.query(User).filter(User.user_id == ad.user_id).first()
    user_name = user.user_name if user else "Unknown"
    ad_response = AdvertisementResponse.from_orm(ad, user_name=user_name)
    return ad_response




@app.post("/createAd")
async def create_ad(
    user_id: int = Form(...),
    city: str = Form(...),
    description: str = Form(...),
    start_price: int = Form(...),
    title: str = Form(...),
    category: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Логирование входных данных
    print(f"user_id: {user_id}, city: {city}, description: {description}, start_price: {start_price}, title: {title}, category: {category}")

    if photo:
        photo_data = await photo.read()
    else:
        photo_data = None

    new_ad = Advertisement(
        user_id=user_id,
        city=city,
        description=description,
        start_price=start_price,
        title=title,
        category=category,
        photo=photo_data
    )
    
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    return {"message": "Ad created successfully", "id": new_ad.ad_id}



@app.post("/place_bid")
async def place_bid(bid: BidRequest, db: Session = Depends(get_db)):
    new_bid = Bid(
        ad_id=bid.ad_id,
        user_id=bid.user_id,
        bid_amount=bid.bid_amount
    )
    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)
    return {"message": "Bid placed successfully", "id": new_bid.bid_id}




@app.get("/get_bids/{ad_id}", response_model=List[BidResponse])
async def get_bids(ad_id: int, db: Session = Depends(get_db)):
    bids = db.query(Bid).filter(Bid.ad_id == ad_id).all()
    bid_responses = []
    for bid in bids:
        user = db.query(User).filter(User.user_id == bid.user_id).first()
        user_name = user.user_name if user else "Unknown"
        bid_responses.append(BidResponse(
            bid_id=bid.bid_id,
            ad_id=bid.ad_id,
            user_id=bid.user_id,
            bid_amount=bid.bid_amount,
            user_name=user_name
        ))
    return bid_responses
