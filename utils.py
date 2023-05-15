from fastapi.encoders import jsonable_encoder as fastapi_jsonable_encoder
from bson import ObjectId
from functools import partial


jsonable_encoder = partial(fastapi_jsonable_encoder,custom_encoder={
    ObjectId:str
})
