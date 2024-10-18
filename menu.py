print("\nBienvenido a la calculadora de simulaciones de python.")
print("¿Que deseas realizar?")

def opciones():
    print("0. Finalizar")
    print("1. Simulador de peluquería")
    print("2. Simulador de sistema de redes")
    print("3. Simulador de reaccion quimica")
    print("4. Simulador de reactor nuclear")
    print("5. Simulador de restaurante")
    print("6. Simulador de restaurante 2")
opciones()
opcion = input("Ingresa la opcion deseada: ")
print("")

while (opcion != "0"):
    if (opcion == "1"):
        import DiscretaPeluqueria
    elif (opcion == "2"):
        import DiscretaSistemaRedes
    elif (opcion == "3"):
        import ContinuoReaccionQuimica
    elif (opcion == "4"):
        import ContinuoReactorNuclear
    elif (opcion == "5"):
        import DiscretaRestaurante
    elif (opcion == "6"):
        import DiscretaRestaurante2
    else:
        print("Opcion invalida, escoja el numero de la opcion: ")
        opciones()
        opcion = input("Ingresa la opcion deseada: ")
        continue
        
print("Programa finalizado.")