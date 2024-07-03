from fastapi import HTTPException, FastAPI, Depends , status
from sqlalchemy.orm import Session
from database import local_session, engine, Base
from pydantic import BaseModel
import models  # Assuming your models are imported correctly
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT" , "DELETE"],  # Add OPTIONS method
    allow_headers=["Content-Type"],
)

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
    if(db_user.role == "user"):
        return { "user_id" : db_user.uid , "role" : "u"}
    else:
        return { "user_id" : db_user.uid , "role" : "a"}


@app.get("/get_user/{uid}",status_code=status.HTTP_200_OK)    
def get_user( uid : int , db  :Session = Depends(get_db) ):
   # user_id = int(user_id)
    db_user = db.query(models.User).filter(models.User.uid == uid).first()
    return {
        "name" : db_user.user_name , 
        "email" : db_user.email ,
        "mobile_number" : db_user.mobile_number 
    }
    
@app.get("/get_address/{uid}",status_code=status.HTTP_200_OK)    
def get_user( uid : int , db  :Session = Depends(get_db) ):
    db_address = db.query(models.Address).filter(models.Address.user_id == uid).all()
    return {"addresses" : db_address}


@app.post("/login" , status_code = status.HTTP_200_OK)
def login(user : login_user , db: Session = Depends(get_db)):
    consider_user = db.query(models.User).filter(models.User.email == user.email).first()
    if(consider_user):
      if(pwd_context.verify(user.password, consider_user.password)):
          if(consider_user.role == "user"):
             return { "user_ID" : consider_user.uid , "role" : "u"}
          else:
              return { "user_ID" : consider_user.uid , "role" : "a"}
      else:
          return { "msg" : "pass_worng"}
    else:
        return {"msg" : "user not exist"}

@app.post("/logout")
def logout():
    return {"message": "Successfully logged out"}

@app.put("/edit/{user_id}")
def update_profile(user_id: int, profile: profileUser, db: Session = Depends(get_db)):
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

    
@app.post("/add_address/{uid}")
def add_address( uid : int , address : ModelAddress , db : Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.uid == uid).first()
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
        return {"msg" : "no mail"}
    send_password_reset_email(change.email ,db_user.token)
    return {"msg" : "yes mail"}

@app.post("/reset_password", status_code=status.HTTP_200_OK)
def reset_password(reset : reset, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.token == reset.token).first()
    
    if not db_user:
        return {"message": "token not found"}        

    db_user.password = pwd_context.hash(reset.new_password) 
    db.commit()
    
    return {"message": "Password reset successfully"}        

def send_password_reset_email(receiver_email, token):
    sender_email = '2022it0835@svce.ac.in'
    password = 'svce4321'
    
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
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

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
    
@app.put("/update_product/{id}")
async def delete_product( id : int , product : product_model , db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.pid == id).first()
    if db_product:
        if product.pname:
            db_product.pname = product.pname
        if product.price:
            db_product.price = product.price
        if product.quantity_available is not None:
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

@app.delete("/delete_product/{id}")
def update_product( id : int , db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.pid == id).first()
    if db_product:
        db.delete(db_product)
        db.commit() 
        return {"msg":"deleted"}
    else:
        return {"msg":"no product"}

@app.get("/get_product/{id}",status_code=status.HTTP_200_OK)    
def get_product( id : int , db  :Session = Depends(get_db) ):
   # user_id = int(user_id)
    db_product = db.query(models.Product).filter(models.Product.pid == id).first()
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
    
@app.get("/read_order/{id}")
def read_all( id : int , db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(id == models.Order.uid).all()
    return orders
    