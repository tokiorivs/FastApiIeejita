from fastapi import FastAPI
from datetime import datetime, time
from pydantic import BaseModel, Field, field_validator ,model_validator, EmailStr
from typing import Optional, Set
import re
from catalagos import *
from fexe_data import data_fe
from extracode import *

app = FastAPI()

class Identificacion(BaseModel):
    version:int = Field(default=1, description="Version")
    ambiente:AmbienteDestino = Field(description="Ambiente de destino")
    tipoDte:TipoDocumento = Field(default="11", description="Tipo de Documento")
    numeroControl:str = Field(
        description= "Numero de control",
        max_length= 31,
        min_length= 31,
        pattern= "^DTE-11-[A-Z0-9]{8}-[0-9]{15}$"
    )
    codigoGeneracion:str = Field(
        description="Código de generación",
        max_length= 36,
        min_length= 36,
        pattern= "^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$"
    )
    tipoModelo:ModeloFacturacion = Field(
        description= "Modelo de Facturación", 
        ge= ModeloFacturacion.modeloFacturacionPrevio, 
        le= ModeloFacturacion.modeloFacturacionDiferido,
    )
    #podran ingresar numeros mayores iguales a 1, y menores iguales a 2, formato entero
    tipoOperacion:TipoTransmision = Field(
        description="Tipo de transmisión",
        ge= 1,
        le= 2,
    )
    #Optional le indica que puede ser un valor None o un int en este ejemplo
    #podran ingresar numeros mayores iguales a 1, y menores iguales a 5, formato entero
    tipoContingencia:Optional[TipoContingencia] = Field(
        description="Tipo de Contingencia",
        ge= 1,
        le= 5,
    )
    motivoContin:Optional[str] = Field(
        description="Motivo de  Contingencia",
        max_length= 500,
        min_length= 1,
    )
    fecEmi:datetime= Field(description="Fecha de Generación")
    horEmi:time =Field(description="Hora de Generación")
    tipoMoneda: Usd = Field(description="Tipo de Moneda")
    
    #validacion de los campos de contingencia y su coherencia entre ellos
    @model_validator(mode="after")
    def ValidadorOperacion(self):
        #validamos si es una transmision normal los campos de contingencia y motivo deben ser nulos
        if self.tipoOperacion == 1: 
            if self.tipoModelo != 1:
                raise ValueError("cuando el tipoOperacion es 1, el tipoModelo debe ser 1")
            elif self.tipoContingencia != None:
                raise ValueError(f"cuando el tipoOperacion es 1, el tipo de contingencia deben ser null o None")
            elif self.motivoContin != None :
                raise ValueError("cuando el tipoOperacion es 1, el motivo de contingencia debe ser null or None") 
        elif self.tipoModelo != 2:
            raise ValueError("cuando el tipoOperacion es 2, el tipoModelo debe ser 2 ")
        elif self.tipoContingencia == 5:
            if self.motivoContin == None:
                raise ValueError("cuando el tipoContingencia es 5, el motivoContingencia no puede ser None")

class Direccion(BaseModel):
    departamento:Departamento = Field(
        pattern = "^0[1-9]|1[0-4]$",
        description= "Dirección Departamento",
    )
    municipio:Municipio = Field(
        pattern= "^[0-9]{2}$",
        description=  "Dirección Municipio",
    )
    complemento:str = Field(
        min_length= 5,
        max_length= 200,
        description= "Dirección complemento",
    )
     #funcion para simplificar el departamentoValidation    
    def caseValidator(self, patronMuni, municipio):
        patternMuni = re.compile(rf'{patronMuni}')
        print(patternMuni)
        if not patternMuni.match(str(municipio)):
            raise ValueError(f"Cambie el Municipio para que concuerde con el patron {patronMuni}")
        
    #validamos los departamentos con sus respectiovos patrones de codigo  
    @model_validator(mode="after")
    def DepartamentoValidation(self):
        municipio = "hola mundo"
        match self.departamento:
            case "01":
                patternMuni=r"^0[1-9]|1[0-2]$"
                self.caseValidator(patternMuni, municipio)
            # case "02" | "10":
            #     patternMuni= "^0[1-9]|1[0-3]$"
            #     caseValidator(patternMuni, municipio)
            # case "03" | "07":
            #     patternMuni= "^0[1-9]|1[0-6]$"
            #     caseValidator(patternMuni, municipio)
            # case "04":
            #     patternMuni= "^0[1-9]|[12][0-9]|3[0-3]$"
            #     caseValidator(patternMuni, municipio)
            # case "05" | "08":
            #     patternMuni= "^0[1-9]|1[0-9]|2[0-2]$"
            #     caseValidator(patternMuni, municipio)
            # case "06":
            #     patternMuni= "^0[1-9]|1[0-9]$"
            #     caseValidator(patternMuni, municipio)
            # case "09":
            #     patternMuni= "^0[1-9]$"
            #     caseValidator(patternMuni, municipio)
            # case "11":
            #     patternMuni= "^0[1-9]|1[0-9]|2[0-3]$"
            #     caseValidator(patternMuni, municipio)
            # case "12":
            #     patternMuni= "^0[1-9]|1[0-9]|20$"
            #     caseValidator(patternMuni, municipio)
            # case "13":
            #     patternMuni= "^0[1-9]|1[0-9]|2[0-6]$"
            #     caseValidator(patternMuni, municipio)
            # case "14":
            #     patternMuni= "^0[1-9]|1[0-8]$"
            #     caseValidator(patternMuni, municipio)
            


class Emisor(BaseModel):
    #verificar el numero de caracteres del nit si pueden ser menores
    nit:str = Field(
        pattern= "^([0-9]{14}|[0-9]{9})$",
        max_length= 14,
        description= "NIT (emisor)",
    )
    nrc:str = Field(
        pattern= "^[0-9]{1,8}$",
        min_length= 2,
        max_length= 8,
        description=("NRC (emisor)"),
    )
    nombre:str =Field(
        min_length= 1,
        max_length= 250,
        description= "Nombre, denominación o razón social del contribuyente (Emisor)",
    )
    codActividad:str = Field(
        pattern= "^[0-9]{2,6}$",
        min_length= 5,
        max_length= 6,
        description="Código de Actividad Económica (Emisor)"
    )
    descActividad:str = Field(
        min_length= 5, 
        max_length= 150,
        description="Actividad Económica (Emisor)"
    )
    nombreComercial:str = Field(
        max_length= 150,
        min_length= 5, 
        description= "Nombre Comercial (Emisor)", 
    )
    tipoEstablecimiento:TipoEstablecimiento = Field(
        description= "Tipo de establecimiento (Emisor)"
    )
    direccion:Direccion
    telefono:str = Field(
        min_length= 8,
        max_length= 30,
        description= "Teléfono (Emisor)",
    )
    correo:EmailStr = Field(
        min_length= 3,
        max_length= 100,
        description= "Correo electrónico (Emisor)"
    )
    codEstableMH:str= Field(
        min_length= 4,
        max_length= 4,
        description= "Código del establecimiento asignado por el MH", 
    )
    codEstable:str = Field(
        min_length= 4,
        max_length= 4,
        description= "Código del establecimiento asignado por el contribuyente", 
    )
    codPuntoVentaMH:str = Field(
        min_length= 4,
        max_length= 4,
        description= "Código del Punto de Venta (Emisor) asignado por el MH", 
    )
    codPuntoVenta:str = Field(
        min_length= 1,
        max_length= 15,
        description= "Código del Punto de Venta (Emisor) asignado por el contribuyente", 
    )
    #verificar en el schema son 3, en tipoItem son 4, lo mas seguro es que sea ese.
    tipoItemExpor:TipoItem = Field(
       description=  "Tipo de ítem",
    )
    recitoFiscal:str = Field(
        min_length= 2,
        max_length= 2,
        description= "Recinto fiscal"
    )
    regimen:str = Field(
        min_length= 1, 
        max_length= 13,
        description= "Régimen de exportación"
    )
    @model_validator(mode= "after") 
    def TipoExporValidator(self):
        if self.tipoItemExpor == 2:
            if self.recitoFiscal != None and self.regimen != None:
                raise ValueError("cuando el tipoItemExport es 2, recintoFiscal y regimen deben ser None")

class DataVerificado(BaseModel):
    identificacion: Identificacion
    # documentoRelacionado:Optional[list[DocRelacionado]] = Field(
    #     default= None,
    #     min_length= 1,
    #     max_length= 10,
    #     description= "Documentos Relacionados",
    # )
    emisor:Emisor
    # receptor:Receptor 
    # otrosDocumentos:Optional[list[OtroDocumento]] = Field( 
    #     default= None,
    #     min_length= 1,
    #     max_length=  10,
    #     description= "Documentos Asociados",
    # )
    # ventaTercero:Optional[VentaTercero] = Field( 
    #     description= "Ventas por cuenta de terceros"
    # )
    # cuerpoDocumento:list[ItemCuerpoDocumento] = Field(
    #     min_items =1,
    #     max_items=2000
    # )
    # resumen:Resumen
    # extension:Optional[Extension]
    # apendice: list[ApendiceItems]
    
#importamos la data para la verificacion
data = data_fe

try: 
    data_validada = DataVerificado(**data_fe)
    print("Se valido correctamente")
    print(data)
except ValueError as e:
    print(f'Error de validadcion: {e}')