from fastapi import FastAPI
import re
from base_pydantic import *
from cde_data import data_cde
from catalagos import *

app = FastAPI()

class IdentificacionCde(Identificacion):
    tipoDte:str = Field(
        default= "15",
    )
    numeroControl:str = Field(
        pattern= r"^DTE-15-[A-Z0-9]{8}-[0-9]{15}$",
    )
    #validamos que el comprobante sea de tipo cfe
    @model_validator(mode= "after")
    def TipoDteValidator(self):
        comprobanteDonacion = TipoDocumento.comprobanteDonacion.value
        if self.tipoDte != comprobanteDonacion:
            raise ValueError( f"para el Cde el tipoDte debe ser {comprobanteDonacion}")
        return self

class Donatario(Emisor):

    tipoDocumento:TipoDocumentoReceptor = Field(
       default= 36,
       description= "Tipo de documento de identificación (Emisor) ",
    )
    numDocumento:str = Field(
        max_length= 14,
        min_length= 9,
        description= "Número de documento de Identificación (Emisor)",
    )
    descActividad:str = Field(
        min_length= 1, 
    )
    nombreComercial:str = Field(
        min_length= 1, 
    )

class Donante(BaseModel):
    tipoDocumento:TipoDocumento = Field(description="Tipo de Documento Tributario Relacionado")
    numDocumento: str = Field(
        description= "Número de docuemento relacionado",
        min_length= 3,
        max_length= 36,
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
        min_length= 1,
        max_length= 6,
        description="Código de Actividad Económica (Emisor)"
    )
    descActividad:str = Field(
        min_length= 1, 
        max_length= 150,
        description="Actividad Económica (Emisor)"
    )
    direccion:Optional[Direccion]
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
    codDomiciliado:DomicilioFiscal = Field(
        ge= 1,
        le= 2,
    )
    codPais:CodPais = Field(
        description= "Codigo de Pais, catalogo 020",
    )
    @model_validator(mode= "after")
    def codDomiciliadoValidator(self):
        if self.codDomiciliado == 1:
            if self.direccion == None:
                raise ValueError(f"cuando codDomiciliado es 1, la direccion no puede ser None  ")
        else:
            if self.direccion != None:
                raise ValueError("cuando el codDomicilado es 2,la direccion debe ser None ")
            elif self.codActividad != None:
                raise ValueError("cuando el codDomicilado es 2,la codActivada debe ser None ")
            elif self.descActividad != None:
                raise ValueError("cuando el codDomicilado es 2, la descActividad debe ser None")
        return self

class OtroDocumentoCde(OtroDocumento):
    codDocAsociado:int = Field(
        ge= 1,
        le= 2,
        #probablemente sea tipo de item verificar
    )
    descDocumento:str  
    detalleDocumento:str  

class ItemCuerpoDocumentoCde(ItemCuerpoDocumento):
    tipoDonacion:TipoDonacion = Field(
       description= "Tipo Donación" 
    )
    descripcion:str = Field(
        min_length= 1,
        description= "Descripción",
    )
    depreciacion:float = Field(
        ge = 0,
        lt= 100000000000,
        multiple_of= 1e-08,
        description= "Depreciación"
    )
    valorUni:float = Field(
        ge = 0,
        lt =  100000000000,
        multiple_of= 1e-08,
        description= "Valor Unitario",
    )
    valor:float = Field(
        ge= 0,
        lt =  100000000000.0,
        multiple_of= 1e-08,
    )
    @model_validator(mode= "after")
    def tipoDonacionValidator(self):
        if self.tipoDonacion == 1 or self.tipoDonacion == 3:
            if self.depreciacion != 0:
                raise ValueError("cuando el tipoDonacion es 1 o 3, la depreciacion debe ser 0")
            if self.uniMedida != 99:
                raise ValueError(f"cuando el tipoDonacion es 1 o 3, la uniMedida debe ser 99 {UnidadDeMedida.otra}")
        else:
            if self.depreciacion >= 0:
                raise ValueError("la depreciacion debe ser igual o mayor a 0")        
        return self

class ItemPagoCde(ItemPago):
    codigo:Optional[str] = Field(
    max_length= 2,
    pattern= r"^(0[1-9]|1[0-4]|99)$",
    description= "Código de forma de pago",
    )  


class ResumenCde(BaseModel):
    valorTotal:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total de la donación",
    )
    totalLetras:str = Field(
        max_length= 200,
        description= "Total en Letras",
    )
    pagos:Optional[list[ItemPagoCde]] = Field(
        min_items = 1,
        description= "Pagos"
    )

class ApendiceItemsCde(ApendiceItems):
    campo:str = Field(
        min_length= 2,
    )
    etiqueta:str = Field(
        min_length= 3,
    )
    valor:str = Field(
         min_length= 1,
    )

class CdePydantic(BaseModel):
    identificacion:IdentificacionCde
    donatario:Donatario = Field(
        description= "Emisor"
    )
    donante:Donante
    otrosDocumentos:list[OtroDocumentoCde] = Field(
        min_length= 1,
        max_length= 10,
        description= "Documentos Asociados",
    )
    cuerpoDocumento:list[ItemCuerpoDocumentoCde] = Field(
        min_length= 1,
        max_length= 2000,
    )
    resumen:ResumenCde
    apendice:Optional[list[ApendiceItemsCde]] = Field(
        description= "Apéndice",
        min_length= 1,
        max_length= 10,
    )

   #este model hay que verificar la logica 
    @model_validator(mode= "after")
    def TipoDonacionValidator(self):
        for item in self.cuerpoDocumento:
            if item.tipoDonacion == 1:
                for item in self.resumen.pagos:
                    if item.codigo == None:
                        raise ValueError("cuando el tipoDonacion es 1, el codigo no puede ser None")
                for item in self.resumen.pagos:
                    if item.referencia == None:
                        raise ValueError("cuando el tipoDonacion es 1, la referencia nue puede ser None")

                    
    
data = data_cde

try: 
    data_validada = CdePydantic(**data)
    print("Se valido correctamente")
    print(data_cde)
except ValueError as e:
    print(f'Error de validadcion: {e}')