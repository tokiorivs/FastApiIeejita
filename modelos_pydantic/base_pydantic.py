from fastapi import FastAPI
from datetime import datetime, time
from pydantic import BaseModel, Field, field_validator ,model_validator, EmailStr
from typing import Optional, Set
import re
from catalagos import *


app = FastAPI()
    
class Identificacion(BaseModel):
    version:int = Field(default=1, description="Version")
    ambiente:AmbienteDestino = Field(description="Ambiente de destino")
    tipoDte:TipoDocumento = Field( description="Tipo de Documento")
    numeroControl:str = Field(
        description= "Numero de control",
        max_length= 31,
        min_length= 31,
        pattern= r"^DTE-01-[A-Z0-9]{8}-[0-9]{15}$",
    )
    codigoGeneracion:str = Field(
        description= "Código de generación",
        max_length= 36,
        min_length= 36,
        pattern= r"^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$",
    )
    tipoModelo:ModeloFacturacion = Field(
        description= "Modelo de Facturación", 
        ge= 1,
        le= 2,
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
        max_length= 150,
        min_length= 5,
    )
    fecEmi:datetime= Field(description="Fecha de Generación")
    horEmi:time =Field(description="Hora de Generación")
    tipoMoneda: Usd = Field(description="Tipo de Moneda")
    
                    
class DocRelacionado(BaseModel):
    tipoDocumento:TipoDocumento = Field(description="Tipo de Documento Tributario Relacionado")
    tipoGeneracion:TipoGeneracionDocumento = Field(
        description="Tipo de Generación del Documeento Tributario relacionado",
        ge= 1,
        le= 2,
    )
    numeroDocumento: str = Field(
        description= "Número de docuemento relacionado",
        min_length= 1,
        max_length= 36,
    )
    fechaEmision:datetime = Field(description= "Fecha de Generacipon del documento relacionado")
    
    #validamos que solo se puedan ingresar como tipo de documento los valores 04 y 09
    @field_validator("tipoDocumento")
    def verificacionDocumento(cls, v ):
        if v != TipoDocumento.notaRemision and v != TipoDocumento.docContableLiquidacion:
            raise ValueError("los valores permitidos para el tipo de Documento es 04, 09")
    
    #validamos las condiciones si el documento es fisico o electronico
    @model_validator(mode="after")
    def tipoGeneracion(self):
        if self.tipoGeneracion == 1:
            if len(self.numeroDocumento) > 20:
                raise ValueError("el numero de documento no puede tener mas de 20 caracteres")
        elif self.tipoGeneracion == 2:
            patronDoc = re.compile(r'^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$')
            if not patronDoc.match(str(self.numeroDocumento)):
                raise ValueError("el numero del documento no cumple con el patron")
        
        return self
    
class Direccion(BaseModel):
    departamento:Departamento = Field(
        pattern = r"^0[1-9]|1[0-4]$",
        description= "Dirección Departamento",
    )
    municipio:Municipio = Field(
        pattern= r"^[0-9]{2}$",
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
        if not patternMuni.match(str(municipio)):
            raise ValueError(f"Cambie el Municipio para que concuerde con el patron {patronMuni}")

    #validamos los departamentos con sus respectiovos patrones de codigo  
    @model_validator(mode="after")
    def DepartamentoValidation(self):
        municipio = self.municipio
        match self.departamento:
            case "01":
                patternMuni= r'^0[1-9]|1[0-2]$'
                self.caseValidator(patternMuni, municipio)
            case "02" | "10":
                patternMuni= r"^0[1-9]|1[0-3]$"
                self.caseValidator(patternMuni, municipio)
            case "03" | "07":
                patternMuni= r"^0[1-9]|1[0-6]$"
                self.caseValidator(patternMuni, municipio)
            case "04":
                patternMuni= r"^0[1-9]|[12][0-9]|3[0-3]$"
                self.caseValidator(patternMuni, municipio)
            case "05" | "08":
                patternMuni= r"^0[1-9]|1[0-9]|2[0-2]$"
                self.caseValidator(patternMuni, municipio)
            case "06":
                patternMuni= r"^0[1-9]|1[0-9]$"
                self.caseValidator(patternMuni, municipio)
            case "09":
                patternMuni= r"^0[1-9]$"
                self.caseValidator(patternMuni, municipio)
            case "11":
                patternMuni= r"^0[1-9]|1[0-9]|2[0-3]$"
                self.caseValidator(patternMuni, municipio)
            case "12":
                patternMuni= r"^0[1-9]|1[0-9]|20$"
                self.caseValidator(patternMuni, municipio)
            case "13":
                patternMuni= r"^0[1-9]|1[0-9]|2[0-6]$"
                self.caseValidator(patternMuni, municipio)
            case "14":
                patternMuni= r"^0[1-9]|1[0-8]$"
                self.caseValidator(patternMuni, municipio)
         
        return self   


class Emisor(BaseModel):
    
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
    codEstableMH:Optional[str] = Field(
        min_length= 4,
        max_length= 4,
        description= "Código del establecimiento asignado por el MH", 
    )
    codEstable:Optional[str] = Field(
        min_length= 4,
        max_length= 4,
        description= "Código del establecimiento asignado por el contribuyente", 
    )
    codPuntoVentaMH:Optional[str] = Field(
        min_length= 4,
        max_length= 4,
        description= "Código del Punto de Venta (Emisor) asignado por el MH", 
    )
    codPuntoVenta:Optional[str] = Field(
        min_length= 1,
        max_length= 15,
        description= "Código del Punto de Venta (Emisor) asignado por el contribuyente", 
    )
class Receptor(BaseModel):
    tipoDocumento: TipoDocumentoReceptor = Field(
       description=   "Tipo de documento de identificación (Receptor)"
    ) 
    numDocumento: str = Field(
        min_length= 3,
        max_length= 20,
        description=  "Número de documento de Identificación (Receptor)",
    )
  
    nombre:str =Field(
        min_length= 1,
        max_length= 250,
        description= "Nombre, denominación o razón social del contribuyente (Receptor)",
    )
    
    descActividad:str = Field(
        min_length= 5, 
        max_length= 150,
        description="Actividad Económica (Receptor)"
    )
    telefono:str = Field(
        min_length= 8,
        max_length= 30,
        description= "Teléfono (Receptor)",
    )
    correo:EmailStr = Field(
        min_length= 3,
        max_length= 100,
        description= "Correo electrónico (Receptor)"
    )

class Medico(BaseModel):
    nombre: str = Field (
        max_length= 100,
        description="Nombre de médico que presta el Servicio")
    nit: Optional[str] = Field(
         pattern=r"^([0-9]{14}|[0-9]{9})$", 
         description="NIT de médico que presta el Servicio")
    docIdentificacion: Optional[str] = Field(
         min_length= 2,
         max_length= 25,
         description="Documento de identificación de médico no domiciliados")
    tipoServicio: TipoServicioMedico = Field(
        ge= 1,
        le= 6,
        description="Código del Servicio realizado")
    
    @model_validator(mode="after")
    def NitValidator(self):
        print(f'impriendo dentro de medico {self.nombre}')
        if self.nit == None and self.docIdentificacion == None:
            raise ValueError(f"Si no hay NIT, ingresa un Documento de Identificación")
        return self 
    
class OtroDocumento(BaseModel):
    codDocAsociado:int = Field(
        ge= 1,
        le= 4,
        description= "Documento asociado",
        #probablemente sea tipo de item verificar
    )
    descDocumento:Optional[str] = Field(
       max_length= 100, 
       description= "Identificación del documento asociado",
    )
    detalleDocumento:Optional[str] = Field(
        max_length= 300,
        description= "Descripción de documento asociado",
    )
    
    
class VentaTercero(BaseModel):
     nit:str = Field(
        pattern= "^([0-9]{14}|[0-9]{9})$",
        max_length= 14,
        description= "NIT por cuenta de terceros",
    )    
     nombre:str = Field(
         min_length= 1,
         max_length= 250,
         description= "Nombre, denominación o razoń social del Tercero",
     )

class ItemCuerpoDocumento(BaseModel):
    numItem:int = Field(
        ge= 1,
        le= 2000,
        description= "N° de item",
    )
  
    cantidad:float = Field(
        gt= 0,
        lt= 100000000000,
        multiple_of= 1e-08,
        description= "Cantidad"
    )
    codigo:Optional[str] = Field(
        min_length= 1,
        max_length= 25,
        description= "Código",
    )

    uniMedida:UnidadDeMedida = Field(
        ge= 1,
        le= 99,
        description= "Unidad de medida"
    )
    descripcion:str = Field(
        max_length= 1000,
        description= "Descripción",
    )
    
class ItemTributo(BaseModel):
    codigo:TributosAplicadosPorItemsReflejados = Field(
        min_length= 2,
        max_length= 2,
    )
    descripcion:str = Field(
        min_length= 2,
        max_length= 150,
        description= "Nombre del Tributo",
    )
    valor:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Valor del Tributo",
    )

class ItemPago(BaseModel):
    codigo: str = Field(
        max_length= 2,
        pattern= r"^(0[1-9]|1[0-4]|99)$",
        description= "Código de forma de pago",
    )
    montoPago:float  = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Monto por forma de pago",
    )
    referencia: Optional[str] = Field(
        max_length= 50,
        description= "Referencia de modalidad de pago",
    )
    
   
        
class Resumen(BaseModel):
  
    totalGravada: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total de Operaciones Gravadas",
    )
    porcentajeDescuento: float = Field(
        ge= 0,
        le= 100,  
        multiple_of= 0.01,
        description= "Porcentaje del monto global de Descuento, Bonificación, Rebajas y otros",
    )
    totalDescu: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total del monto de Descuento, Bonificación, Rebajas",
    )
    montoTotalOperacion: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Monto Total de la Operación",
    )
    totalNoGravado: float = Field(
        gt= -100000000000,  
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total Cargos/Abonos que no afectan la base imponible",
    )
    totalPagar: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total a Pagar",
    )
    totalLetras: str = Field(
        max_length= 200,
        description= "Valor en Letras",
    )
    condicionOperacion: int = Field(
        enum=[1, 2, 3],
        description="Condición de la Operación",
    )
 
    numPagoElectronico: Optional[str] = Field(
        max_length= 100,
        description= "Número de pago Electrónico"
    )
    
class Extension(BaseModel):
    nombEntrega:str = Field(
        min_length= 5,
        max_length= 100,
        description= "Nombre del responsable que Genera el DTE",
    )   
    docuEntrega:str = Field(
        min_length= 5,
        max_length= 25,
        description= "Documento de identificación de quien genera el DTE",
    )
    nombRecibe: str = Field(
        min_length= 5,
        max_length= 100,
        description= "Nombre del responsable de la operación por parte del receptor",
    )
    docuRecibe: str = Field(
        min_length= 5,
        max_length= 100,
        description= "Documento de identificación del responsable de la operación por parte del receptor",
    )
    observaciones: str = Field(
        max_length= 3000,
        description= "Observaciones",
    )
    placaVehiculo: Optional[str] = Field(
        max_length= 10,
        description= "Placa del Véhiculo",
    )
    
class ApendiceItems(BaseModel):
    campo:str = Field(
        max_length= 25,
        description= "Nombre del campo",
    )
    etiqueta:str = Field(
        max_length= 50,
        description= "Descripcion"
    )
    valor:str = Field(
       max_length= 150,
       description= "Valor/Dato" 
    )
 
# class DataVerificado(BaseModel):
#     identificacion: Identificacion
#     documentoRelacionado:Optional[list[DocRelacionado]] = Field(
#         default= None,
#         min_length= 1,
#         max_length= 10,
#         description= "Documentos Relacionados",
#     )
#     emisor:Emisor
#     receptor:Receptor 
#     otrosDocumentos:Optional[list[OtroDocumento]] = Field( 
#         default= None,
#         min_length= 1,
#         max_length=  10,
#         description= "Documentos Asociados",
#     )
#     ventaTercero:Optional[VentaTercero] = Field( 
#         description= "Ventas por cuenta de terceros"
#     )
#     cuerpoDocumento:list[ItemCuerpoDocumento] = Field(
#         min_items =1,
#         max_items=2000
#     )
#     resumen:Resumen
#     extension:Optional[Extension]
#     apendice: list[ApendiceItems]
    
#     @model_validator(mode="after")
#     def MontoTotalOperacionValidator(self):
#         if self.resumen.montoTotalOperacion > 1095:
#             if self.receptor.tipoDocumento == None:
#                 raise ValueError("el TipoDocumento no puede ser None")
#             if self.receptor.numDocumento == None:
#                 raise ValueError("el numDocumento no puede ser None")
#             if self.receptor.nombre == None:
#                 raise ValueError("el nombre no puede ser None")
            
# #importamos la data para la verificacion
# data = data_fe

# try: 
#     data_validada = DataVerificado(**data)
#     print("Se valido correctamente")
#     print(data)
# except ValueError as e:
#     print(f'Error de validadcion: {e}')