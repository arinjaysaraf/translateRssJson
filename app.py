from googletrans import Translator
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import os
import json
from dotenv import load_dotenv 
import requests


load_dotenv()

app = FastAPI()

api_uri = os.getenv("API_URI")

origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)

class translationClass(BaseModel): 
    jsonData:dict
    title: str
    createdAt:str
@app.post("/")
async def getTrans(translation:translationClass):
    finalDict = {}
    res=""
    thumbnail = []
    print(translation.jsonData)
    print(type(translation.jsonData))
    for i in translation.jsonData:
        print(translation.jsonData[i])
        print('\n')
        if translation.jsonData[i] == "" :
            break

        if "https" in translation.jsonData[i] :
            thumbnail.append(translation.jsonData[i]) 
        else:
            print(type(res))
            res += translation.jsonData[i] + '#$#'
    
    
    translatedLangs = {}
    if(len(thumbnail)>0):
        translatedLangs["thumbnail"] = thumbnail[0]
        if(len(thumbnail)>1):
            translatedLangs["thumbnail"] = thumbnail[0]
        translatedLangs["img"] = thumbnail[1:]
    else:
        translatedLangs["thumbnail"] = "https://ik.imagekit.io/sihassembly/sih-placeholder_cXgXA446y.png"
    translator = Translator()
    toLangs = ["hi","gu","kn","mr","ml","pa","ta","te","en"]
    for i in toLangs:
        translatedLangs[i] = translator.translate(res, dest=i).text
    finalDict["thumbnail"] = translatedLangs["thumbnail"]
    del translatedLangs["thumbnail"]
    finalDict["content"] = translatedLangs
    finalDict["slug"] = translation.title.lower().replace(" ", "-")
    finalDict["categories"] = ["Ministry"]
    finalDict["title"] = translation.title
    finalDict["createdAt"] = translation.createdAt
    print(finalDict)
    requests.post('http://localhost:5000/article/create', json=finalDict);

    return [{"translatedLangs" : translatedLangs}]

#   \n en English(India)
#   \n gu-IN Gujarati(India)
#   \n hi-IN Hindi(India) 
#   \n kn-IN Kannada(India) 
#   \n kok-IN Konkani(India) 
#   \n mr-IN Marathi(India) 
#   \n pa-IN Punjabi(India) 
#   \n sa-IN Sanskrit(India) 
#   \n ta-IN Tamil(India) 
#   \n te-IN Telugu(India)