from fastapi import FastAPI
import re
from base_pydantic import *
from ccfe_data import data_ccfe
from catalagos import *

app = FastAPI()
class IdentificacionCcfe(Identificacion):
    version:int = Field(default= 3)
    tipoDte:TipoDocumento = Field(default= 3)
    numeroControl:str = Field(
        pattern= r"^DTE-03-[A-Z0-9]{8}-[0-9]{15}$",
    )
    motivoContin:Optional[str] = Field(
        min_length= 1,
    )
    @model_validator(mode= "after")
    def ValidadorOperacion(self):
        #validamos si es una transmision normal los campos de contingencia y motivo deben ser nulos
        if self.tipoOperacion == TipoTransmision.transmisionNormal: 
            if self.tipoModelo != ModeloFacturacion.modeloFacturacionPrevio:
                raise ValueError("cuando el tipoOperacion es 1, el tipoModelo debe ser 1") 
            if self.tipoContingencia != None:
                raise ValueError(f"el tipo de contingencia deben ser null o None")
            elif self.motivoContin != None  :
                raise ValueError("el motivo de contingencia debe ser null or None, no debe haber motivo de contingencia") 
        elif self.tipoOperacion == TipoTransmision.transmisionDiferido:
            if self.tipoModelo != ModeloFacturacion.modeloFacturacionDiferido:
                raise ValueError("cuando el tipoOperacion es 2, el tipoModelo debe ser 2") 
            if self.tipoContingencia == None:
                raise ValueError("cuando el tipoOperacion es 2, el tipoContingencia no puede ser None") 
        elif self.tipoContingencia == TipoContingencia.otro:
            if self.motivoContin == None:
                raise ValueError("cuando le tipoContingencia es 5, el motivoContin no puede ser None")


class DocRelacionadoCcfe(DocRelacionado):
    @model_validator(mode="after")
    def tipoGeneracion(self):
        if self.tipoGeneracion == 2:
            patronDoc = re.compile(r'^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$')
            if not patronDoc.match(str(self.numeroDocumento)):
                raise ValueError("el numero del documento no cumple con el patron")
        return self
class EmisorCcfe(Emisor):
    nit:str = Field(
        pattern= r"^([0-9]{14}|[0-9]{9})$",
        description= "NIT (Emisor)"
    )
    #por alguna razon no tiene validacion de nrc de minimo y maximo verificar
    nrc:str = Field(
        pattern= r"^[0-9]{1,8}$",
        min_length= 2,
        max_length= 8,
        description=("NRC (emisor)"),
    ) 
    nombre:str = Field(
        min_length= 3,
        max_length= 200,
        description= "Nombre, denominación o razón social del contribuyente (Emisor)",

    )
    codActividad:str = Field(
       pattern= r"^[0-9]{2,6}$",
       min_length= 5,
       max_length= 6,
       description="Código de Actividad Económica (Emisor)"
    )
    descActividad:str = Field(
        min_length= 1, 
        max_length= 150,
        description="Actividad Económica (Emisor)"
    )
    nombreComercial:str = Field(
        max_length= 150,
        min_length= 1, 
        description= "Nombre Comercial (Emisor)", 

    )
    codEstableMH:str = Field(
        min_length= 4,
        max_length= 4,
        description= "Código del establecimiento asignado por el MH", 
    )
    codEstable:str = Field(
        min_length= 1,
        max_length= 10,
        description= "Código del establecimiento asignado por el contribuyente", 
    )
    codPuntoVentaMH:str
    codPuntoVenta:str

class ReceptorCcfe(BaseModel):
    nit:str = Field(
        pattern= r"^([0-9]{14}|[0-9]{9})$",
        description= "NIT (Receptor)"
    )
    nrc:str = Field(
        pattern= "^[0-9]{1,8}$",
        min_length= 2,
        max_length= 8,
        description=("NRC (Receptor)"),
    )
    nombre:str =Field(
        min_length= 1,
        max_length= 250,
        description= "Nombre, denominación o razón social del contribuyente (Receptor)",
    )
    codActividad:str = Field(
       pattern= "^[0-9]{2,6}$",
       min_length= 5,
       max_length= 6,
       description="Código de Actividad Económica (Receptor)"
    )
    descActividad:str = Field(
        min_length= 1, 
        max_length= 150,
        description="Actividad Económica (Receptor)"
    )
    nombreComercial:str = Field(
        min_length= 1,
        max_length= 150,
        description= "Nombre Comercial (Receptor)",
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
class OtroDocumentoCcfe(OtroDocumento):
    medico:Medico
    @model_validator(mode="after")
    def codDocAsociado_Validator(self):
        if self.codDocAsociado == CodDocAsociado.transporte:
            if self.medico == None:
                raise ValueError(f"cuando el codDocAsociado es {CodDocAsociado.transporte.name} valor = 4,el medico no puede ser None ")
            elif self.descDocumento != None:
                raise ValueError(f"cuando el codDocAsociado es {CodDocAsociado.transporte.name} valor = 4,el descDocumento debe ser None ")
            elif self.detalleDocumento != None:
                raise ValueError(f"cuando el codDocAsociado es {CodDocAsociado.transporte.name} valor = 4,el detalleDocumento debe ser None ")
        else:
            if self.descDocumento == None:
               raise ValueError("el descDocumento no puede ser None")   
            elif self.detalleDocumento == None:
                raise ValueError("el detalleDocumento no puede ser None")
            elif self.medico != None:
                raise ValueError("el valor del médico de ser None")
class VentaTerceroCcfe(BaseModel):
    nit:str = Field(
        pattern= "^([0-9]{14}|[0-9]{9})$",
        description= "NIT por cuenta de terceros",
    )  
    nombre:str = Field(
        min_length= 3,
        max_length= 200,
        description=  "Nombre, denominación o razón social del Tercero",
    )
    
class ItemCuerpoDocumentoCcfe(ItemCuerpoDocumento):
    tipoItem:TipoItem = Field(
        ge=1,
        le=4,
        description=  "N° de ítem",
    )
    numeroDocumento:str = Field(
        min_length= 1,
        max_length= 36,
        description= "Número de documento relacionado",
    )
    codTributo:Optional[TributosAplicadosPorItemsReflejados] = Field(
        min_length= 2,
        max_length= 2,
        description=  "Tributo sujeto a cálculo de IVA.",
    )
    precioUni:float = Field(
        #verficar que no existe una restriccion menor o igual a  0
        ge=0,
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
    ventaNoSuj:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Ventas no Sujetas", 
    )
    ventaExenta:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Ventas Exentas",
    )
    ventaGravada:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Ventas Gravadas",
    )
    #verificar cuales son los tributos que deben aplicar
    #validar que los tributos no se dupliquen en la lista
    tributos:Optional[list[TributosAplicadosPorItemsResumidos]] = Field(
        description= "codigo de tributo",
        min_length= 1,
    )
    psv: float = Field(
        ge= 0,  
        lt= 100000000000,  
        multiple_of= 0.00000001,
        description= "Precio sugerido de venta",
    )
    noGravado: float = Field(
        gt= -100000000000, 
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "Cargos/Abonos que no afectan la base imponible",
    )
    @model_validator(mode="after")
    def ventaGravada_validator(self):
        if self.ventaGravada <= 0:
            if self.tributos is not None:
                raise ValueError("cuando la ventaGravada es menor, igual a 0, el tributos deben ser None")
        if self.tipoItem == TipoItem.otrosTributosPorItem:
            if self.uniMedida != UnidadDeMedida.otra:
                raise ValueError("cuando el tipoItem es otro(4), uniMedida debe ser otro, valor = 99")
            elif  self.codTributo == None:
                raise ValueError("cuando el tipoItem es otro(4), codTributo no debe ser None")
            elif not all(tributo == "20" for tributo in self.tributos):
                raise ValueError("cuando el tipoItem es otros, los tributos debe ser '20' ")
        else:
            if self.codTributo == None:
                if self.tributos != None:
                    raise ValueError("cuando el codTributo es None, los tributos no puden ser None")
            return self
class ItemPagoCcfe(ItemPago):
    plazo:str = Field(
        pattern= r"^0[1-3]$",
        description="Plazo",
    )
     #verificar si es int o float
    periodo:int= Field(
        description="Período de plazo",
    )
class ResumenCcfe(Resumen):
    totalNoSuj:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total de Operaciones no sujetas",
    )
    totalExenta: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total de Operaciones exentas",
    )
    subTotalVentas: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Suma de operaciones sin impuestos",
    )
    descuNoSuj: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Monto global de Descuento, Bonificación, Rebajas y otros a ventas no sujetas",
    )
    descuExenta: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Monto global de Descuento, Bonificación, Rebajas y otros a ventas exentas",
    )
    tributos:list[ItemTributo] = Field(
        # unique_items= True,
        description= "Resumen de tributos"    
    )
    ivaPercil:float = Field(
        ge=0,
        lt=100000000000,
        multiple_of= 0.01,
        description= "IVA Percibido",
    )
    subTotal: float = Field(
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
    saldoFavor: float = Field(
        le= 0,  
        gt= -100000000000,
        multiple_of= 0.01,
        description= "Saldo a Favor",
    )
    pagos:Optional[list[ItemPagoCcfe]] = Field(
        min_length= 1,
        description= "Pagos"
    )
    @model_validator(mode="after")
    def condicion_operacion(self):
        if self.condicionOperacion == CondicionOperacion.credito:
            if self.pagos == None:
                raise ValueError("cuando la condicionOperacion es a credito(2), pagos no puede ser None")
        elif self.totalGravada <= 0:
            if self.ivaPercil  > 0:  
                raise ValueError("cuando  totalGravada es menor igual a 0, ivaPercil deber ser 0")
            elif self.ivaRetel > 0:
                raise ValueError("cuando  totalGravada es menor igual a 0, ivaRetel deber ser 0")
        elif self.totalPagar <= 0:
            if self.condicionOperacion != 1:
                raise ValueError("cuando totalPagar es menor igual a 0, condicionOperacion debe ser igual al contado(1) ")

    
class ExtensionCcfe(Extension):
    nombEntrega:str = Field(
        min_length=1,
    )
    docuEntrega:str = Field(
        min_length=1,
    )
    nombRecibe:str = Field(
        min_length=1,
    )
    docuRecibe:str = Field(
        min_length=1,
    )
    placaVehiculo:str = Field(
        min_length=2,
    )
class ApendiceItemsCcfe(ApendiceItems):
    campo:str = Field(
        min_length= 2,
        max_length= 25,
        description= "Nombre del campo",
    )
    etiqueta:str = Field(
        min_length= 3,
        max_length= 50,
        description= "Descripcion"
    )
    valor:str = Field(
        min_length= 1,
       max_length= 150,
       description= "Valor/Dato" 
    )
    
        
class CcfePydantic(BaseModel):
    identificacion:IdentificacionCcfe
    documentoRelacionado: list[DocRelacionadoCcfe] = Field(
        min_length= 1,
        max_length= 50,
        description= "Documentos Relacionados",
    )
    emisor:EmisorCcfe 
    receptor:ReceptorCcfe
    otrosDocumentos:list[OtroDocumentoCcfe] = Field(
        min_length= 1,
        max_length= 10,
        description= "Documentos Asociados",
    )
    ventaTercero:VentaTerceroCcfe = Field(
        description= "Ventas por cuenta de terceros",
    )
    cuerpoDocumento:list[ItemCuerpoDocumentoCcfe] = Field(
        min_length= 1,
        max_length= 2000,
    )
    resumen:ResumenCcfe
    extension:ExtensionCcfe
    apendice:Optional[list[ApendiceItemsCcfe]] = Field(
        description= "Apéndice",
        min_length= 1,
        max_length= 10,
    )

data = data_ccfe

try: 
    data_validada = CcfePydantic(**data)
    print("Se valido correctamente")
    print(data_ccfe)
except ValueError as e:
    print(f'Error de validadcion: {e}')