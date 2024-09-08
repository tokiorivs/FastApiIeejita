from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, field_validator
from pydantic.types import constr
from datetime import date, time
import re

app = FastAPI()

class Identificacion(BaseModel):
    version: int = Field(defatult=1, description="Version")
    ambiente: str = Field(description= "Ambiente de destino", enum=["00", "01"])
    tipoDte: str = Field("01", description= "Tipo de  Documento")
    numeroControl: str =Field(
        min_length=31,
        max_length=31,
        pattern="^DTE-01-[A-Z0-9]{8}-[0-9]{15}$", 

        description="Número de Control")
    
class Version(BaseModel):
    version: int = Field(default=1, Literal=True)
class Ambiente(BaseModel):
    ambiente: str = Field(description= "Ambiente de destino", enum=["00", "01"])
class TipoDte(BaseModel):
    tipoDte: str = Field("01", description= "Tipo de Documento")
class NumeroControl(BaseModel):
    numeroControl: str = Field(
        min_length=31,
        max_length=31,
        pattern="^DTE-01-[A-Z0-9]{8}-[0-9]{15}$", 
        description="Número de Control"
    )
class CodigoGeneracion(BaseModel):
    #los ... indican que el codigo es requerido.
    codigoGeneracion: str = Field(
        ...,
        description="Código de Generación",
        min_length=36,
        max_length=36
    )

    @field_validator('codigoGeneracion')
    @classmethod
    #el patron regex asegura el formato de la a-f, 0-9 y 8,4,4,4,12 caracteres
    def validate_codigo_generacion(cls, v):
        pattern = r'^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$'
        if not re.match(pattern, v):
            raise ValueError('El código de generación no cumple con el formato requerido')
        return v  
class TipoModelo(BaseModel):
    tipoModelo: int = Field(description="Modelo de Facturación", ge=1, le=2)
class TipoContingencia(BaseModel):
    tipoContingencia: int | None = Field(
        default= None,
        ge=1,
        le=5,
        description="Tipo de Contingencia"
    )
class MotivoContin(BaseModel):
    motivoContin: str | None = Field(
        min_length = 5,
        max_length = 150
    )
class FecEmi(BaseModel):
    fecEmi: date = Field(
    ...,
    description = "Fecha de Generación",
    format='%Y-%m-%d'
    )
class HorEmi(BaseModel):
    horEmi: time = Field(
        ...,
        description="Horal de Generación",
        format= '%H:%M:%S'
    )
    @field_validator('horEmi')
    def validate_hora(cls, v):
        # Validación adicional para asegurar que el formato coincida con el patrón
        if str(v) != v.strftime('%H:%M:%S'):
            raise ValueError('Hora de emisión en formato inválido')
        return v
class TipoMoneda(BaseModel):
    tipoMoneda:str = Field(
        description= "Tipo de Moneda",
        enum=["USD"]
    )
class DocumentoRelacionado(BaseModel):
    documentoRelacionado:int = Field(default=1)
class Emisor(BaseModel):
    nit: str
    nrc: str
    nombre: str
    codActividad: str
    descActividad: str
    nombreComercial: str
    tipoEstablecimiento: str
    direccion: str
    telefono: str
    correo: str
    codEstable: int | None
    codPuntoVenta: int | None
    codEstableMH: str
    codPuntoVentaMH: str