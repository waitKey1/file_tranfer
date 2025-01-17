# -*- coding: UTF-8 -*-
'''
@Project :AIProject 
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/18 2:58 
@Describe:
'''
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import List
import os
import shutil
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的来源
    allow_credentials=True,  # 支持cookie跨域
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)


# 存储上传文件的目录
UPLOAD_DIRECTORY = "./uploaded_files"

# 确保上传目录存在
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"message": "文件上传成功"}

@app.get("/files")
async def list_files():
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append({"name": filename})
    return files

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    raise HTTPException(status_code=404, detail=f"文件 {filename} 未找到")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10001)