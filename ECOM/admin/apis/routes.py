from .models import *
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, UploadFile, File
from admin.apis.pydantic_models import categoryitem, subcategoryitem, productitem,categoryUpdate,categoryDelete,subcategoryUpdate,updateproductitem,Useradmin,AdminLogin,Token
from fastapi_login import LoginManager
from fastapi.encoders import jsonable_encoder
import json
import jwt
import os
from slugify import slugify
from datetime import datetime, timedelta
from configs import appinfo
from functools import lru_cache
from email_validator import validate_email,EmailNotValidError
from passlib.context import CryptContext

# @lru_cache()
# def app_setting():
#     return appinfo.Setting()

# settings=app_setting()
# app_url=settings.app_url
SECRET='your-secret-key'


router = APIRouter()
manager=LoginManager(SECRET,token_url='/admin_login/')
pwd_context=CryptContext(schemes=["bcrypt"],deprecated='auto')
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post('/category/')
async def create_category(data: categoryitem = Depends(), category_image: UploadFile = File(...)):
    if await Category.exists(name=data.name):
        return{"status": False, "message": "category already exists"}
    else:
        slug = slugify(data.name)

        FILEPATH = 'static/images/category/'

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = category_image.filename
        extention = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extention not in ['png', 'jpg', 'jpeg']:
            return {'status': 'error', "details": 'file extension not allowed'}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+" "+str(dt_timestamp)+" "+extention
        generated_name = FILEPATH+modified_image_name
        file_content = await category_image.read()

        with open(generated_name, "wb") as file:
            file.write(file_content)
            file.close()
        # image_url=generated_name

        category_obj = await Category.create(
            category_image=generated_name,
            description=data.description,
            name=data.name,
            slug=slug
        )

        if category_obj:
            return {"status": True, "message": " category added"}
        else:
            return {"status": False, "message": " something wrong"}


@router.get('/allcat/')
async def get_cat():
    cat = await Category.all()
    return cat


@router.post('/subcategory/')
async def create_subcategory(data: subcategoryitem = Depends(), subcategory_image: UploadFile = File(...)):
    if await Category.exists(id=data.category_id):
        category_obj = await Category.get(id=data.category_id)

        if await SubCategory.exists(name=data.name):
            return{"status": False, "message": "category already exists"}
        else:
            slug = slugify(data.name)

            FILEPATH = "static/images/subcategory"

            if not os.path.isdir(FILEPATH):
                os.mkdir(FILEPATH)

            filename = subcategory_image.filename
            extension = filename.split(".")[1]
            imagename = filename.split(".")[0]

            if extension not in ['png', 'jpg', 'jpeg']:
                return {"status": "error", "detail": "file extension not allowed"}

            dt = datetime.now()
            dt_timestamp = round(datetime.timestamp(dt))

            modified_image_name = imagename+"_"+str(dt_timestamp)+" "+extension
            generated_name = FILEPATH+modified_image_name

            file_content = await subcategory_image.read()

            with open(generated_name, "wb") as file:
                file.write(file_content)
                file.close()
            # image_url = generated_name

            subcategory_obj = await SubCategory.create(
                subcategory_image=generated_name,
                description=data.description,
                category=category_obj,
                name=data.name,
                slug=slug
            )

            if subcategory_obj:
                return{"status": True, "message": "sub category added"}
            else:
                return{"status": False, "message": "something wrong"}
            
@router.get('/allsubcat/')
async def get_subcat():
    subcat = await SubCategory.all()
    return subcat


# product API
@router.post('/product/')
async def create_product(data: productitem = Depends(), product_image: UploadFile = File(...)):
    # if await Category.exists(id=data.category_id):
        category_obj = await Category.get(id=data.category_id)
    # if await SubCategory.exists(id=data.subcategory_id):
        subcategory_obj = await SubCategory.get(id=data.subcategory_id)
        if await Product.exists(product_name=data.product_name):
            return{"status": False, "message": "Product already exists"}
        else:
            # slug = slugify(data.product_name)

            FILEPATH = "static/images/product"

            if not os.path.isdir(FILEPATH):
                os.mkdir(FILEPATH)

            filename = product_image.filename
            extension = filename.split(".")[1]
            imagename = filename.split(".")[0]

            if extension not in ['png', 'jpg', 'jpeg']:
                return {"status": "error", "detail": "file extension not allowed"}

            dt = datetime.now()
            dt_timestamp = round(datetime.timestamp(dt))

            modified_image_name = imagename+"_" + \
                str(dt_timestamp)+" "+extension
            generated_name = FILEPATH+modified_image_name

            file_content = await product_image.read()

            with open(generated_name, "wb") as file:
                file.write(file_content)
                file.close()
            # image_url = generated_name

            product_obj = await Product.create(
                product_image=generated_name,
                selling_price=data.selling_price,
                discount_price=data.discount_price,
                description=data.description,
                category=category_obj,
                subcategory=subcategory_obj,
                brand=data.brand,
                product_name=data.product_name,
                # slug=slug
            )

            if product_obj:

                return{"status": True, "message": "product added"}
            else:
                return{"status": False, "message": "something wrong"}
            


@router.get('/allproduct/')
async def get_procat():
    pro = await Product.all()
    return pro


@router.put("/up_category/")
async def update_category_details(data:categoryUpdate=Depends(),category_image: UploadFile=File(...)):
    if await Category.exists(id=data.id):
        slug = slugify(data.name)

        FILEPATH = 'static/images/category/'

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = category_image.filename
        extention = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extention not in ['png', 'jpg', 'jpeg']:
            return {'status': 'error', "details": 'file extension not allowed'}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+" "+str(dt_timestamp)+" "+extention
        generated_name = FILEPATH+modified_image_name
        file_content = await category_image.read()

        with open(generated_name, "wb") as file:
            file.write(file_content)
            file.close()
        # image_url=generated_name

        cat_obj = await Category.filter(id=data.id).update(
            category_image=generated_name,
            description=data.description,
            name=data.name,
            slug=slug
        )

        if cat_obj:
            return {"status": True, "message": " category updated"}
        else:
            return {"status": False, "message": " something wrong"}
        


@router.delete("/delete_category/")
async def read_item(data:categoryDelete):
    delete_category=await Category.filter(id=data.category_id).delete()
    return{"massage":"category deleted sucessfully"}


@router.put("/up_subcategory/")
async def update_subcategory_details(data:subcategoryUpdate=Depends(),category_image: UploadFile=File(...)):

    if await SubCategory.exists(id=data.id):
        category= await Category.get(id=data.category_id)
        slug = slugify(data.name)

        FILEPATH = 'static/images/subcategory/'

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = category_image.filename
        extention = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extention not in ['png', 'jpg', 'jpeg']:
            return {'status': 'error', "details": 'file extension not allowed'}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+" "+str(dt_timestamp)+" "+extention
        generated_name = FILEPATH+modified_image_name
        file_content = await category_image.read()

        with open(generated_name, "wb") as file:
            file.write(file_content)
            file.close()
        # image_url=generated_name

        subcat_obj = await SubCategory.filter(id=data.id).update(
            subcategory_image=generated_name,
            description=data.description,
            category=category,
            name=data.name,
            slug=slug
        )

        if subcat_obj:
            return {"status": True, "message": " subcategory updated"}
        else:
            return {"status": False, "message": " something wrong"}


@router.put("/up_product/")
async def update_product_details(data:updateproductitem=Depends(),category_image: UploadFile=File(...)):

    if await Product.exists(id=data.id):
        category= await Category.get(id=data.category_id)
        subcategory=await SubCategory.get(id=data.subcategory_id)
        slug=data.product_name

        FILEPATH = 'static/images/product/'

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = category_image.filename
        extention = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extention not in ['png', 'jpg', 'jpeg']:
            return {'status': 'error', "details": 'file extension not allowed'}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+" "+str(dt_timestamp)+" "+extention
        generated_name = FILEPATH+modified_image_name
        file_content = await category_image.read()

        with open(generated_name, "wb") as file:
            file.write(file_content)
            file.close()
        # image_url=generated_name

        pro_obj = await Product.filter(id=data.id).update(
            product_image=generated_name,
            description=data.description,
            category=category,
            subcategory=subcategory,
            product_name=data.product_name,
            
        )

        if pro_obj:
            return {"status": True, "message": " product updated"}
        else:
            return {"status": False, "message": " something wrong"}
      



@router.post('/admin.registration',)
async def create_admin(data:Useradmin):
    try:
        try:
            valid=validate_email(data.email)
        except EmailNotValidError as e:
            return { "status":False, "message":"invalid email id"}
        if len(data.mobile)!=10:
            return { "status":False, "message":"invalid number"}

        if await Admin.exists(mobile=data.mobile):
            { "status":False, "message":"This number already register"}
        elif await Admin.exists(email=data.email):
            { "status":False, "message":"email already register"}
        else:
            add_user=await Admin.create(email=data.email,full_name=data.fullname,mobile=data.mobile,password=get_password_hash(data.password))
        return JSONResponse({
            "status":True,
            "message":"Registered Successfully"
        })
    except Exception as e:
        return JSONResponse({
            "status":True,
            "message":"Registered Successfully"
        })
    

@manager.user_loader()
async def load_user(email:str):
    if await Admin.exists(email=email):
        user=await Admin.get(email=email)
        return user

@router.post('/admin_login/')
async def login(data:AdminLogin):
    print(data.email)
    email=data.email
    user=await load_user(email)

    if not user:
        return JSONResponse({'status':False,'message':'user not registered'},status_code=403)         
    elif not verify_password(data.password,user.password):
        return JSONResponse({'status':False,'message':'invalid password'},status_code=403)         
    access_token=manager.create_access_token(data={'sub':jsonable_encoder(user.email),'full_name':jsonable_encoder(user.full_name),'mobile':jsonable_encoder(user.mobile)})
    new_dict=jsonable_encoder(user)
    new_dict.update({'access_token':access_token})
    res=Token(access_token=access_token,token_type='bearer')
    print(res)
    return res