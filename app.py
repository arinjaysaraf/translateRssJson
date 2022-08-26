from googletrans import Translator
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv 


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

@app.post("/")
async def getTrans(translation:translationClass):
    res=""
    thumbnail = []
    for i in translation.jsonData:
        print(translation.jsonData[i])
        print('\n')
        if translation.jsonData[i] == "" :
            break

        if "https" in translation.jsonData[i] :
            thumbnail.append(translation.jsonData[i]) 
        else:
            res += translation.jsonData[i] + '#$#'
    print(res)
    
    toLangs = ["hi","gu","kn","mr","ml","pa","ta","te","en"]
    translatedLangs = {}
    translatedLangs["thumbnail"] = thumbnail[0]
    translatedLangs["img"] = thumbnail[1:]
    translator = Translator()
    for i in toLangs:
        translatedLangs[i] = translator.translate(res, dest=i).text
    print(translatedLangs)


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