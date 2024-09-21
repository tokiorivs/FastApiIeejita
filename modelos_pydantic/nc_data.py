data_nc= {
    "identificacion": {
        "version": 3,
        "ambiente":"00",
        "tipoDte": "05",
        "numeroControl": "DTE-05-F0000000-311111111111111",
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
    "documentoRelacionado": [
      # {
      #   "tipoDocumento": "03",
      #   "tipoGeneracion":2,
      #   "numeroDocumento": "12345678-E89B-12D3-A456-123456789012",
      #   "fechaEmision":"2024-01-01"
      # },
      {
        "tipoDocumento":"07",
        "tipoGeneracion":2,
        "numeroDocumento":"12345678-1893-1233-A456-426614174000",
        "fechaEmision":"2024-01-01",
      }
    ],
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
       
    },
    # # #en el ejemplo original no existen tipo de docuemnto y numero de documento, igual ambos son opcionales
    "receptor":{
        "nit":"111111111",
        "nrc":"111111",
        "nombre":"Jhon Salchichon",
        "codActividad": "46495",
        "descActividad": "peluquero ",
        "nombreComercial":"akjsdfl",
        "direccion":{
            "departamento": "01",
            "municipio": "11",
            "complemento":"cerca al patio de comidas"
        },
        "telefono":"98203840339",
        "correo":"jhonsalchichon@gmail.com",
    },
    "ventaTercero":{
        "nit":"111111111",
        "nombre":"Jhon Salchichon",
    },
    "cuerpoDocumento":[
        {
          "numItem": 1,
          "tipoItem": 4,
          "numeroDocumento":"01",
          "codTributo":"57",
          "codigo": "12",
          "codTritubo":1,
          "descripcion": "bebidas gaseosas",
          "cantidad": 1,
          "uniMedida": 99,
          "precioUni": 3,
          "montoDescu": 1,
          "ventaNoSuj":1,
          "ventaExenta":2,
          "ventaGravada":1,
          "tributos":[
            "C3","59","20"
            ],
          # "tributos": None,
        },
      ],
    "resumen": {
      "totalNoSuj":0,
      "totalExenta":0,
      "totalGravada":0,
      "subTotalVentas":0,
      "descuNoSuj":0,
      "descuExenta":0,
      "descuGravada":0,
      "totalDescu":0,
      "tributos":[
       {
       "codigo":"A8",
       "descripcion":"mundo",
       "valor":1, 
       },
      ],
      "subTotal":0,
      "ivaPercil":0,
      "ivaRetel": 0,
      "reteRenta": 0,
      "montoTotalOperacion":0,
      "totalLetras": "02",
      "condicionOperacion": 2,
    },
    "extension": {
      "nombEntrega": "holss",
      "docuEntrega": " asddfs",
      "nombRecibe": " dfdsff",
      "docuRecibe": "fdfddfd",
      "observaciones": "fdfd",
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
