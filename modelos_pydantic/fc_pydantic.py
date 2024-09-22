from fastapi import FastAPI
from base_pydantic import *
from fc_data import data_fc


app = FastAPI()
class IdentificacionFe(Identificacion):
    tipoDte:TipoDocumento = Field(
        default= "01",
        description="Tipo de Documento")
    
    #validacion de los campos de contingencia y su coherencia entre ellos
    @model_validator(mode="after")
    def ValidadorOperacion(self):
        #validamos si es una transmision normal los campos de contingencia y motivo deben ser nulos
        if self.tipoDte is not TipoDocumento.factura:
            raise ValueError("el tipoDte debe ser factura(01)")
        if self.tipoOperacion == 1: 
            if self.tipoModelo != 1:
                raise ValueError(f"cuando el tipoOperacion es {TipoTransmision.transmisionNormal.name} valor 1, el tipoModelo debe ser {ModeloFacturacion.modeloFacturacionPrevio.name} de valor 1 ") 
            if self.tipoContingencia != None:
                raise ValueError(f"el tipo de contingencia deben ser null o None")
            elif self.motivoContin != None  :
                raise ValueError("el motivo de contingencia debe ser null or None") 
        elif self.tipoOperacion == 2:
            if self.tipoModelo != 2:
                raise ValueError(f"cuando el tipoOperacion es {TipoTransmision.transmisionDiferido.name} valor 2, el tipoModelo debe ser {ModeloFacturacion.modeloFacturacionDiferido.name} de valor 2") 
        #validamos si el motivo de la contingencia es otro, si o si debemos rellenar el campo del motivo de la contingencia
        elif self.tipoOperacion == 2:
            if self.tipoContingencia == TipoContingencia.otro:
                if self.motivoContin == None:
                    raise ValueError("error, debe ingresar el motivo de la contigencia, no puede ser None")
        elif self.tipoDte == "0":
            raise ValueError("Para facturas electronicas tipoDte es '01' ")


class DocRelacionadoFe(DocRelacionado):
    numeroDocumento:str = Field(
        pattern= r"^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$"
    )
    
    @model_validator(mode="after")
    def tipoGeneracionValidator(self):
        if self.tipoGeneracion == TipoGeneracionDocumento.fisico:
            if len(self.numeroDocumento) > 20:
                raise ValueError("el numero de documento no puede tener mas de 20 caracteres")
        elif self.tipoGeneracion == TipoGeneracionDocumento.electronico:
            patronDoc = re.compile(r'^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$')
            if not patronDoc.match(str(self.numeroDocumento)):
                raise ValueError("si el tipoGeneracionDocumento es electronico(2), numeroDocumento debe tener el situiente patron: '^[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}$' ")
        elif self.tipoDocumento is not TipoDocumento.docContableLiquidacion or self.tipoDocumento is not TipoDocumento.notaRemision:
            raise ValueError(f"Tipo de Documento Tributario relacionad solo permite docContableLiquidacion(09), notaRemision(04)") 
        elif self.tipoDocumento is not TipoDocumento.notaRemision or self.tipoDocumento is not TipoDocumento.docContableLiquidacion:
            raise ValueError("los valores permitidos para el tipo de Documento es 04, 09")
        return self
             

class EmisorFe(Emisor):
    #verificar el numero de caracteres del nit si pueden ser menores
    nit:str = Field(
        pattern= r"^([0-9]{14}|[0-9]{9})$",
        max_length= 14,
        description= "NIT (emisor)",
    )
    codEstableMH:str = Field(
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
class ReceptorFe(Receptor):
    
    nrc:str = Field(
    pattern= r"^[0-9]{1,8}$",
    min_length= 2,
    max_length= 8,
    description= ("NRC (Receptor)"),
    )
    codActividad:str = Field(
            pattern= "^[0-9]{2,6}$",
            min_length= 5,
            max_length= 6,
            description="Código de Actividad Económica (Receptor)"
    )
    direccion: Direccion
    @model_validator(mode="after")
    def DocumentoReceptorValidator(self):
        if self.tipoDocumento == TipoDocumentoReceptor.nit:
            patternDoc = re.compile(r"^([0-9]{14}|[0-9]{9})$")
            if not patternDoc.match(str(self.numDocumento)):
                raise ValueError(f"El patron del TipoDocumento no cumple {patternDoc}")
            else:
                if self.nrc != None:
                    raise ValueError(f"El nrc debe ser null o none") 
        elif self.tipoDocumento == TipoDocumentoReceptor.dui:
            patternDoc = re.compile(r"^[0-9]{8}-[0-9]{1}$")
            if not patternDoc.match(str(self.numDocumento)):
                raise ValueError(f"El patron del TipoDocumento no cumple con la condicion {patternDoc}")
        
        return self
class OtroDocumentoFe(OtroDocumento):
    medico:Optional[Medico] = Field()
    @model_validator(mode="after")
    def OtroDocumentoValidator(self):
        if self.codDocAsociado == 3:
            if self.descDocumento != None or self.detalleDocumento != None:
                raise ValueError("el valor de desDocumento y detalleDocumento debe ser null o none")
            if self.medico != None:
                raise ValueError("los datos del medico no pueden ser None") 
        else:
            if self.descDocumento == None:
                raise ValueError(f"el valor de descDocumento no puede ser None")
            elif self.detalleDocumento == None:
                raise ValueError(f"el valor de detalleDocumento no puede ser None")
            elif self.medico != None:
                raise ValueError("el valor de la variable medico debe ser null o none") 

class ItemCuerpoDocumentoFe(ItemCuerpoDocumento):
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
    tributos:Optional[list[TributosAplicadosPorItemsResumidos]] = Field(
        description= "codigo de tributo",
        min_length= 1,
        set = True, # nose permiten elementos duplicados en el arreglo se cambio unique_items por deprecado
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
    ivaItem: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.00000001,
        description= "IVA por ítem",
        #verificar si le ponemos optional, o le ponemos default 0
    )
    @model_validator(mode= "after")
    def ventaGravadaValidator(self):
        if self.ventaGravada <= 0:
            if self.tributos != None:
                raise ValueError("Cuando la venta gravada = 0, los tributos deben ser None ")
            if self.ivaItem != 0:
                raise ValueError("Cuando la venta gravada = 0, el iva item tambien debe ser 0")
        if self.tipoItem == TipoItem.otrosTributosPorItem:
            if self.uniMedida != UnidadDeMedida.otra:
                raise ValueError("cuando el tipo de item es otro, uniMedida debe ser 99")
            elif  self.codTributo == None:
                raise ValueError("cuando el tipo de item es otro, codTributo no debe ser None")
            elif self.tributos != None:
                raise ValueError("Los tributos debe ser None")
        else:
            if self.codTributo == None:
                if self.tributos == None:
                    raise ValueError(" si el codTributo es None, los tributos no pueden ser None")

class ItemPagoFe(ItemPago):
    plazo:Optional[Plazo] = Field(
        pattern= r"^0[1-3]$",
        description="Plazo",
    )
     #verificar si es int o float
    periodo:Optional[int]= Field(
        description="Período de plazo",
    )


class ResumenFe(Resumen):
    pagos:Optional[list[ItemPagoFe]] = Field(
        min_length= 1,
        description= "Pagos"
    )
    
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
    totalIva: float = Field(
        ge= 0,
        lt= 100000000000,
        multiple_of= 0.01,
        description= "IVA 13%",
    )

class DataVerificado(BaseModel):
    identificacion: IdentificacionFe
    documentoRelacionado:Optional[list[DocRelacionadoFe]] = Field(
        default= None,
        min_length= 1,
        max_length= 10,
        description= "Documentos Relacionados",
    )
    emisor:EmisorFe
    receptor:ReceptorFe 
    otrosDocumentos:Optional[list[OtroDocumentoFe]] = Field( 
        default= None,
        min_length= 1,
        max_length=  10,
        description= "Documentos Asociados",
    )
    ventaTercero:Optional[VentaTercero] = Field( 
        description= "Ventas por cuenta de terceros"
    )
    cuerpoDocumento:list[ItemCuerpoDocumentoFe] = Field(
        min_length=1,
        max_length=2000
    )
    resumen:ResumenFe
    extension:Optional[Extension]
    apendice: list[ApendiceItems]
    
    @model_validator(mode="after")
    def MontoTotalOperacionValidator(self):
        if self.resumen.montoTotalOperacion > 1095:
            if self.receptor.tipoDocumento == None:
                raise ValueError("el TipoDocumento no puede ser None")
            if self.receptor.numDocumento == None:
                raise ValueError("el numDocumento no puede ser None")
            if self.receptor.nombre == None:
                raise ValueError("el nombre no puede ser None")
            
#importamos la data para la verificacion
data = data_fc

try: 
    data_validada = DataVerificado(**data)
    print("Se valido correctamente")
    print(data)
except ValueError as e:
    print(f'Error de validadcion: {e}')