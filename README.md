# sdlc-electronica-angel-libreros
# Driver UART modernizado

Este proyecto implementa un driver UART modular en Python. Su función es recibir datos, interpretarlos mediante distintos protocolos, almacenar temporalmente los resultados y generar registros estructurados.

## Funcionamiento general

El funcionamiento del driver sigue este flujo:

1. `UartConfig` define y valida los parámetros de comunicación.
2. `UartDevice` controla la conexión y desconexión del dispositivo.
3. Al recibir una trama, el dispositivo la entrega al parser configurado.
4. El parser valida e interpreta los datos según el protocolo correspondiente.
5. El resultado puede almacenarse en un búfer circular.
6. Los mensajes pueden guardarse mediante JSON Lines o registrarse como eventos JSON.

El driver permite trabajar con los siguientes protocolos:

- **Modbus RTU:** valida la trama mediante CRC-16.
- **NMEA GPGGA:** comprueba el checksum y convierte las coordenadas a grados decimales.
- **CAN simplificado:** interpreta la cabecera, el identificador de 11 bits, el DLC y los datos.

## Componentes principales

- `config.py`: configuración y validación de los parámetros UART.
- `parsers.py`: interpretación de tramas Modbus RTU, NMEA GPGGA y CAN simplificado.
- `device.py`: conexión, desconexión y procesamiento de datos.
- `buffer.py`: almacenamiento temporal mediante un búfer circular seguro para concurrencia.
- `recorder.py`: almacenamiento de mensajes en formato JSON Lines.
- `json_logging.py`: generación de registros estructurados en formato JSON.

<!-- ## Reflexión sobre los principios SOLID -->

El desarrollo del driver permitió aplicar los principios SOLID estudiados durante la semana.

### Responsabilidad única — SRP

Cada módulo tiene una responsabilidad específica. La configuración, el procesamiento de protocolos, el control del dispositivo, el almacenamiento y el registro se encuentran separados.

Esta división evita que `UartDevice` concentre toda la lógica del sistema y facilita localizar errores o modificar un componente sin afectar innecesariamente a los demás.

### Abierto/cerrado — OCP

El driver puede ampliarse mediante nuevos parsers sin modificar el comportamiento principal de `UartDevice`.

Para incorporar otro protocolo solamente sería necesario crear un parser compatible e inyectarlo al dispositivo. Esto mantiene el sistema abierto a extensiones y reduce los cambios sobre el código existente.

### Sustitución de Liskov — LSP

Los diferentes parsers pueden sustituirse entre sí porque todos cumplen con la operación de procesamiento esperada por el dispositivo.

`UartDevice` puede trabajar con Modbus RTU, NMEA GPGGA o CAN simplificado sin cambiar su lógica interna. Cada parser conserva el comportamiento esperado y devuelve un resultado compatible.

### Segregación de interfaces — ISP

Las responsabilidades se representan mediante contratos pequeños. Un parser solamente necesita procesar datos y un búfer únicamente debe recibir los resultados.

De esta manera, los componentes no están obligados a implementar operaciones que no necesitan.

### Inversión de dependencias — DIP

`UartDevice` no crea internamente un parser o un búfer específico. Estas dependencias se proporcionan desde el exterior al construir el dispositivo.

Esto disminuye el acoplamiento, permite cambiar las implementaciones y facilita utilizar objetos controlados durante las pruebas.

## Conclusión

La aplicación de SOLID permitió transformar el driver UART en un conjunto de componentes pequeños, comprensibles y reemplazables. La principal ventaja del diseño es que cada parte puede modificarse o extenderse sin reconstruir el sistema completo.

El ejercicio también permitió comprender que aplicar SOLID no consiste únicamente en dividir el código en varios archivos, sino en asignar responsabilidades claras y definir correctamente la relación entre los componentes.

## Ejecución de las pruebas

Desde la raíz del repositorio y con el entorno virtual activado:

```bash
python -m pytest
```

Al finalizar el desarrollo, todas las pruebas automatizadas se ejecutaron correctamente.