# Prueba Técnica – Desarrollador Python de Integraciones

Autor: Diego Andres Riveros Lopez
Fecha: Octubre 20 2025

## Descripción general

Este proyecto es la solución completa a la Prueba Técnica para Desarrollador Python de Integraciones de Fracttal.
La prueba está organizada en tres puntos principales, cada uno diseñado para demostrar diferentes habilidades técnicas:

- Pipeline asíncrono de procesamiento de pedidos con cola de trabajo

- Ejecución dinámica de funciones (transformaciones de datos)

- Diseño arquitectónico de una integración en tiempo real con ERPs (event-driven)

Cada sección se encuentra modularizada y documentada, con instrucciones claras para su ejecución.

## Requisitos previos

- Python 3.10+
- pip actualizado
- Recomendado: entorno virtual (venv o virtualenv)

### Instalar dependencias:

- pip install -r requirements.txt

## Punto 1 – Pipeline Asíncrono con Cola de Trabajo

- Ubicación: app/
- Archivo principal: cli.py
- Datos de ejemplo: data/orders.json

### Objetivo

Procesar pedidos de forma asíncrona y concurrente, incluyendo:

- Validación de datos de entrada

- Enriquecimiento de productos mediante la API FakeStoreAPI

- Cálculo de totales y descuentos

- Generación de hash único por pedido

- Persistencia en base de datos SQLite sin duplicación

- Reintentos automáticos con backoff exponencial

- Dead Letter Queue para pedidos fallidos

- Logging estructurado en formato JSON

### Ejecución
python app/cli.py --orders data/orders.json --workers 3 --db orders.db


#### Parámetros disponibles:
- --orders	Ruta al archivo JSON con pedidos	Obligatorio
- --workers	Número de workers concurrentes	3
- --db	Ruta a la base de datos SQLite	orders.db

### Ejemplo de pedido:

{
  "id": 123,
  "cliente": "ACME Corp",
  "productos": [
    {"sku": "P001", "cantidad": 3, "precio_unitario": 10},
    {"sku": "P002", "cantidad": 5, "precio_unitario": 20}
  ],
  "fecha": "2025-01-01T10:30:00Z"
}

### **Resultados persistidos en la tabla processed_orders.**

## Punto 2 – Ejecutor Dinámico de Funciones

- Ubicación: operations/
- Archivo principal: main.py
- Funciones: ops.py

### Objetivo

Implementar un sistema capaz de ejecutar transformaciones de datos dinámicamente sin necesidad de modificar el código principal.
Incluye funciones de ejemplo:
- suma(var1, var2)
- resta(var1, var2)
- mayuscula_a_minuscula(var1, var2=None)
- concat_ws(var1, var2)

### Ejecución
- python operations/main.py <funcion> <var1> <var2>


### Ejemplos:
- python operations/main.py suma 10 5
- python operations/main.py mayuscula_a_minuscula HOLA MUNDO
- python operations/main.py concat_ws hola mundo

## Punto 3 – Arquitectura de Integración en Tiempo Real (EDA)

- Ubicación: architecture/
- Documentación: arquitectura_eventos.md
- Diagrama: diagrama.png

### Objetivo

Diseñar una arquitectura de integración basada en eventos (Event-Driven Architecture) para permitir que Fracttal emita eventos en tiempo real ante cambios relevantes, evitando el uso de polling y permitiendo escalabilidad multitenant.

- Componentes principales
- Event Emitter: Emisión de eventos con Webhooks, Outbox Pattern o CDC.
- Event Bus: Transporte asíncrono con Kafka, RabbitMQ o Pub/Sub.
- Event Processor & Transformer: Aplicación de transformaciones y reglas.
- Tenant Router: Enrutamiento.
- ERP Connectors: Entrega de eventos con reintentos automáticos y DLQ.
- Dead Letter Queue: Manejo de errores y reprocesamiento.

### El diseño considera:

- Multitenancy con partición.
- Reutilización de transformaciones existentes.
- Reintentos automáticos con backoff exponencial.
- Observabilidad y trazabilidad de eventos.
- Soporte para alto volumen de datos (bulk ingestion o CDC).

### - **Para ver todos los detalles técnicos y opciones tecnológicas, consulta el archivo architecture/arquitectura_eventos_fracttal.md**

### - **Visualiza el diagrama architecture/diagrama.png**

## Contacto
- Autor: Diego Andres Riveros Lopez
- Email: diegoriveross06@gmail.com
- Fecha de entrega: Octubre 20 2025
