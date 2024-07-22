"""Main module."""
import warnings
warnings.filterwarnings('ignore')

from typing import Dict, List, Optional, Union, Annotated
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi import UploadFile, File, Form, Body, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette import status
#import aiofiles
from sqlalchemy.orm import Session 
#from PIL import Image
#import base64
#from io import BytesIO

from src.base import BaseClass
from src.logger import logger
#from src.ocr import extract_text, perform_ocr
from src.gemini import chat_with_gemini, chat_with_gemini_old, call_gemini_api
from src.gemini import transaction_based_prompt
#from src.restapi_models import (DocItem,
#                              QuestionAnswerItem,
#                              ProcessDocItem)

from src.db.db import get_db
from src.db import schemas, crud
#from src.db import default_record_create

#default_record_create.create_default_recommend_product()
db_dependency = Annotated[Session, Depends(get_db)]
baseclass_obj = BaseClass()
app = FastAPI()


class Item(BaseModel):
    text: str

class CompItem(BaseModel):
    product_category: List[str]

class UserItem(BaseModel):
    mail: str


# Load the product data
products_df = pd.read_csv("sample_data/tanishq_product_structured_data.csv")
products_df.fillna('No Information', inplace=True)

# Load Complementary product data
complementary_products_df = pd.read_csv('sample_data_csv/complementary_products.csv')

# Load user transaction data
user_transaction_df = pd.read_csv('sample_data_csv/user_transaction.csv')

# Load Complementary product data
new_products_df = pd.read_csv('sample_data_csv/new_products.csv')


@app.get("/")
def read_root():
    '''
    ROOT.
    '''
    logger.info(f"root API.")

    return {"Hello": "you made it."}


@app.post("/user/signup/", status_code=status.HTTP_201_CREATED, tags=["user singn-up/sign-in"])
async def create_user(db: db_dependency, user: schemas.UserCreate):
    db_user = crud.get_user(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    return crud.create_user(db,user=user)


@app.post("/get_answer_given_question/")
async def get_answer_given_question(item:Item):
    '''
    get_answer_given_question.
    '''
    response = chat_with_gemini(item.text)

    return json.loads(response)


@app.post("/get_complementary_products/")
async def get_complementary_products(item:CompItem):
    '''
    get_complementary_products
    '''
    comp_filter = complementary_products_df[complementary_products_df['product_category'].isin(item.product_category)]
    comp_filter_records = comp_filter.to_dict('records')

    return comp_filter_records


@app.post("/get_content_based_recommendation/")
async def get_content_based_recommendation(item:UserItem):
    '''
    get_content_based_recommendation.
    '''
    user_filter_df = user_transaction_df[user_transaction_df['name']==item.mail]
    user_filter_list = user_filter_df.to_dict('records')
    new_products_list = new_products_df.to_dict('records')
    transaction_based_prompt_new = transaction_based_prompt.format(transaction_records=user_filter_list, new_products_records=new_products_list)
    response = await call_gemini_api(transaction_based_prompt_new)
    product_ids = json.loads(response)

    # filter dataframe
    prod_tobe_recmd_df = new_products_df[new_products_df['product_id'].isin(product_ids)]
    prod_tobe_recmd = prod_tobe_recmd_df.to_dict('records')

    return prod_tobe_recmd


@app.post("/get_recommendations_based_preference/")
async def get_recommendations_based_preference(item: Dict):
    '''# Define a function to generate product recommendations'''
    tmp = {'gender':'Gender','product_category':'file_name'}
    new_df_list = []
    target_strings = dict()
    for key in tmp:
        if item.get(key,None):
            target_strings[tmp.get(key)] = item.get(key)

    if len(target_strings) != 0:
        # Check if all specified columns contain the target strings
        mask = products_df.apply(lambda row: all(row[col].lower().find(target.lower()) != -1 for col, target in target_strings.items()), axis=1)
        final_df = products_df[mask]

        if target_strings.get('Gender',None):
            mask = final_df['Gender'].str.lower() == target_strings.get('Gender').lower()
            final_df = final_df[mask]
        
        if len(final_df) == 0:
            mask = products_df.apply(lambda row: all(row[col].lower().find(target.lower()) != -1 for col, target in target_strings.items()), axis=1)
            final_df = products_df[mask]
    else:
        final_df = pd.DataFrame()
    
    if len(final_df) == 0:
        new_df_list.append(products_df)
        final_df = pd.concat(new_df_list, ignore_index=True)
        final_df.drop_duplicates(inplace=True)

    # Return the top 10 products
    return final_df.head(10).to_dict('records')
