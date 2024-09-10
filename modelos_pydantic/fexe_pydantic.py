from fastapi import FastAPI
import re
from base_pydantic import *
from fexe_data import data_fe

app = FastAPI()

class IdentificacionFexe(Identificacion):
    numeroControl:str = Field(
        pattern= "^DTE-11-[A-Z0-9]{8}-[0-9]{15}$"
    )
    motivoContin:Optional[str] = Field(
        max_length= 500,
    )
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
        return self

class EmisorFexe(Emisor):
    nit:str = Field(
        pattern= "^([0-9]{14}|[0-9]{9})$",
        max_length= 14,
        description= "NIT (emisor)",
    ) 
    tipoItemExpor:TipoItem = Field(
       description=  "Tipo de ítem",
    )
    recintoFiscal:Optional[str] = Field(
        min_length= 2,
        max_length= 2,
        description= "Recinto fiscal"
    )
    regimen:Optional[str] = Field(
        min_length= 1, 
        max_length= 13,
        description= "Régimen de exportación"
    )
    @model_validator(mode= "after") 
    def TipoExporValidator(self):
        if self.tipoItemExpor == 2:
            if self.recintoFiscal != None and self.regimen != None:
                raise ValueError("cuando el tipoItemExport es 2, recintoFiscal y regimen deben ser None")
        
class ReceptorFexe(Receptor):
    nombre:str = Field(
        min_length= 1,
        max_length= 250,
        description= "Nombre, denominación o razón social del contribuyente (Receptor)",
    )
    nombreComercial:str = Field(
        min_length= 1,
        max_length= 150,
        description= "Nombre, denominación o razón social del contribuyente (Receptor)",
    )
    codPais:CodPais = Field(
        description=  "Código de país (receptor)",                      
    )
    nombrePais:str =Field(
        min_length= 3,
        max_length= 50,
        description=  "País destino de la exportación (receptor)",
    )
    complemento:str = Field(
        min_length= 5,
        max_length= 300,
        description=  "Colocar las especificaciones de la direccion",
    )
    tipoPersona:TipoPersona = Field(
        description= "tipo de persona Juridica o persona natural",
    )
    @model_validator(mode= "after")
    def TipoDocumentoFexe(self):
        if self.tipoDocumento == 36:
            patternDoc = re.compile(r"^([0-9]{14}|[0-9]{9})$")
            if not patternDoc.match(str(self.numDocumento)):
                raise ValueError(f"El patron del TipoDocumento no cumple {patternDoc}")
        elif self.tipoDocumento == 13:
            patternDoc = re.compile(r"^[0-9]{8}-[0-9]{1}$")
            if not patternDoc.match(str(self.numDocumento)):
                raise ValueError(f"El patron del TipoDocumento no cumple {patternDoc}")
    
class OtroDocumentoFexe(OtroDocumento):
    placaTrans:Optional[str] = Field(
        min_length= 5,
        max_length= 70,
        description= "Número de identificación del transporte",  
    )
    #en el json schema a pesar de que el enum es hasta el 6, solo se puede elegir hasta el 4
    modoTransp:Optional[Transporte] = Field(
        ge = 1,
        le = 4,
    )
    numConductor:Optional[str] = Field(
        min_length= 5,
        max_length= 100,
        description= "N documento de identificación del Conductor",
    )
    nombreConductor:Optional[str] = Field(
        min_length= 5,
        max_length= 200,
        description= "Nombre y apellidos del Conductor",
    )
    #funcion que validara los cassos del modo de transporte
    @model_validator(mode= "after")
    def ModoTranspValidation(self):
        if self.codDocAsociado == 4:
            if self.modoTransp == None:
                raise ValueError("cuando el codDocAsociado es 4, modoTransp no puede ser None")
            elif self.numConductor == None:
                raise ValueError("cuando el codDocAsociado es 4, numConductor no puede ser None")
            elif self.nombreConductor == None:
                raise ValueError("cuando el codDocAsociado es 4, nombreConductor no puede ser None")
            elif self.placaTrans == None:
                raise ValueError("cuando el codDocAsociado es 4, placaTrans no puede ser None")
        elif self.codDocAsociado == 1 or self.codDocAsociado == 2:
            if self.descDocumento == None:
                raise ValueError("cuando el codDocAsociado es 1 o 2, descDocumento no puede ser None")
            elif self.detalleDocumento == None:
                raise ValueError("cuando el codDocAsociado es 1 o 2, detalleDocumento no puede ser None")
        else:
            if self.modoTransp != None:
                raise ValueError("cuando el codDocAsociado no es 4, modoTransp debe ser None")
            elif self.numConductor != None:
                raise ValueError("cuando el codDocAsociado no es 4, numConductor  debe ser None")
            elif self.nombreConductor != None:
                raise ValueError("cuando el codDocAsociado no es 4, nombreConductor debe ser None")
            elif self.placaTrans != None:
                raise ValueError("cuando el codDocAsociado no es 4, placaTrans debe ser None")        

class ItemCuerpoDocumentoFexe(ItemCuerpoDocumento):
    codigo:Optional[str] = Field(
        min_length= 1,
        max_length= 200,
    )
    precioUni:float = Field(
        #verficar que no existe una restriccion menor o igual a  0
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Precio Unitario"
    ) 
    montoDescu:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Descuento, Bonificación, Rebajas por ítem"
    ) 
    ventaGravada:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Ventas Gravadas",
    )
    tributos:Optional[list[str]] = Field(
        description= "codigo de tributo",
        min_items = 1,
        set = True, # nose permiten elementos duplicados en el arreglo se cambio unique_items por deprecado
    )
    noGravado: float = Field(
        gt= -100000000000, 
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Cargos/Abonos que no afectan la base imponible",
    )
    @model_validator(mode= "after")
    def NoGravadoFexe(self):
        if self.noGravado == 0:
            if self.precioUni == None:
                raise ValueError("cuando el noGravado es 0, precioUni no puede ser None")
            elif self.tributos != None:
                if "C3" not in self.tributos:
                    raise ValueError("cuando el noGravado es 0, incluye en tributos el valor 'C3' ")
        return self
class ItemPagoFexe(ItemPago):
    plazo:Optional[str] = Field(
        pattern= r"^0[1-3]$",
        description="Plazo",
    )
     #verificar si es int o float
    periodo:Optional[int]= Field(
        description="Período de plazo",
    )

class ResumenFexe(Resumen):
    pagos:Optional[list[ItemPagoFexe]] = Field(
        min_items = 1,
        description= "Pagos"
    )
    descuento:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Monto global de Descuento, Bonificación, Rebajas y otros a ventas",
    )
    seguro:Optional[float] = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Seguro"
    )
    flete:Optional[float] = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Flete",
    )
    codIncoterms:Optional[str] = Field(
        description= "INCOTERMS"
    )
    descIncoterms:Optional[str] = Field(
        min_length= 3,
        max_length= 150,
        description= "Descripción INCOTERMS",
    )
    observaciones:Optional[str] = Field(
        max_length= 500,
        description= "Observaciones"
    )


class FexePydantic(BaseModel):
    identificacion: IdentificacionFexe
    emisor:EmisorFexe
    receptor:ReceptorFexe
    otrosDocumentos:Optional[list[OtroDocumentoFexe]] = Field( 
        default= None,
        min_length= 1,
        max_length=  20,
        description= "Documentos Asociados",
    )
    ventaTercero:Optional[VentaTercero] = Field( 
        description= "Ventas por cuenta de terceros"
    )
    cuerpoDocumento:list[ItemCuerpoDocumentoFexe] = Field(
        min_items =1,
        max_items=2000
    )
  
    resumen:ResumenFexe
    apendice:Optional[list[ApendiceItems]] = Field(
        min_length= 1,
        max_length= 10,
    )
    @model_validator(mode="after") 
    def MontoTotalOperacionValidator(self):
        if self.resumen.montoTotalOperacion >= 10000:
            if self.receptor.correo == None:
                raise ValueError("cuando el monto es igual o superior a 10000, el correo no puede ser None")
            

#importamos la data para la verificacion
data_fexe = data_fe

try: 
    data_validada = FexePydantic(**data_fexe)
    print("Se valido correctamente")
    print(data_fe)
except ValueError as e:
    print(f'Error de validadcion: {e}')