data_fse = {
    "identificacion": {
        "version": 1,
        "ambiente":"00",
        "tipoDte": "01",
        "numeroControl": "DTE-14-F0000000-311111111111111",
        "codigoGeneracion": "516413E3-12A2-78D5-7A79-6B6DFE861395",
        "tipoModelo": 1,
        "tipoOperacion": 1,
        "tipoContingencia": None,
        "motivoContin": None,
        "fecEmi": "2022-10-20",
        "horEmi": "11:02:49",
        "tipoMoneda": "USD" 
    },
    # "documentoRelacionado": None,
    # "documentoRelacionado": [
    #   {
    #     "tipoDocumento": "04",
    #     "tipoGeneracion":2,
    #     "numeroDocumento": "123E4567-E89B-12D3-A456-426614174000",
    #     "fechaEmision":"2024-01-01"
    #   },
    #   {
    #     "tipoDocumento": "09",
    #     "tipoGeneracion":2,
    #     "numeroDocumento": "123E4567-E89B-12D3-A456-426614174000",
    #     "fechaEmision":"2024-01-01"
    #   }
    # ],
    "emisor":{
        "nit":"11111111111111",
        "nrc":"1",
        "nombre":"Albert sdfd",
        "codActividad": "111111",
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
        "codEstable": "1234",
        "codPuntoVenta": "12",
        "codEstableMH": "1232",
        "codPuntoVentaMH": "4578"  
    },
    # # #en el ejemplo original no existen tipo de docuemnto y numero de documento, igual ambos son opcionales
    "sujetoExcluido":{
        "nit":"111111111",
        "tipoDocumento":"36",
        "numDocumento": "11111111111111",
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
        "nombreComercial":"akjsdfl",
    },
    
          
    "cuerpoDocumento": [
        {
          "numItem": 1,
          "tipoItem": 3,
          "cantidad": 1,
          "codigo": "12",
          "uniMedida": 99,
          "descripcion": "bebidas gaseosas ",
          "precioUni": 3,
          "montoDescu": 1,
          "compra": 0,
        },
      ],
    "resumen": {
      "totalCompra": 0,
      "descu": 0,
      "totalDescu": 0,
      "subtotal": 0,
      "ivaRetel": 0,
      "reteRenta": 0,
      "totalPagar": 0,
      "totalLetras": " ",
      "saldoFavor": 0,
      "condicionOperacion": 2,
      "pagos": [
         {
         "codigo":"02",
          "montoPago": 20,
          "referencia":"compra de combustible",
          "plazo":"01",
          "periodo":12,
         } 
      ],
    # "pagos":None,
      "observaciones": "hola",
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
