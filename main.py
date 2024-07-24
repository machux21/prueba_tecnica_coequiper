#PREGUNTA TÉCNICA COEQUIPER
"""
    Escribí el código en python para agregar funcionalidad de trabajo 
    mediante una cola estilo producer/consumer, 
    donde el método que ejecuta dichos componentes se ejecuta en paralelo con multiprocesamiento, 
    por lo cual ambos componentes no comparten datos en memoria.

"""

# Import de librerías necesarias
import multiprocessing
import time
import random


def producer(queue, event):

    """
        Funcionamiento: 
        
            Genera (datos) números aleatorios y los pone en la cola
    """
    while not event.is_set(): # Verificación por si el evento ha sido activado -> indica cuándo detenerse

        item = random.randint(1, 100) # Generación de un número aleatorio entre 1 y 100
        
        queue.put(item) # Almacenamiento del item en la cola
        
        print(f'Producer: item {item} generado')
        
        time.sleep(random.random())  # Agregado de un tiempo para simular variabilidad

def consumer(queue, event):

    """
        Funcionamiento:
            Consume datos de la cola proveniente de Producer
    """
    while not event.is_set() or not queue.empty(): # Verificación por si el evento ha sido activado  o mientras la cola contenga datos -> lo que ocurra primero 

        item = queue.get() # Extracción de un número de la cola

        print(f'Consumer: item {item} consumido')

        time.sleep(random.random()) # Agregado de un tiempo para simular variabilidad


if __name__ == "__main__":

    # 1. Creación de la cola de comunicación
    queue = multiprocessing.Queue()

    # 2. Creación del evento para señalizar el cierre
    event = multiprocessing.Event()

    # 3. Creación de procesos para el productor y el consumidor
    producer_process = multiprocessing.Process(target=producer, args=(queue, event))
    consumer_process = multiprocessing.Process(target=consumer, args=(queue, event))

    # 4. Comienzo de los procesos
    producer_process.start()
    consumer_process.start()

    # 5. Ejecución por un tiempo determinado
    time.sleep(5)

    # 6. Señalización a los procesos para que terminen
    event.set()

    # 7. Esperar que los procesos terminen
    producer_process.join()
    consumer_process.join()

    print("Proceso finalizado :)")

##############################
##  EXPLICACIÓN DEL PROCESO ##  
##############################
"""
    Partícipes del proceso:

        * Productor
        * Consumidor
        * Cola (Queue)
        * Evento (Event)
    
    1. El productor genera números aleatorios y los coloca en una cola
    2. El consumidor toma números de la cola y los procesa
    3. La cola permite la comunicación entre el productor y el consumidor
    4. El evento señala cuándo los procesos deben detenerse
    5. El bloque principal crea y maneja los procesos

    De esta manera los procesos no comparten datos en memoria pero se comunican a través de una cola

"""