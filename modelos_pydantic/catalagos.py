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

class TributosResumenDte(str, Enum):
    iva13 = "20"  # Impuesto al Valor Agregado 13%/
    ivaExportaciones = "C3"  # Impuesto al Valor Agregado (exportaciones) 0%
    turismoAlojamiento = "59"  # Turismo: por alojamiento (5%)
    turismoSalidaAerea = "71"  # Turismo: salida del país por vía aérea $7.00
    fovial = "D1"  # FOVIAL ($0.20 Ctvs. por galón)
    cotrans = "D2"  # COTRANS ($0.10 Ctvs. por galón)/
    otrasTasasCasosEspeciales = "D5"  # Otras tasas casos especiales
    otrosImpuestosCasosEspeciales = "D4"  # Otros impuestos casos especiales

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




#CAT-020 Tipo de persona
class TipoPersona(int, Enum):
    personaNatural = 1
    personaJuridica = 2  
#CAT-026 Tipo Donacion
class TipoDonacion(int, Enum):
    efectivo = 1,
    bien = 2,
    servicio = 3,
    
#CAT-030 Transporte
class Transporte(int, Enum):
    terrestre= 1
    aereo= 2
    maritimo= 3
    ferreo= 4
    multimodal= 5
    correo= 6
#CAT-032 Domicilio fiscal
class DomicilioFiscal(int, Enum):
    domiciliado= 1
    noDomiciliado= 2    

class CodPais(str, Enum):
    _9320 = "9320"
    _9539 = "9539"
    _9565 = "9565"
    _9905 = "9905"
    _9999 = "9999"
    _9303 = "9303"
    _9306 = "9306"
    _9309 = "9309"
    _9310 = "9310"
    _9315 = "9315"
    _9317 = "9317"
    _9318 = "9318"
    _9319 = "9319"
    _9324 = "9324"
    _9327 = "9327"
    _9330 = "9330"
    _9333 = "9333"
    _9336 = "9336"
    _9339 = "9339"
    _9342 = "9342"
    _9345 = "9345"
    _9348 = "9348"
    _9349 = "9349"
    _9350 = "9350"
    _9354 = "9354"
    _9357 = "9357"
    _9360 = "9360"
    _9363 = "9363"
    _9366 = "9366"
    _9372 = "9372"
    _9374 = "9374"
    _9375 = "9375"
    _9377 = "9377"
    _9378 = "9378"
    _9381 = "9381"
    _9384 = "9384"
    _9387 = "9387"
    _9390 = "9390"
    _9393 = "9393"
    _9394 = "9394"
    _9396 = "9396"
    _9399 = "9399"
    _9402 = "9402"
    _9405 = "9405"
    _9408 = "9408"
    _9411 = "9411"
    _9414 = "9414"
    _9417 = "9417"
    _9420 = "9420"
    _9423 = "9423"
    _9426 = "9426"
    _9432 = "9432"
    _9435 = "9435"
    _9438 = "9438"
    _9440 = "9440"
    _9441 = "9441"
    _9444 = "9444"
    _9446 = "9446"
    _9447 = "9447"
    _9450 = "9450"
    _9453 = "9453"
    _9456 = "9456"
    _9459 = "9459"
    _9462 = "9462"
    _9465 = "9465"
    _9468 = "9468"
    _9471 = "9471"
    _9474 = "9474"
    _9477 = "9477"
    _9480 = "9480"
    _9481 = "9481"
    _9483 = "9483"
    _9486 = "9486"
    _9487 = "9487"
    _9495 = "9495"
    _9498 = "9498"
    _9501 = "9501"
    _9504 = "9504"
    _9507 = "9507"
    _9513 = "9513"
    _9516 = "9516"
    _9519 = "9519"
    _9522 = "9522"
    _9525 = "9525"
    _9526 = "9526"
    _9528 = "9528"
    _9531 = "9531"
    _9534 = "9534"
    _9537 = "9537"
    _9540 = "9540"
    _9543 = "9543"
    _9544 = "9544"
    _9546 = "9546"
    _9549 = "9549"
    _9552 = "9552"
    _9555 = "9555"
    _9558 = "9558"
    _9561 = "9561"
    _9564 = "9564"
    _9567 = "9567"
    _9570 = "9570"
    _9573 = "9573"
    _9576 = "9576"
    _9577 = "9577"
    _9582 = "9582"
    _9585 = "9585"
    _9591 = "9591"
    _9594 = "9594"
    _9597 = "9597"
    _9600 = "9600"
    _9601 = "9601"
    _9603 = "9603"
    _9606 = "9606"
    _9609 = "9609"
    _9611 = "9611"
    _9612 = "9612"
    _9615 = "9615"
    _9618 = "9618"
    _9621 = "9621"
    _9624 = "9624"
    _9627 = "9627"
    _9633 = "9633"
    _9636 = "9636"
    _9638 = "9638"
    _9639 = "9639"
    _9642 = "9642"
    _9645 = "9645"
    _9648 = "9648"
    _9651 = "9651"
    _9660 = "9660"
    _9663 = "9663"
    _9666 = "9666"
    _9669 = "9669"
    _9672 = "9672"
    _9675 = "9675"
    _9677 = "9677"
    _9678 = "9678"
    _9679 = "9679"
    _9680 = "9680"
    _9681 = "9681"
    _9682 = "9682"
    _9683 = "9683"
    _9684 = "9684"
    _9687 = "9687"
    _9690 = "9690"
    _9691 = "9691"
    _9693 = "9693"
    _9696 = "9696"
    _9699 = "9699"
    _9702 = "9702"
    _9705 = "9705"
    _9706 = "9706"
    _9707 = "9707"
    _9708 = "9708"
    _9714 = "9714"
    _9717 = "9717"
    _9720 = "9720"
    _9722 = "9722"
    _9723 = "9723"
    _9725 = "9725"
    _9726 = "9726"
    _9727 = "9727"
    _9729 = "9729"
    _9732 = "9732"
    _9735 = "9735"
    _9738 = "9738"
    _9739 = "9739"
    _9740 = "9740"
    _9741 = "9741"
    _9744 = "9744"
    _9747 = "9747"
    _9750 = "9750"
    _9756 = "9756"
    _9758 = "9758"
    _9759 = "9759"
    _9760 = "9760"
    _9850 = "9850"
    _9862 = "9862"
    _9863 = "9863"
    _9865 = "9865"
    _9886 = "9886"
    _9898 = "9898"
    _9899 = "9899"
    _9897 = "9897"
    _9887 = "9887"
    _9571 = "9571"
    _9300 = "9300"
    _9369 = "9369"
    _9439 = "9439"
    _9510 = "9510"
    _9579 = "9579"
    _9654 = "9654"
    _9711 = "9711"
    _9736 = "9736"
    _9737 = "9737"
    _9640 = "9640"
    _9641 = "9641"
    _9673 = "9673"
    _9472 = "9472"
    _9311 = "9311"
    _9733 = "9733"
    _9541 = "9541"
    _9746 = "9746"
    _9551 = "9551"
    _9451 = "9451"
    _9338 = "9338"
    _9353 = "9353"
    _9482 = "9482"
    _9494 = "9494"
    _9524 = "9524"
    _9304 = "9304"
    _9332 = "9332"
    _9454 = "9454"
    _9457 = "9457"
    _9489 = "9489"
    _9491 = "9491"
    _9492 = "9492"
    _9523 = "9523"
    _9530 = "9530"
    _9532 = "9532"
    _9535 = "9535"
    _9542 = "9542"
    _9547 = "9547"
    _9548 = "9548"
    _9574 = "9574"
    _9598 = "9598"
    _9602 = "9602"
    _9607 = "9607"
    _9608 = "9608"
    _9623 = "9623"
    _9652 = "9652"
    _9692 = "9692"
    _9709 = "9709"
    _9712 = "9712"
    _9716 = "9716"
    _9718 = "9718"
    _9719 = "9719"
    _9751 = "9751"
    _9452 = "9452"
    _9901 = "9901"
    _9902 = "9902"
    _9903 = "9903"
    _9664 = "9664"
    _9415 = "9415"
    _9904 = "9904"
    _9514 = "9514"
    _9906 = "9906"
    _9359 = "9359"
    _9493 = "9493"
    _9521 = "9521"
    _9533 = "9533"
    _9538 = "9538"
    _9689 = "9689"
    _9713 = "9713"
    _9449 = "9449"
    _9888 = "9888"
    _9490 = "9490"
    _9527 = "9527"
    _9529 = "9529"
    _9536 = "9536"
    _9545 = "9545"
    _9568 = "9568"
    _9610 = "9610"
    _9622 = "9622"
    _9643 = "9643"
    _9667 = "9667"
    _9676 = "9676"
    _9685 = "9685"
    _9686 = "9686"
    _9688 = "9688"
    _9715 = "9715"
    _9900 = "9900"
    _9371 = "9371"
    _9376 = "9376"
    _9907 = "9907"
    
    