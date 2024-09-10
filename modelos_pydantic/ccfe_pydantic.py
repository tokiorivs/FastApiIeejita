from fastapi import FastAPI
import re
from base_pydantic import *
from cde_data import data_cde
from catalagos import *

app = FastAPI()

