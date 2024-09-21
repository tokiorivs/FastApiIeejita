from fastapi import FastAPI
from base_pydantic import *
from nc_data import data_nc
from catalagos import *

app = FastAPI()

class IdentificacionNc(Identificacion):
    version:int = Field( 
        default= 3,
        gt=2,
        lt=4,
        description="Version",
    )
    tipoDte:TipoDocumento = Field( 
        default= "05",
        description="Tipo de Documento",
    )
    numeroControl:str = Field(
        description= "Numero de control",
        max_length= 31,
        min_length= 31,
        pattern= r"^DTE-05-[A-Z0-9]{8}-[0-9]{15}$",
    )
    motivoContin:Optional[str] = Field(
        description="Motivo de  Contingencia",
        max_length= 150,
        min_length= 1,
    )
    @model_validator(mode= "after")
    def tipo_operacion_validator(self):
        if self.tipoOperacion == TipoTransmision.transmisionNormal: 
                if self.tipoModelo != ModeloFacturacion.modeloFacturacionPrevio:
                    raise ValueError(f"cuando el tipoOperacion es {TipoTransmision.transmisionNormal.name}(1), el tipoModelo debe ser {ModeloFacturacion.modeloFacturacionPrevio.name}(1)") 
                elif self.tipoContingencia != None:
                    raise ValueError(f"el tipo de contingencia deben ser null o None")
                elif self.motivoContin != None  :
                    raise ValueError("el motivo de contingencia debe ser null or None") 
        elif self.tipoOperacion == TipoTransmision.transmisionDiferido:
            if self.tipoContingencia != None:
                raise ValueError(f"cuando el tipoOperacion es {TipoTransmision.transmisionDiferido.name}(2), el tipoContingencia no puede ser None") 
        #validamos si el motivo de la contingencia es otro, si o si debemos rellenar el campo del motivo de la contingencia
        elif self.tipoContingencia == TipoContingencia.otro:
                if self.motivoContin == None:
                    raise ValueError("error, debe ingresar el motivo de la contigencia, no puede ser None")

class documentoRelacionadoNc(DocRelacionado):
        tipoDocumento:TipoDocumento = Field(
            description="Tipo de Documento Tributario Relacionado"
        )
        

        @model_validator(mode="after")
        def tipo_documento_validator(self):
            if self.tipoDocumento != "03" and self.tipoDocumento != "07":
                raise ValueError("el tipoDocumento debe ser '03', '07'")
            elif self.tipoGeneracion == TipoGeneracionDocumento.electronico:
                newPattern = re.compile(r"^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$")
                if not newPattern.match(str(self.numeroDocumento)):
                    raise ValueError("si el tipoGeneracionDocumento es electronico(2), numeroDocumento debe tener el situiente patron: '^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$' ")
            

class EmisorNc(Emisor):
    nit:str = Field(
        pattern= r"^([0-9]{14}|[0-9]{9})$",
        max_length= 14,
        description= "NIT (emisor)",
    )
    nrc:str = Field(
        pattern= r"^[0-9]{1,8}$",
        description=("NRC (emisor)"),
    )
    nombre:str =Field(
        min_length= 3,
        max_length= 200,
        description= "Nombre, denominación o razón social del contribuyente (Emisor)",
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
    nombreComercial:str = Field(
        min_length= 1, 
        max_length= 150,
        description= "Nombre Comercial (Emisor)", 
    )
    
class ReceptorNc(BaseModel):
    nit:str = Field(
        pattern= r"^([0-9]{14}|[0-9]{9})$",
        max_length= 14,
        description= "NIT (receptor)",
    )
    nrc:str = Field(
        pattern= r"^[0-9]{1,8}$",
        description=("NRC (receptor)"),
    )
    nombre:str =Field(
        min_length= 1,
        max_length= 250,
        description= "Nombre, denominación o razón social del contribuyente (Receptor)",
    )
    codActividad:str = Field(
        pattern= r"^[0-9]{2,6}$",
        description="Código de Actividad Económica (Emisor)"
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
    direccion:Direccion
    telefono:str = Field(
        min_length= 8,
        max_length= 30,
        description= "Teléfono (Receptor)",
    )
    correo:EmailStr = Field(
        max_length= 100,
        description= "Correo electrónico (Receptor)"
    )
class ItemCuerpoDocumentoNc(ItemCuerpoDocumento):
    tipoItem:TipoItem = Field(
        description= "Tipo de item"
    )
    numeroDocumento:str = Field(
        min_length= 1,
        max_length= 36,
        description= "Número de documento relacionado"
    )
    codTributo: Optional[TributosAplicadosPorItemsReflejados] = Field(
        min_length= 2,
        max_length= 2,
        description= "Tributo sujeto a cálculo de IVA",
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
    #verificar la lista de tributos, on especifica que tributos entran
    tributos:Optional[list[TributosAplicadosPorItemsResumidos]] = Field(
        description= "codigo de tributo",
        min_length= 1,
        set = True, # nose permiten elementos duplicados en el arreglo se cambio unique_items por deprecado
    )
    @model_validator(mode="after")
    def item_cuerpo_documento_nc_validator(self):
        if self.ventaGravada <= 0:
            if self.tributos is not None:
                raise ValueError("cuando la ventaGravada es 0, los tributos deben ser None")
        elif self.tipoItem == TipoItem.otrosTributosPorItem:
            if self.uniMedida is not UnidadDeMedida.otra:
                raise ValueError("cuando tipoItem es otrosTributosPorItem(4), uniMedida debe ser 'otra'(99)")
            elif sum(tributo == "20" for tributo in self.tributos ) == 0:
                raise ValueError("cuando el tipoItem es otrosTributosPorItem(4), en los tributos debe haber por lo menos un 'iva13'(20)")
        elif self.codTributo == None:
            #verificar que elementos entran en los tributos, para hacer la correcta validacion
            if self.tributos != None:
                raise ValueError("cuando el codTributo es None,  los tributos no pueden ser None")
                
class ResumenNc(Resumen):
    totalNoSuj:float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Total de Operaciones no sujetas"
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
    descuGravada: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Monto global de Descuento, Bonificación, Rebajas y otros a ventas gravadas",
    )
    tributos:list[ItemTributo] = Field(
        # unique_items= True,
        description= "Resumen de tributos"    
    )
    subTotal: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "Sub-Total",
    )
    ivaPercil: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "IVA Percibido",
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
    
    @model_validator(mode= "after")
    def resume_validator(self):
        if self.totalGravada == 0:
            if self.ivaPercil > 0:
                raise ValueError("se totalGravada es igual a 0, ivaPercil no puede ser mayor a 0")
            if self.ivaRetel > 0:
                raise ValueError("cuando totalGravada es 0, el ivaRetel no puede ser mayor a 0")
 
class ExtensionNc(BaseModel):
    nombEntrega:str = Field(
        min_length= 1,
        max_length= 100,
        description= "Nombre del responsable que Genera el DTE",
    )   
    docuEntrega:str = Field(
        min_length= 1,
        max_length= 25,
        description= "Documento de identificación de quien genera el DTE",
    )
    nombRecibe: str = Field(
        min_length= 1,
        max_length= 100,
        description= "Nombre del responsable de la operación por parte del receptor",
    )
    docuRecibe: str = Field(
        min_length= 1,
        max_length= 100,
        description= "Documento de identificación del responsable de la operación por parte del receptor",
    )
    observaciones: str = Field(
        max_length= 3000,
        description= "Observaciones",
    )
            
class ApendiceItemsNc(BaseModel):
    campo:str = Field(
        min_length= 2,
        max_length= 25,
        description= "Nombre del campo",
    )
    etiqueta:str = Field(
        min_length= 2,
        max_length= 50,
        description= "Descripcion"
    )
    valor:str = Field(
        min_length= 1,
        max_length= 150,
        description= "Valor/Dato" 
    )
       
class NcPydantic(BaseModel):
    identificacion:IdentificacionNc
    documentoRelacionado:list[documentoRelacionadoNc] = Field(
        min_length= 1,
        max_length= 50,
        description=  "Documentos Relacionados",
    )
    emisor:EmisorNc 
    receptor:ReceptorNc
    ventaTercero:VentaTercero

    cuerpoDocumento:list[ItemCuerpoDocumentoNc] = Field(
        min_length= 1,
        max_length= 2000,
    )
    resumen:ResumenNc
    extension:ExtensionNc
    apendice:Optional[list[ApendiceItemsNc]] = Field(
        description= "Apéndice",
        min_length= 1,
        max_length= 10,
    )

data = data_nc

try: 
    data_validada = NcPydantic(**data)
    print("Se valido correctamente")
    print(data_nc)
except ValueError as e:
    print(f'Error de validadcion: {e}')