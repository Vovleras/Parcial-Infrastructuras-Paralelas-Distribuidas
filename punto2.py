import json
from time import sleep
import pandas as pd

def leer_configuracion():
    with open("configuracion.json", "r") as f:
        config = json.load(f)  
    return [list(obj.values()) for obj in config]  

def secuencial(m, dEtapas):
    tiempoTotal = 0
    
    #simulación
    for i in range(m):
        for etapa in dEtapas:
            sleep(etapa/1000) 
            tiempoTotal += etapa
            
    return tiempoTotal

def pipelined(m, dEtapas):
    tiempoEtapaLenta= max(dEtapas)
    k = len(dEtapas) # etapas
    tiempoTotal = 0
    

    pipeline = [" " for _ in range(k)] # Llena el arreglo con " " 

    # Simulación ciclo a ciclo
    print("Ciclo ", end="")
    for i in range(k):
        print(f"    E{i + 1}", end="")
    print()
    
    
    for ciclo in range(m + k - 1):  # M instrucciones + K ciclos 
        
        # desplazar de derecha a izquierda
        for i in range(k - 1, 0, -1):
            pipeline[i] = pipeline[i - 1]
        
        # Insertar nueva instrucción si aún quedan
        if ciclo < m:
            pipeline[0] = f"I{ciclo + 1}"
        else:
            pipeline[0] = " "

        # Mostrar estado del pipeline
        print(f"Ciclo {ciclo + 1}: {pipeline}")

        # Simular el tiempo de la etapa más lenta
        sleep(tiempoEtapaLenta / 1000)
        tiempoTotal += tiempoEtapaLenta
    
        
    return tiempoTotal
        

def speed(valorm, dEtapas):
    resultados=[]

    for m in valorm:
        print(f"Simulando para m = {m} instrucciones...")

        #secuencial
        tiempoSecuencial = secuencial (m, dEtapas)
        print(f"Tiempo secuencial: {tiempoSecuencial} ms")

        #pipeline
        tiempoPipeline = pipelined(m, dEtapas)
        print(f"Tiempo en pipeline: {tiempoPipeline} ms")

        #SpeedUp
        speedup= tiempoSecuencial/tiempoPipeline
        print(f"Speedup: {speedup:.2f} \n")

        resultados.append((m, len(dEtapas), tiempoSecuencial, tiempoPipeline, speedup))
    return resultados
    
  
def mostrarTablaVariandoM():
    
    
    print("Simulacion de pipeline en matriz para diferentes valores de m: \n")
    resultado = speed([5,10,15,20,25], leer_configuracion()[0])
    print("Resultados para diferentes valores de m: \n")
    print("m\tk\tTiempo Secuencial\tTiempo Pipeline\tSpeedup")
    print("--------------------------------------------------")
      
    for m, k, ts, tp, s in resultado:
        print(f"{m}\t{k}\t{ts:.2f}\t\t{tp:.2f}\t\t{s:.2f}")
        
    print("\n")


def mostrarTablaVariandoK(m, arregloEtapas):
    resultados = []
    print("Simulacion de pipeline en matriz para diferentes valores de k: \n")
    for etapas in arregloEtapas:
        resultado = speed(m, etapas)
        resultados.extend(resultado) 
    print("Resultados para diferentes valores de K: \n")
    print("m\tk\tTiempo Secuencial\tTiempo Pipeline\tSpeedup")
    print("--------------------------------------------------")
    
    for m, k, ts, tp, s in resultados:
        print(f"{m}\t{k}\t{ts:.2f}\t\t{tp:.2f}\t\t{s:.2f}")
    print("\n")


mostrarTablaVariandoM()
mostrarTablaVariandoK([10], leer_configuracion())





     






        


    


    
    
            
            
            

    
    