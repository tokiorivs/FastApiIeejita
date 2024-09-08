from enum import Enum


#clase que no esta en el catalogo

class Usd(str, Enum):
    usd = "USD"

class TipoDoc(str, Enum):
    array = "array"
    
#CAT-001
class AmbienteDestino(str, Enum):
    pruebas ="00"
    produccion ="01"

#CAT-002
class TipoDocumento(str, Enum):
    factura="01"    
    comprobanteCreditoFiscal = "03"
    notaRemision ="04"
    notaCredito = "05"
    notaDebito = "06"
    comprobanteRetencion = "07"
    comprobanteLiquidacion = "08"
    docContableLiquidacion = "09"
    facturasExportacion = "11"
    facturaSujetoExcluido = "14"
    comprobanteDonacion = "15"
    
#CAT-003
class ModeloFacturacion(int, Enum):
    modeloFacturacionPrevio = 1
    modeloFacturacionDiferido = 2
    
#CAT-004
class TipoTransmision(int, Enum):
    transmisionNormal = 1
    transmisionDiferido = 2

#CAT-005
class TipoContingencia(int, Enum):
    noSistemaMH = 1
    noSistemaEmisor = 2
    fallaInternetEmisor = 3
    fallaEnergiaElectricaEmisor = 4 
    otro = 5

#CAT-006
class RetencionIvaMh(str, Enum):
    retencion1 = '22'
    retencion13 = 'C4'
    otrasRetencionesEspeciales = 'C9'

#CAT-007
class TipoGeneracionDocumento(int, Enum):
    fisico = 1
    electronico = 2

#CAT-009
class TipoEstablecimiento(str, Enum):
    sucursal= "01"
    casaMatriz= "02"
    bodega= "04"
    patio= "07"

#CAT-010
class TipoServicioMedico(int, Enum):
    cirugia = 1
    operacion = 2
    tratamientoMedico = 3
    cirugiaInstitutoSBM = 4
    operacionInstitutoSBM = 5
    tratamientoMedicoInstitutoSBM = 6

#CAT-011
class TipoItem(int, Enum):
    bienes = 1
    servicios = 2
    ambos = 3  # Bienes y Servicios
    otrosTributosPorItem = 4

#CAT-012
class Departamento(str, Enum):
    otro = "00"  # Para extranjeros
    ahuachapan = "01"
    santaAna = "02"
    sonsonate = "03"
    chalatenango = "04"
    laLibertad = "05"
    sanSalvador = "06"
    cuscatlan = "07"
    laPaz = "08"
    cabañas = "09"
    sanVicente = "10"
    usulutan = "11"
    sanMiguel = "12"
    morazan = "13"
    laUnion = "14"


#CAT-013 
class Municipio(str, Enum):
    otro = "00"
    ahuachapanNorte = "13"
    ahuachapanCentro = "14"
    ahuachapanSur = "15"
    santaAnaNorte = "14"
    santaAnaCentro = "15"
    santaAnaEste = "16"
    santaAnaOeste = "17"
    sonsonateNorte = "17"
    sonsonateCentro = "18"
    sonsonateEste = "19"
    sonsonateOeste = "20"
    chalatenangoNorte = "34"
    chalatenangoCentro = "35"
    chalatenangoSur = "36"
    laLibertadNorte = "23"
    laLibertadCentro = "24"
    laLibertadOeste = "25"
    laLibertadEste = "26"
    laLibertadCosta = "27"
    laLibertadSur = "28"
    sanSalvadorNorte = "20"
    sanSalvadorOeste = "21"
    sanSalvadorEste = "22"
    sanSalvadorCentro = "23"
    sanSalvadorSur = "24"
    cuscatlanNorte = "17"
    cuscatlanSur = "18"
    laPazOeste = "23"
    laPazCentro = "24"
    laPazEste = "25"
    cabanasOeste = "10"
    cabanasEste = "11"
    sanVicenteNorte = "14"
    sanVicenteSur = "15"
    usulutanNorte = "24"
    usulutanEste = "25"
    usulutanOeste = "26"
    sanMiguelNorte = "21"
    sanMiguelCentro = "22"
    sanMiguelOeste = "23"
    morazanNorte = "27"
    morazanSur = "28"
    laUnionNorte = "19"
    laUnionSur = "20"

#CAT-014
class UnidadDeMedida(int, Enum):
    metro = 1
    yarda = 2
    milimetro = 6
    kilometroCuadrado = 9
    hectarea = 10
    metroCuadrado = 13
    varaCuadrada = 15
    metroCubico = 18
    barril = 20
    galon = 22
    litro = 23
    botella = 24
    mililitro = 26
    tonelada = 30
    quintal = 32
    arroba = 33
    kilogramo = 34
    libra = 36
    onzaTroy = 37
    onza = 38
    gramo = 39
    miligramo = 40
    megawatt = 42
    kilowatt = 43
    watt = 44
    megavoltioAmperio = 45
    kilovoltioAmperio = 46
    voltioAmperio = 47
    gigawattHora = 49
    megawattHora = 50
    kilowattHora = 51
    wattHora = 52
    kilovoltio = 53
    voltio = 54
    millar = 55
    medioMillar = 56
    ciento = 57
    docena = 58
    unidad = 59
    otra = 99

 
#CAT-022 tipo de documento de identificacion del recepto
class TipoDocumentoReceptor(str, Enum):
    nit = "36"
    dui = "13"
    otro = "37"
    pasaporte = "03"
    carnetRecidente = "02"

#CAT-015 tributos 2-tributos aplicados por items reflejados en el del 
class TributosAplicadosPorItemsReflejados(str, Enum):
    impuestoEspecialCombustible = "A8"
    impuestoIndustriaCemento = "57"
    impuestoPrimeraMatricula = "90"
    otrosImpuestosCasosEspeciales = "D4"
    otrasTasasCasosEspeciales = "D5"
    impuestoAdValoremArmasFuego = "A6"

class TributosAplicadosPorItemsResumidos(str, Enum):
    iva13 = "20"  # Impuesto al Valor Agregado 13%/
    ivaExportaciones = "C3"  # Impuesto al Valor Agregado (exportaciones) 0%
    turismoAlojamiento = "59"  # Turismo: por alojamiento (5%)
    turismoSalidaAerea = "71"  # Turismo: salida del país por vía aérea $7.00
    fovial = "D1"  # FOVIAL ($0.20 Ctvs. por galón)
    cotrans = "D2"  # COTRANS ($0.10 Ctvs. por galón)/
    otrasTasasCasosEspeciales = "D5"  # Otras tasas casos especiales
    otrosImpuestosCasosEspeciales = "D4"  # Otros impuestos casos especiales
    c5 = "C5"  # Impuesto ad-valorem por diferencial de precios de bebidas alcohólicas (8%)
    c6 = "C6"  # Impuesto ad-valorem por diferencial de precios al tabaco cigarrillos (39%)
    c7 = "C7"  # Impuesto ad-valorem por diferencial de precios al tabaco cigarros (100%)
    fabricanteBebidasGaseosas = "19"  # Fabricante de Bebidas Gaseosas, Isotónicas, Deportivas, Fortificantes, Energizantes o Estimulantes
    importadorBebidasGaseosas = "28"  # Importador de Bebidas Gaseosas, Isotónicas, Deportivas, Fortificantes, Energizantes o Estimulantes
    detallistasBebidasAlcoholicas = "31"  # Detallistas o Expendedores de Bebidas Alcohólicas
    fabricanteCerveza = "32"  # Fabricante de Cerveza
    importadorCerveza = "33"  # Importador de Cerveza
    fabricanteProductosTabaco = "34"  # Fabricante de Productos de Tabaco
    importadorProductosTabaco = "35"  # Importador de Productos de Tabaco
    fabricanteArmasFuego = "36"  # Fabricante de Armas de Fuego, Municiones y Artículos Similares
    importadorArmasFuego = "37"  # Importador de Armas de Fuego, Munición y Artículos Similares
    fabricanteExplosivos = "38"  # Fabricante de Explosivos
    importadorExplosivos = "39"  # Importador de Explosivos
    fabricanteProductosPirotecnicos = "42"  # Fabricante de Productos Pirotécnicos
    importadorProductosPirotecnicos = "43"  # Importador de Productos Pirotécnicos
    productorTabaco = "44"  # Productor de Tabaco
    distribuidorBebidasGaseosas = "50"  # Distribuidor de Bebidas Gaseosas, Isotónicas, Deportivas, Fortificantes, Energizante o Estimulante
    bebidasAlcoholicas = "51"  # Bebidas Alcohólicas
    cerveza = "52"  # Cerveza
    productosTabaco = "53"  # Productos del Tabaco
    bebidasCarbonatadas = "54"  # Bebidas Carbonatadas o Gaseosas Simples o Endulzadas
    otrosEspecificos = "55"  # Otros Específicos
    alcohol = "58"  # Alcohol
    importadorJugos = "77"  # Importador de Jugos, Néctares, Bebidas con Jugo y Refrescos
    distribuidorJugos = "78"  # Distribuidor de Jugos, Néctares, Bebidas con Jugo y Refrescos
    sobreLlamadasTelefonicas = "79"  # Sobre Llamadas Telefónicas Provenientes del Ext.
    detallistaJugos = "85"  # Detallista de Jugos, Néctares, Bebidas con Jugo y Refrescos
    fabricantePreparacionesBebidas = "86"  # Fabricante de Preparaciones Concentradas o en Polvo para la Elaboración de Bebidas
    importadorPreparacionesBebidas = "92"  # Importador de Preparaciones Concentradas o en Polvo para la Elaboración de Bebidas
    espcificosAdvalorem = "A1" 
    bebidasAlcoholicasDeportivas = "A5"  # Bebidas Gaseosas, Isotónicas, Deportivas, Fortificantes, Energizantes o Estimulantes
    alcoholEtilico = "A7"  # Alcohol Etilico
    sacosSinteticos = "A9"  # Sacos Sintéticos