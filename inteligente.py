# La aspiradora inteligente podrá analizar su entorno para determinar qué acción realizar
# El usuario podrá interactuar en cualquier momento, para ensuciar un espacio, el cual la aspiradora deberá limpiar

# Para crear un entorno virtual ejecutamos el comando: python -m venv venv
# Para habilitar el entorno virtual, ejecutar el siguiente comando venv\Scripts\activate

import threading
import keyboard
import time

cuadranteALimpio = True
cuadranteBLimpio = True
posicionAspiradora = 1

def analizar():
    global posicionAspiradora
    global cuadranteALimpio
    global cuadranteBLimpio
    for i in range(1,10):
        print("-----------------------------------------------------------------------------")
        print("ESTADO:> La aspiradora está en el cuadrante: ", ("A" if posicionAspiradora == 1 else "B"))
        print("ESTADO:> El cuadrante A está: ", ("Limpio" if cuadranteALimpio else "Sucio"))
        print("ESTADO:> El cuadrante B está: ", ("Limpio" if cuadranteBLimpio else "Sucio"))
        print("-----------------------------------------------------------------------------")
        if(cuadranteALimpio and cuadranteBLimpio):
            print("ACCIÓN:> La aspiradora detectó los cuadrantes limpios no se movió")
        elif(posicionAspiradora == 1 and cuadranteALimpio and not cuadranteBLimpio):
            posicionAspiradora=2
            print("ACCIÓN:> La aspiradora se movió al cuadrante B")
            aspirar()
        elif(posicionAspiradora == 1 and not cuadranteALimpio):
            aspirar()
        elif(posicionAspiradora == 2 and cuadranteBLimpio and not cuadranteALimpio):
            posicionAspiradora=1
            print("ACCIÓN:> La aspiradora se movió al cuadrante A")
            aspirar()
        elif(posicionAspiradora == 2 and not cuadranteBLimpio):
            aspirar()
        time.sleep(3)
    print("Finalizando el hilo de análisis")

def aspirar():
    global posicionAspiradora
    global cuadranteALimpio
    global cuadranteBLimpio

    if(posicionAspiradora==1):
        cuadranteALimpio=True
        print("ACCIÓN:> La aspiradora limpió el cuadrante A")
    elif(posicionAspiradora==2):
        cuadranteBLimpio=True
        print("ACCIÓN:> La aspiradora limpió el cuadrante B")

def teclado_escucha(exit_event):
    def on_key_event(e):
        global cuadranteALimpio
        global cuadranteBLimpio

        if e.event_type == keyboard.KEY_DOWN:
            if e.name == 'a':
                print("ACCION:> Se ensució el cuadrante A")
                cuadranteALimpio=False
            elif e.name == 's':
                print("ACCION:> Se ensució el cuadrante B")
                cuadranteBLimpio=False
            elif e.name == 'd':
                print("Finalizando el hilo de interacción")
                exit_event.set()

    # Configurar el manejador de eventos de teclado
    keyboard.hook(on_key_event)

    # Mantener el hilo en ejecución hasta que se establezca la señal de salida
    while not exit_event.is_set():
        time.sleep(0.1)

    # Limpiar el manejador de eventos al finalizar el hilo
    keyboard.unhook_all()

if __name__ == "__main__":
    # Crear un evento para señalizar la salida del hilo
    exit_event = threading.Event()

    # Crear un hilo para la escucha de teclas
    hilo_interaccion = threading.Thread(target=teclado_escucha, args=(exit_event,))
    hilo_aspiradora = threading.Thread(target=analizar)

    # Iniciar el hilo
    hilo_aspiradora.start()
    hilo_interaccion.start()

    # Esperar a que el hilo termine (no bloquea el hilo principal)
    hilo_interaccion.join()
    hilo_aspiradora.join()

    print("Programa principal finalizado")