from fastapi import FastAPI
from base_pydantic import *
from nd_data import data_nd
from catalagos import *

app = FastAPI()

class IdentificacionNd(Identificacion):
    version:int = Field( 
        default= 3,
        gt=2,
        lt=4,
        description="Version",
    )
    tipoDte:TipoDocumento = Field( 
        default= "06",
        description="Tipo de Documento",
    )
    numeroControl:str = Field(
        description= "Numero de control",
        max_length= 31,
        min_length= 31,
        pattern= r"^DTE-06-[A-Z0-9]{8}-[0-9]{15}$",
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


class DocumentoRelacionadoNd(DocRelacionado):
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
        
class EmisorNd(Emisor):
    nit:str = Field(
        pattern= r"^([0-9]{14}|[0-9]{9})$",
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
class ReceptorNd(BaseModel):
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

class NdPydantic(BaseModel):
    identificacion:IdentificacionNd
    documentoRelacionado:list[DocumentoRelacionadoNd] = Field(
        min_length= 1,
        max_length= 50,
        description=  "Documentos Relacionados",
    )
    emisor:EmisorNd 
    receptor:ReceptorNd
    # ventaTercero:VentaTercero

    # cuerpoDocumento:list[ItemCuerpoDocumentoNd] = Field(
    #     min_length= 1,
    #     max_length= 2000,
    # )
    # resumen:ResumenNd
    # extension:ExtensionNd
    # apendice:Optional[list[ApendiceItemsNd]] = Field(
    #     description= "Apéndice",
    #     min_length= 1,
    #     max_length= 10,
    # )

data = data_nd

try: 
    data_validada = NdPydantic(**data)
    print("Se valido correctamente")
    print(data_nd)
except ValueError as e:
    print(f'Error de validadcion: {e}')