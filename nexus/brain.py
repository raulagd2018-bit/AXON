import sys
import os
# Añadimos la ruta del oracle para que el Nexus pueda verlo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from oracle.engine import AxiomaOracle

class AxiomaNexus:
    def __init__(self):
        self.oracle = AxiomaOracle()

    def procesar_intencion(self, entrada):
        if "buscar" in entrada:
            return self.oracle.buscar(entrada)
        else:
            return "Redirigiendo a otro módulo..."

if __name__ == "__main__":
    nexus = AxiomaNexus()
    print(nexus.procesar_intencion("buscar el precio de bitcoin"))
