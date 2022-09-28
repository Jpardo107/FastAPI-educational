#Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

#pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#fastapi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

app = FastAPI()

#Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=16
        )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)
    
class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=16
        )

class Tweet(BaseModel):
    tweet_id: UUID= Field(...)
    content: str = Field(
        ...,
        min_length =1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    update_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

#Path Operations

##Users

@app.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary= 'Register a user',
    tags=['Users']
)
def SignUp(user:UserRegister = Body(...)):
    """
    SignUp a Users

    This path operation registar a users in the app
    Parameters:
        - Request body parameters:
            - **user:UserRegister**
    Returns a json with the basic user information:
        -user_id: UUID
        -email: EmailStr
        -first_name: str
        -last_name: str
        -birth_date: datetime
    """  
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

@app.post(
    path='/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary= 'Login a user',
    tags=['Users']
)
def Login():
    pass

@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary= 'Show all users',
    tags=['Users']
)
def ShowAllUsers():
    """
    this path operations show all users registered in the app
    Parameters:
        - None
    Return a json list with all the users, with the followin keys:
        -user_id: UUID
        -email: EmailStr
        -first_name: str
        -last_name: str
        -birth_date: datetime
    """    
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


@app.get(
    path='/users{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary= 'Show a user',
    tags=['Users']
)
def ShowAUsers():
    pass

@app.delete(
    path='/users{user_id}/delete',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary= 'Delete a user',
    tags=['Users']
)
def DeleteAUsers():
    pass

@app.put(
    path='/users{user_id}/update',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary= 'update a user',
    tags=['Users']
)
def UpdateAllUsers():
    pass

##Tweets

@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary= 'Show all tweets',
    tags=['Tweet']
    )
def Home():
    """
    This path operations show all users registered in the app
    Parameters:
        - None
    Return a json list with all the users, with the all of tweets registered in the app
    """ 
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

@app.post(
    path='/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary= 'Post a Tweet',
    tags=['Tweet']
)
def PostATweet(tweet: Tweet = Body(...)):
    """
    This path operation post a tweet in the app

    Parameters:
    - Request body parameters:
        - **tweet:Tweet**

    Returns a json with the tweet information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - update_at: Optional[datetime]
    - by: User
    """  
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict['created_at'])
        tweet_dict['update_at'] = str(tweet_dict['update_at'])
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict['by']['birth_date'])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

@app.get(
    path='/tweet/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'Show a Tweet',
    tags=['Tweet']
)
def GetATweet():
    pass

@app.delete(
    path='/tweet/{tweet_id}/delete',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'Delete a Tweet',
    tags=['Tweet']
)
def DeleteATweet():
    pass

@app.put(
    path='/tweet/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary= 'Update a Tweet',
    tags=['Tweet']
)
def UpdateATweet():
    pass