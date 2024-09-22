data_fc = {
    "identificacion": {
        "version": 1,
        "ambiente":"00",
        "tipoDte": "01",
        "numeroControl": "DTE-01-F0000000-311111111111111",
        "codigoGeneracion": "516413E3-12A2-78D5-7A79-6B6DFE861395",
        "tipoModelo": 2,
        "tipoOperacion": 2,
        "tipoContingencia": None,
        "motivoContin": None,
        "fecEmi": "2022-10-20",
        "horEmi": "11:02:49",
        "tipoMoneda": "USD" 
    },
    # "documentoRelacionado": None,
    "documentoRelacionado": [
      {
        "tipoDocumento": "04",
        "tipoGeneracion":2,
        "numeroDocumento": "123E4567-E89B-12D3-A456-426614174000",
        "fechaEmision":"2024-01-01"
      },
      {
        "tipoDocumento": "09",
        "tipoGeneracion":2,
        "numeroDocumento": "123E4567-E89B-12D3-A456-426614174000",
        "fechaEmision":"2024-01-01"
      }
    ],
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
        "codEstable": "0312",
        "codPuntoVenta": "02934",
        "codEstableMH": "4577",
        "codPuntoVentaMH": "4578"  
    },
    #en el ejemplo original no existen tipo de docuemnto y numero de documento, igual ambos son opcionales
    "receptor":{
        "tipoDocumento":"13",
        "numDocumento": "11111111-1",
        # "numDocumento": None,
        "nrc":"111111",
        "nombre":"Jhon Salchichon",
        "codActividad": "46495",
        "descActividad": "peluquero ",
        "direccion":{
            "departamento": "01",
            "municipio": "11",
            "complemento":"cerca al patio de comidas"
        },
        "telefono":"98203840339",
        "correo":"jhonsalchichon@gmail.com",
        "nombreComercial":"",
        "nit":"",
    },
    # "otrosDocumentos": None
    "otrosDocumentos":[
      {
        "codDocAsociado": 2,
        "descDocumento": "skdjlnd1231231",
        #  "descDocumento": None,
        "detalleDocumento": "kasdlkjf de riños",
        # "detalleDocumento": None,
        # "medico":{
        #   "nombre": "juan perez as",
        #   "nit": "111111111",
        #   "docIdentificacion": "kjldjklsdj",
        #   "tipoServicio": 2
        #   },
        
        "medico":None
        }
      ],
    "ventaTercero": {
        "nit": "12345678912345",
        "nombre": "Juan Pérez"
    },
    
    "cuerpoDocumento": [
        {
          "numItem": 1,
          "tipoItem": 2,
          "numeroDocumento":"12",
          "cantidad": 1,
          "codigo": "12",
          "uniMedida": 99,
          "descripcion": "bebidas gaseosas ",
          "precioUni": 3,
          "montoDescu": 1,
          "codTributo": None,
          "ventaNoSuj": 1,
          "ventaExenta": 1,
          "ventaGravada": 1,
          "tributos": [
            "20"
          ],
          # "tributos": None,
          "psv": 0,
          "noGravado": 0,
          "ivaItem": 0,
        },
      ],
    "resumen": {
      "totalNoSuj": 0,
      "totalExenta": 0,
      "totalGravada": 0,
      "subTotalVentas": 0,
      "descuNoSuj": 0,
      "descuExenta": 0,
      "descuGravada": 0,
      "porcentajeDescuento": 0,
      "totalDescu": 0,
      "tributos":[
        {
        "codigo":"A8",
        "descripcion": "IVA sdfadf",
        "valor":0
        }
      ],
  
      "subTotal": 0,
      "ivaRetel": 0,
      "reteRenta": 0,
      "montoTotalOperacion": 1100,
      "totalNoGravado": 0,
      "totalPagar": 0,
      "totalLetras": " ",
      "saldoFavor": 0,
      "totalIva":0,
      "condicionOperacion": 1,
      "pagos": [
         {
         "codigo":"02",
          "montoPago": 20,
          "referencia":"compra de combustible",
          "plazo":"01",
          "periodo":12,
         } 
      ],
      "numPagoElectronico": None
    },
    "extension": {
      "nombEntrega": "holss",
      "docuEntrega": " asddfs",
      "nombRecibe": " dfdsff",
      "docuRecibe": "fdfddfd",
      "placaVehiculo": "dfddfdf",
      "observaciones": "fdfd"
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
