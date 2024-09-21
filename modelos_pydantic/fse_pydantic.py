from fastapi import FastAPI
from base_pydantic import *
from fse_data import data_fse
from catalagos import *

app = FastAPI()
class IdentificacionFse(Identificacion):
    version:int = Field(default= 1)
    tipoDte:TipoDocumento = Field(default= 14)
    numeroControl:str = Field(
        pattern= "^DTE-14-[A-Z0-9]{8}-[0-9]{15}$"
    )
    motivoContin:Optional[str] = Field(
        min_length= 1,
    )
    @model_validator(mode="after")
    def ValidadorOperacion(self):
        #validamos si es una transmision normal los campos de contingencia y motivo deben ser nulos
        if self.tipoOperacion == TipoTransmision.transmisionNormal: 
            if self.tipoModelo != ModeloFacturacion.modeloFacturacionPrevio:
                raise ValueError("cuando el tipoOperacion es transmisionNormal(1), el tipoModelo debe ser modeloFacturacionPrevio(1)") 
            if self.tipoContingencia != None:
                raise ValueError(f"cuando el tipoOperacion es transmisionNormal(1), el tipo de contingencia deben ser null o None")
            elif self.motivoContin != None  :
                raise ValueError("cuando el tipoOperacion es transmisionNormal(1), el motivo de contingencia debe ser null or None, no debe haber motivo de contingencia") 
        elif self.tipoOperacion == TipoTransmision.transmisionDiferido:
            if self.tipoContingencia == None:
                raise ValueError("cuando el tipoOperacion es transmisionDiferido(2), el tipoContingencia no puede ser None") 
        elif self.tipoContingencia == TipoContingencia.otro:
            if self.motivoContin == None:
                raise ValueError("cuando le tipoContingencia es Otro(5), el motivoContin no puede ser None")

    

class EmisorFse(Emisor):
    nit:str = Field(
        pattern= r"^([0-9]{14}|[0-9]{9})$",
        description= "NIT (Emisor)"
    )
    nrc:str = Field(
        pattern= r"^[0-9]{1,8}$",
        description=("NRC (emisor)"),
    ) 
    nombre:str = Field(
        min_length= 1,
        max_length= 250,
    )
    codActividad:str = Field(
        pattern= r"^[0-9]{2,6}$",
        min_length= 2,
        description="Código de Actividad Económica (Emisor)",
    )
    descActividad:str = Field(
        min_length= 1, 
        max_length= 150,
        description="Actividad Económica (Emisor)"
    )
    direccion:Direccion 
    codEstable:str = Field(
        min_length= 1,
        max_length= 10,
    )

class SujetoExcluido(Receptor):
    numDocumento:str = Field(
        min_length= 1,
        max_length= 20,
        # pattern= "^([0-9]{14}|[0-9]{9})$",
        description=  "Número de documento de Identificación (Receptor)",
    )
    codActividad:str = Field(
        pattern= r"^[0-9]{2,6}$",
        description="Código de Actividad Económica (Emisor)"
    )
    descActividad:str = Field(
        min_length= 1, 
        max_length= 150,
        description="Actividad Económica (Emisor)"
    )
    direccion:Direccion  
    correo:EmailStr = Field(
        max_length= 100,
        description= "Correo electrónico (Receptor)"
    )
    nrc:Optional[str] = Field(
        default=None,
        pattern= r"^[0-9]{1,8}$",
    )
    @model_validator(mode="after")
    def tipo_documento_validation(self):
        if self.tipoDocumento == TipoDocumentoReceptor.nit:
            nuevoPatron = re.compile(r"^([0-9]{14}|[0-9]{9})$")
            if not nuevoPatron.match(str(self.numDocumento)):
                raise ValueError("el numDocumento no cumple con el patron '[0-9]{14}|[0-9]{9}' ")
            #hay una validacion mas con el nrc, pero ya esta definida arriba. 
        elif self.tipoDocumento == TipoDocumentoReceptor.dui:
            nuevoPatron = re.compile(r"^([0-9]{9})$")
            if not nuevoPatron.match(str(self.numDocumento)):
                raise ValueError("el numDocumento debe cumplir con el patron '[0-9]{9}' ")
            
class ItemCuerpoDocumentoFse(ItemCuerpoDocumento):
    tipoItem:TipoItem = Field(
        ge= 1,
        le = 3,
        description=  "Tipo de ítem",
    )
    precioUni:float = Field(
        ge = 0,
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Precio Unitario",
    )        
    montoDescu:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Descuento, Bonificación, Rebajas por ítem",
    )
    compra:float = Field(
        ge = 0,
        lt = 100000000000,
        multiple_of= 0.00000001,
        description= "Ventas",
    )

class ItemPagoFse(ItemPago):
    plazo:Optional[Plazo] = Field(
        pattern= r"^0[1-3]$",
        description="Plazo",
    )
     #verificar si es int o float
    periodo:Optional[int]= Field(
        description="Período de plazo",
    )  
class ResumenFse(BaseModel):
    totalCompra: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total de Operaciones ",
    )
    descu: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Monto global de Descuento, Bonificación, Rebajas y otros al total de operaciones.",
    )
    totalDescu: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total del monto de Descuento, Bonificación, Rebajas",
    )
    subtotal: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Sub-Total",
    )
    ivaRetel: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "IVA Retenido",
    )
    reteRenta: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Retención Renta",
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
    condicionOperacion: CondicionOperacion = Field(
        description="Condición de la Operación",
    )
    pagos:Optional[list[ItemPagoFse]] = Field(
        min_length= 1,
        description= "Pagos"
    )
    observaciones:Optional[str] = Field(
        max_length= 3000,
        description= "Observaciones"
    )
    @model_validator(mode= "after")
    #verificar la validacion, si puede haber mas pagos, para 
    def condicion_operacion_validator(self):
        if self.condicionOperacion == CondicionOperacion.credito:
            if self.pagos == None:
                raise ValueError("si el pago es a crédito, ingresar el plazo y el periodo")


class fsePydantic(BaseModel):
    identificacion:IdentificacionFse
    emisor:EmisorFse 
    sujetoExcluido:SujetoExcluido

    cuerpoDocumento:list[ItemCuerpoDocumentoFse] = Field(
        min_length= 1,
        max_length= 2000,
    )
    resumen:ResumenFse
    apendice:Optional[list[ApendiceItems]] = Field(
        description= "Apéndice",
        min_length= 1,
        max_length= 10,
    )

data = data_fse

try: 
    data_validada = fsePydantic(**data)
    print("Se valido correctamente")
    print(data_fse)
except ValueError as e:
    print(f'Error de validadcion: {e}')