from fastapi import HTTPException, FastAPI, Depends , status
from sqlalchemy.orm import Session
from database import local_session
from pydantic import BaseModel
import models  
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT" , "DELETE"],  # Add OPTIONS method
    allow_headers=["Authorization","Content-Type"],
)
sender_email = os.getenv('EMAIL_SENDER')
password = os.getenv('EMAIL_PASSWORD')
class ModelUser(BaseModel):
    user_name: str
    email: str
    password: str
    mobile_number: str
    role: str
        
class profileUser(BaseModel):
    user_name: str
    email: str
    password: str
    mobile_number: str

class ModelAddress(BaseModel):
    street: str
    city: str
    state: str
    country: str

class login_user(BaseModel):
    email : str
    password : str

class forget_pass(BaseModel):
    email : str
    
class reset(BaseModel): 
   token: str 
   new_password: str

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()


def generate_token(length=20):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token



from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key for token signing
SECRET_KEY = "26"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up(user: ModelUser, addresses: ModelAddress, db: Session = Depends(get_db)):
    # Create a new user
    
    db_user = models.User(
        user_name=user.user_name,
        email=user.email,
        mobile_number=user.mobile_number,
        role=user.role,
        token = generate_token())
    db_user.password = pwd_context.hash(user.password)
    # Create an address associated with the user
    db_address = models.Address(
        street=addresses.street,
        city=addresses.city,
        state=addresses.state,
        country=addresses.country,
        user=db_user,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)    
    access_token = create_access_token(data={"id": db_user.uid ,"role": user.role})
    token_type = "bearer"
    return {"access_token": access_token, "token_type": token_type, "user_id": db_user.uid, "role": db_user.role}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def decode(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Example endpoint to retrieve user details using token
@app.get('/get_user')
def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode(token)
        user_id = payload.get('id')  # Assuming 'sub' is the key for user_id in the token payload

        # Fetch user from database based on user_id
        db_user = db.query(models.User).filter(models.User.uid == user_id).first()

        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return {
            "name": db_user.user_name,
            "email": db_user.email,
            "mobile_number": db_user.mobile_number
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    
@app.get("/get_address",status_code=status.HTTP_200_OK)    
def get_user( token: str = Depends(oauth2_scheme), db  :Session = Depends(get_db) ):
    payload = decode(token)
    user_id = payload.get('id')
    db_address = db.query(models.Address).filter(models.Address.user_id == user_id).all()
    return {"addresses" : db_address}


@app.post("/login" , status_code = status.HTTP_200_OK)
def login(user : login_user , db: Session = Depends(get_db)):
    consider_user = db.query(models.User).filter(models.User.email == user.email).first()
    if(consider_user):
      if(pwd_context.verify(user.password, consider_user.password)):
          access_token = create_access_token(data={"id": consider_user.uid , "role" :consider_user.role })
          token_type = "bearer"
          return {"access_token": access_token, "token_type": token_type, "user_id": consider_user.uid, "role": consider_user.role}
      else:
          return { "msg" : "pass_worng"}
    else:
        return {"msg" : "user not exist"}

@app.post("/logout")
def logout():
    return {"message": "Successfully logged out"}

@app.put("/edit")
def update_profile( profile: profileUser , token: str = Depends(oauth2_scheme) , db: Session = Depends(get_db)):
    payload = decode(token)
    user_id = payload.get('id')
    db_user = db.query(models.User).filter(models.User.uid == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user data based on provided fields
    if profile.user_name:
        db_user.user_name = profile.user_name
    if profile.email:
        db_user.email = profile.email
    if profile.password:
        db_user.password = pwd_context.hash(profile.password)
    if profile.mobile_number:
        db_user.mobile_number = profile.mobile_number

    # Commit changes to database
    db.commit()
    db.refresh(db_user)
    return db_user    

    
@app.post("/add_address")
def add_address( address : ModelAddress,token: str = Depends(oauth2_scheme) , db : Session = Depends(get_db) ):
    payload = decode(token)
    user_id = payload.get('id')
    user = db.query(models.User).filter(models.User.uid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_address = models.Address(street=address.street,
        city=address.city,
        state=address.state,
        country=address.country,
        user=user)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)

@app.post("/forget_password",status_code=status.HTTP_202_ACCEPTED)
def change_password( change : forget_pass , db : Session = Depends(get_db) ):
    db_user = db.query(models.User).filter(models.User.email == change.email).first()
    if not db_user:
        return {"message": "user not found"}
    mg = send_password_reset_email(change.email ,db_user.token)
    return {"message" : mg}

@app.post("/reset_password", status_code=status.HTTP_200_OK)
def reset_password(reset : reset, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.token == reset.token).first()
    
    if not db_user:
        return {"message": "user not found"}        

    db_user.password = pwd_context.hash(reset.new_password) 
    db.commit()
    
    return {"message": "Password reset successfully"}        

def send_password_reset_email(receiver_email, token):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Password Reset Request'
    
    body = f'Use this token to reset your password: {token}'
    message.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return "Email sent successfully"
    except Exception as e:
        return "Error sending email"

#product 

class product_model(BaseModel):
    pname : str
    price : int
    quantity_available : int
    category : str
    brand : str
    description : str


@app.post("/create_product")
def create_product(product : product_model , db: Session = Depends(get_db)):
    db_product = models.Product( 
        pname = product.pname, 
        price = product.price,
        quantity_available = product.quantity_available,
        category = product.category,
        brand = product.brand,
        description = product.description
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return { "msg" : "created" }
    
@app.put("/update_product/{pid}")
async def update_product( pid : int ,product : product_model , token: str = Depends(oauth2_scheme) , db: Session = Depends(get_db)):
    payload = decode(token)
    user_id = payload.get('id')
    db_product = db.query(models.Product).filter(models.Product.pid == pid).first()
    if db_product:
        if product.pname:
            db_product.pname = product.pname
        if product.price:
            db_product.price = product.price
        if product.quantity_available:
            if product.quantity_available == -1:
                db_product.quantity_available = 0
            else:
                db_product.quantity_available = product.quantity_available
        if product.category:
            db_product.category = product.category
        if product.brand:
            db_product.brand = product.brand
        if product.description:
            db_product.description = product.description
        if db_product.quantity_available == 0:
            db.delete(db_product)
            db.commit()
        db.commit() 
        return {"msg":"updated"}
    else:
        return {"msg":"no product"}

    
    
@app.get("/read_product")
def read_all(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get("/read_product/{pid}")
def read_all(pid : int ,db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.pid == pid).first()
    if(product):
      return product
    return {"msg" : "not found"}


@app.delete("/delete_product")
def update_product(token: str = Depends(oauth2_scheme) , db: Session = Depends(get_db)):
    payload = decode(token)
    user_id = payload.get('id')
    db_product = db.query(models.Product).filter(models.Product.pid == user_id).first()
    if db_product:
        db.delete(db_product)
        db.commit() 
        return {"msg":"deleted"}
    else:
        return {"msg":"no product"}

@app.get("/get_product",status_code=status.HTTP_200_OK)    
def get_product( token: str = Depends(oauth2_scheme), db  :Session = Depends(get_db) ):
   # user_id = int(user_id)
    payload = decode(token)
    user_id = payload.get('id')
    db_product = db.query(models.Product).filter(models.Product.pid == user_id).first()
    return {"name" : db_product.pname , "quantity":db_product.quantity_available , "price" : db_product.price}


#order

class order(BaseModel):
    uid : int
    total_rate : int
    address : str
    
@app.post("/pot_order")
def order( order : order , db: Session = Depends(get_db)):
    db_order = models.Order(
        uid = order.uid ,
        total_amount = order.total_rate ,
        address = order.address
    )
    db.add(db_order)
    db.commit() 
    db.refresh(db_order)
    
@app.get("/read_order")
def read_all( token: str = Depends(oauth2_scheme) , db: Session = Depends(get_db)):
    payload = decode(token)
    user_id = payload.get('id')
    orders = db.query(models.Order).filter(user_id == models.Order.uid).all()
    return orders

#review

class model_review(BaseModel):
    rating : int
    review_text : str

@app.post('/review/{pid}' , status_code=status.HTTP_201_CREATED , response_model=None)
def review( pid : int , review : model_review , token: str = Depends(oauth2_scheme) ,db : Session = Depends(get_db)):
    payload = decode(token)
    user_id = payload.get('id')
    db_review = models.Review(
        uid = user_id ,
        pid =pid ,
        rating = review.rating ,
        review_text = review.review_text
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return {'msg' : 'success'}
    
@app.get("/read_reviews/{pid}")
def read_all( pid : int ,  token: str = Depends(oauth2_scheme) , db: Session = Depends(get_db)):
    payload = decode(token)
    user_id = payload.get('id')
    reviews = db.query(models.Review,models.User.user_name).join(models.User,models.User.uid == user_id).filter(models.Review.pid ==  pid).all()
    reviews_with_username = []
    for review , user_name in reviews:
            review_dict = {
                "id": review.id,
                "review_text": review.review_text,
                "rating": review.rating,
                "username": user_name  
            }
            reviews_with_username.append(review_dict)

    return reviews_with_username
    