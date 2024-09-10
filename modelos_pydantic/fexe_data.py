data_fe = {
    "identificacion": {
        "version": 3,
        "ambiente":"00",
        "tipoDte": "03",
        "numeroControl": "DTE-11-ABCDE1F1-123456789012345",
        "codigoGeneracion": "516413E3-12A2-78D5-7A79-6B6DFE861395",
        "tipoModelo": 2,
        "tipoOperacion": 2,
        "tipoContingencia": 5,
        "motivoContin": "contin",
        "fecEmi": "2022-10-20",
        "horEmi": "11:02:49",
        "tipoMoneda": "USD" 
    },
    
    "emisor":{
        "nit":"11111111111111",
        "nrc":"11",
        "nombre":"Albert sdfd",
        "codActividad": "62020",
        "descActividad": "venta de pelotas",
        "nombreComercial": "pelitinhas",
        "tipoEstablecimiento": "02",
        "direccion":{
            "departamento": "05",
            "municipio": "22",
            "complemento": "cerca a la piscina municipal",   
        },
        "telefono": "123456789",
        "correo":"albertPelo@gmail.com",
        "codEstable": "23kj",
        "codPuntoVenta": "1111",
        "codEstableMH": "4577",
        "codPuntoVentaMH": "4578",
        "tipoItemExpor": 1,
        "recintoFiscal": "sd",
        "regimen": None, 
    },
    #en el ejemplo original no existen tipo de docuemnto y numero de documento, igual ambos son opcionales
    "receptor":{
        "nombre": "los importadores",
        "tipoDocumento":"36",
        "saludo": "hola mundo",
        "numDocumento": "kjsdlfajd",
        "nombreComercial":"Jhon Salchichon",
        "codPais": '9539',
        "nombrePais": "albania",
        "complemento": "complementados",
        "tipoPersona": 1,
        "descActividad": "importador electrodomesticos ",
        "telefono":"98203840339",
        "correo":"jhonsalchichon@gmail.com",
    },
    # # "otrosDocumentos": None
    "otrosDocumentos":[
      {
        "codDocAsociado": 4,
        "descDocumento": None,
        "detalleDocumento": "kasdlkjf de riños",
        "placaTrans": "fdkjlj",
        "modoTransp": 4,
        "numConductor": "23900923",
        "nombreConductor": "pedrito de los palotes",
      }
      ],
      "ventaTercero":None, 
    "cuerpoDocumento": [
        {
          "numItem": 1,
          "cantidad": 1,
          "codigo": "12",
          "uniMedida": 99,
          "descripcion": "bebidas gaseosas ",
          "precioUni": 3,
          "montoDescu": 1,
          "ventaGravada": 1,
          "tributos": {
            "22", "C3"},
          # "tributos": None,
          "noGravado": 0,
        },
      ],
    "resumen": {
      "totalGravada": 0,
      "descuento": 0,
      "porcentajeDescuento": 0,
      "totalDescu": 0,
      "seguro": 1221,
      "flete": 0,
      "montoTotalOperacion": 1100,
      "totalNoGravado": 0,
      "totalPagar": 0,
      "totalLetras": "34 letras",
      "condicionOperacion": 1,
       "pagos": [
         {
         "codigo":"02",
          "montoPago": 20,
          "referencia":"compra de combustible",
          "periodo":12,
         } 
      ],
      "codIncoterms": "32",
      "descIncoterms": "232",
      "numPagoElectronico": None,
      "observaciones": "todo bien",
    },
  
    # "apendice":None,
    "apendice": [
      {
        "campo": "hola mundo",
        "etiqueta": "saludos ",
        "valor": "laksjldjfakldjlkdkjkl"
      }
    ]

    
}
