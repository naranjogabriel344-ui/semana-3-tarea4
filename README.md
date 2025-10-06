# Bot de Trading para IQ Option (Estrategia RSI)

Este es un bot de trading simple diseñado para operar en la plataforma IQ Option. Implementa una estrategia de scalping basada en el **Índice de Fuerza Relativa (RSI)**.

**ADVERTENCIA MUY IMPORTANTE:** Este bot utiliza una API no oficial de IQ Option y se proporciona **únicamente con fines educativos y de estudio**. No lo utilices en una cuenta con dinero real. El uso de este software es bajo tu propio riesgo. Se recomienda encarecidamente usarlo solo en la **cuenta de práctica**.

---

## 1. Requisitos Previos

- Python 3.7 o superior.

---

## 2. Instalación

Sigue estos pasos para configurar el entorno:

**a. Clona o descarga este repositorio.**

**b. Instala las dependencias:**
Abre una terminal o línea de comandos en la carpeta del proyecto y ejecuta el siguiente comando. Esto instalará la API de IQ Option y otras librerías necesarias.

```bash
pip install -r requirements.txt
```

---

## 3. Configuración

Antes de ejecutar el bot, necesitas configurarlo con tus credenciales de IQ Option.

**a. Abre el archivo `trading_bot.py`** con un editor de texto o código.

**b. Edita tus credenciales:**
Busca la sección `main()` al final del archivo y reemplaza los valores de `email` y `password` con los de tu cuenta de IQ Option (recuerda, ¡la de práctica!).

```python
def main():
    # ...
    # Reemplaza con tus credenciales de IQ Option.
    email = "TU_EMAIL@EJEMPLO.COM"  # <-- PON TU EMAIL AQUÍ
    password = "TU_PASSWORD"        # <-- PON TU CONTRASEÑA AQUÍ
    # ...
```

**(Opcional) Configura la estrategia:**
En la misma sección, puedes ajustar los parámetros de la estrategia si lo deseas (por ejemplo, cambiar el activo o los niveles del RSI).

```python
    # ...
    # bot = TradingBot(email, password) # Estrategia por defecto

    # Ejemplo con parámetros personalizados:
    # bot = TradingBot(
    #     email,
    #     password,
    #     active="EURGBP",
    #     rsi_overbought=80,
    #     rsi_oversold=20
    # )
    # ...
```

---

## 4. Ejecución

Una vez configurado, puedes ejecutar el bot con el siguiente comando en tu terminal:

```bash
python trading_bot.py
```

El bot se conectará a IQ Option, cambiará a la cuenta de práctica y comenzará a analizar el mercado. Verás mensajes en la consola que indican el RSI actual y las operaciones que realiza.

Para detener el bot, simplemente presiona `Ctrl + C` en la terminal.