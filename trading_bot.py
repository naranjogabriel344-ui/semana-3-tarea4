import logging
import time
import numpy as np
from iqoptionapi.stable_api import IQ_Option

# --- Configuración del Logger ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

class TradingBot:
    def __init__(self, email, password, active="EURUSD", rsi_period=14, rsi_overbought=70, rsi_oversold=30, amount=1):
        """
        Inicializa el bot con los parámetros de la estrategia.
        """
        self.email = email
        self.password = password
        self.api = None
        self.active = active
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.amount = amount
        self.last_action_time = 0

    def connect(self):
        """
        Conecta el bot a la API de IQ Option y cambia a la cuenta de práctica.
        """
        logging.info("Conectando a IQ Option...")
        self.api = IQ_Option(self.email, self.password)
        check, reason = self.api.connect()
        if check:
            logging.info("Conexión exitosa.")
            logging.info("Cambiando a cuenta de PRÁCTICA.")
            self.api.change_balance("PRACTICE")
        else:
            logging.error(f"No se pudo conectar: {reason}")
            exit()

    def calculate_rsi(self, prices):
        """
        Calcula el RSI (Índice de Fuerza Relativa).
        """
        deltas = np.diff(prices)
        seed = deltas[:self.rsi_period+1]
        up = seed[seed >= 0].sum()/self.rsi_period
        down = -seed[seed < 0].sum()/self.rsi_period
        rs = up/down
        rsi = 100.0 - (100.0 / (1.0 + rs))

        for i in range(self.rsi_period, len(prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.0
            else:
                upval = 0.0
                downval = -delta

            up = (up * (self.rsi_period - 1) + upval) / self.rsi_period
            down = (down * (self.rsi_period - 1) + downval) / self.rsi_period
            rs = up/down
            rsi = 100.0 - (100.0 / (1.0 + rs))

        return rsi

    def trade(self, action):
        """
        Ejecuta una operación de trading (CALL o PUT).
        """
        # Evitar operaciones demasiado seguidas
        if time.time() - self.last_action_time < 60:
            return

        logging.info(f"Ejecutando operación: {action} en {self.active} por ${self.amount}")
        duration = 1  # 1 minuto

        # La API de IQ Option usa 'call' y 'put' en minúsculas
        status, order_id = self.api.buy(self.amount, self.active, action.lower(), duration)

        if status:
            logging.info(f"Operación exitosa. ID: {order_id}")
            self.last_action_time = time.time()
        else:
            logging.error("No se pudo ejecutar la operación.")

    def run(self):
        """
        Lógica principal del bot que ejecuta la estrategia de RSI.
        """
        logging.info(f"Iniciando el bot de trading para {self.active}...")

        while True:
            try:
                # Obtenemos 100 velas de 1 minuto para tener datos suficientes para el RSI
                candles = self.api.get_candles(self.active, 60, 100, time.time())

                if candles:
                    # Usamos los precios de cierre para el cálculo del RSI
                    close_prices = np.array([c['close'] for c in candles])

                    current_rsi = self.calculate_rsi(close_prices)
                    logging.info(f"RSI actual para {self.active}: {current_rsi:.2f}")

                    if current_rsi > self.rsi_overbought:
                        logging.info(f"Señal de VENTA (PUT) detectada (RSI > {self.rsi_overbought})")
                        self.trade("PUT")
                    elif current_rsi < self.rsi_oversold:
                        logging.info(f"Señal de COMPRA (CALL) detectada (RSI < {self.rsi_oversold})")
                        self.trade("CALL")

                # Esperamos 60 segundos antes de la siguiente comprobación
                time.sleep(60)

            except Exception as e:
                logging.error(f"Ha ocurrido un error: {e}")
                time.sleep(15)


def main():
    """
    Función principal para configurar y ejecutar el bot.
    """
    # --- IMPORTANTE ---
    # Reemplaza con tus credenciales de IQ Option.
    # Considera usar variables de entorno para mayor seguridad en un futuro.
    email = "TU_EMAIL@EJEMPLO.COM"
    password = "TU_PASSWORD"

    if email == "TU_EMAIL@EJEMPLO.COM" or password == "TU_PASSWORD":
        logging.error("Por favor, introduce tu email y contraseña en la función main() del archivo trading_bot.py")
        return

    bot = TradingBot(email, password)
    bot.connect()
    bot.run()


if __name__ == "__main__":
    main()