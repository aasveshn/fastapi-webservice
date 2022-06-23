
from fastapi import FastAPI, UploadFile, File
from fastapi.encoders import jsonable_encoder
#from fastapi.testclient import TestClient

from dbmodels import Image
from db import metadata, database, engine

import uuid
from typing import List
import datetime

from minio import Minio
from minio.error import InvalidResponseError



#Minio client
def getMinioClient(access,secret):
    return Minio('localhost:9000', access_key=access, secret_key=secret, secure=False)

if __name__=='__main__':
    minioClient_c = getMinioClient('minioadmin', 'minioadmin')


app = FastAPI()

#db begin
metadata.create_all(engine)
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()

@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

#db end

@app.post("/frames/")
async def upload_image(files: List[UploadFile] = File(...)):
    data_d = {}
    counter = 0
    minioClient = getMinioClient('minioadmin', 'minioadmin')

    if (not minioClient.bucket_exists(str(datetime.date.today()))):
        try:
            minioClient.make_bucket(str(datetime.date.today()))
        except InvalidResponseError as identifier:
            raise
    for i in files:
        if counter>14:
            return data_t

        filename = str(uuid.uuid4())
        minioClient.put_object(str(datetime.date.today()), filename+'.jpg', i.file, -1, part_size=10485760)
        await Image.objects.create(name=filename)
        data_d[i] = jsonable_encoder((await Image.objects.get()))
        data_t = [(key, value) for key, value in data_d.items()]
        counter += 1
    return data_t

@app.get("/frames/{request_code}")
async def get_image(request_code: int):
    return await Image.objects.get(pk=request_code)

@app.delete("/frames/{request_code}")
async def delete_image(request_code: int):
    image = await Image.objects.get(pk=request_code)
    minioClient_r=getMinioClient('minioadmin', 'minioadmin')
    try:
        minioClient_r.remove_object(str(image.registration_date.date()), image.name+'.jpg')
    except InvalidResponseError as indetifier:
            raise
    return await Image.objects.delete(pk=request_code)