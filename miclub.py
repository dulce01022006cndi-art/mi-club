"""
MiClub - Sistema de Gestión de Clientes VIP
Sistema simple para gestionar clientes con niveles y descuentos
"""

from datetime import datetime
import json


class Nivel:
    """Clase base para niveles de cliente"""
    def __init__(self, nombre, descuento):
        self.nombre = nombre
        self.descuento = descuento
    
    def __str__(self):
        return f"{self.nombre} ({self.descuento}%)"


# Definir los 4 niveles
NIVELES = {
    'cobre': Nivel('Cobre', 5),
    'plata': Nivel('Plata', 10),
    'oro': Nivel('Oro', 15),
    'diamante': Nivel('Diamante', 20)
}


class Cliente:
    """Representa un cliente con su información y nivel"""
    
    def __init__(self, id_cliente, nombre, direccion, ano_registro):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.direccion = direccion
        self.ano_registro = ano_registro
        self.nivel = NIVELES['cobre']  # Nivel inicial
        self.servicios = []
    
    def cambiar_nivel(self, nivel_nombre):
        """Cambia el nivel del cliente"""
        if nivel_nombre in NIVELES:
            self.nivel = NIVELES[nivel_nombre]
            return True
        return False
    
    def agregar_servicio(self, servicio):
        """Agrega un servicio al historial del cliente"""
        self.servicios.append({
            'servicio': servicio,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
    
    def calcular_descuento(self, monto):
        """Calcula el descuento según el nivel"""
        descuento = monto * (self.nivel.descuento / 100)
        total = monto - descuento
        return {
            'monto_original': monto,
            'descuento': descuento,
            'total_a_pagar': total,
            'porcentaje': self.nivel.descuento
        }
    
    def to_dict(self):
        """Convierte el cliente a diccionario para guardar"""
        return {
            'id': self.id_cliente,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'ano_registro': self.ano_registro,
            'nivel': self.nivel.nombre.lower(),
            'servicios': self.servicios
        }
    
    def __str__(self):
        return f"{self.nombre} (ID: {self.id_cliente}) - Nivel {self.nivel}"


class Empresa:
    """Gestiona la empresa y sus clientes"""
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.clientes = {}  # Diccionario: id -> Cliente
    
    def agregar_cliente(self, id_cliente, nombre, direccion, ano_registro=None):
        """Agrega un nuevo cliente"""
        if id_cliente in self.clientes:
            raise ValueError(f"ERROR: El ID {id_cliente} ya existe")
        
        if ano_registro is None:
            ano_registro = datetime.now().year
        
        cliente = Cliente(id_cliente, nombre, direccion, ano_registro)
        self.clientes[id_cliente] = cliente
        return cliente
    
    def obtener_cliente(self, id_cliente):
        """Obtiene un cliente por ID"""
        if id_cliente not in self.clientes:
            raise ValueError(f"ERROR: El cliente ID {id_cliente} no existe")
        return self.clientes[id_cliente]
    
    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente"""
        if id_cliente not in self.clientes:
            raise ValueError(f"ERROR: El cliente ID {id_cliente} no existe")
        del self.clientes[id_cliente]
    
    def listar_clientes(self):
        """Lista todos los clientes"""
        return list(self.clientes.values())
    
    def cambiar_nivel_cliente(self, id_cliente, nivel):
        """Cambia el nivel de un cliente"""
        cliente = self.obtener_cliente(id_cliente)
        if cliente.cambiar_nivel(nivel):
            return cliente
        raise ValueError(f"ERROR: Nivel '{nivel}' no válido")
    
    def aplicar_descuento(self, id_cliente, monto):
        """Aplica descuento según nivel del cliente"""
        cliente = self.obtener_cliente(id_cliente)
        return cliente.calcular_descuento(monto)
    
    def guardar_datos(self, archivo='empresa_data.json'):
        """Guarda los datos en un archivo JSON"""
        datos = {
            'nombre_empresa': self.nombre,
            'clientes': [c.to_dict() for c in self.clientes.values()]
        }
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    def cargar_datos(self, archivo='empresa_data.json'):
        """Carga los datos desde un archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            self.nombre = datos['nombre_empresa']
            self.clientes = {}
            
            for c in datos['clientes']:
                cliente = Cliente(c['id'], c['nombre'], c['direccion'], c['ano_registro'])
                cliente.cambiar_nivel(c['nivel'])
                cliente.servicios = c['servicios']
                self.clientes[c['id']] = cliente
        except FileNotFoundError:
            print(f"Archivo {archivo} no encontrado. Iniciando con datos vacíos.")


# ==========================================
# FUNCIONES DEL MENÚ INTERACTIVO
# ==========================================

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("MICLUB - SISTEMA DE GESTION DE CLIENTES")
    print("="*50)
    print("1. Agregar nuevo cliente")
    print("2. Listar todos los clientes")
    print("3. Buscar cliente por ID")
    print("4. Cambiar nivel de cliente")
    print("5. Calcular descuento")
    print("6. Eliminar cliente")
    print("7. Guardar datos")
    print("8. Cargar datos")
    print("9. Salir")
    print("="*50)


def agregar_cliente_menu(empresa):
    """Menú para agregar cliente"""
    print("\nAGREGAR NUEVO CLIENTE")
    try:
        id_cliente = int(input("ID del cliente (número): "))
        nombre = input("Nombre completo: ")
        direccion = input("Dirección: ")
        
        cliente = empresa.agregar_cliente(id_cliente, nombre, direccion)
        print(f"\nCliente agregado exitosamente:")
        print(f"   {cliente}")
    except ValueError as e:
        print(f"\n{e}")
    except Exception as e:
        print(f"\nError: {e}")


def listar_clientes_menu(empresa):
    """Menú para listar clientes"""
    print("\nLISTA DE CLIENTES")
    clientes = empresa.listar_clientes()
    
    if not clientes:
        print("   No hay clientes registrados.")
        return
    
    print("-" * 70)
    for cliente in clientes:
        print(f"   {cliente}")
        print(f"      Dirección: {cliente.direccion}")
        print(f"      Año de registro: {cliente.ano_registro}")
        print(f"      Servicios: {len(cliente.servicios)}")
        print("-" * 70)


def buscar_cliente_menu(empresa):
    """Menú para buscar cliente"""
    print("\nBUSCAR CLIENTE")
    try:
        id_cliente = int(input("ID del cliente: "))
        cliente = empresa.obtener_cliente(id_cliente)
        
        print(f"\nCliente encontrado:")
        print(f"   {cliente}")
        print(f"   Dirección: {cliente.direccion}")
        print(f"   Año de registro: {cliente.ano_registro}")
        print(f"   Descuento actual: {cliente.nivel.descuento}%")
        
        if cliente.servicios:
            print(f"\n   Servicios ({len(cliente.servicios)}):")
            for s in cliente.servicios:
                print(f"      - {s['servicio']} ({s['fecha']})")
    except ValueError as e:
        print(f"\n{e}")


def cambiar_nivel_menu(empresa):
    """Menú para cambiar nivel"""
    print("\nCAMBIAR NIVEL DE CLIENTE")
    try:
        id_cliente = int(input("ID del cliente: "))
        
        print("\nNiveles disponibles:")
        print("  1. Cobre (5%)")
        print("  2. Plata (10%)")
        print("  3. Oro (15%)")
        print("  4. Diamante (20%)")
        
        opcion = input("\nSelecciona nivel (1-4): ")
        niveles = ['cobre', 'plata', 'oro', 'diamante']
        
        if opcion in ['1', '2', '3', '4']:
            nivel = niveles[int(opcion) - 1]
            cliente = empresa.cambiar_nivel_cliente(id_cliente, nivel)
            print(f"\nNivel actualizado:")
            print(f"   {cliente}")
        else:
            print("Opción inválida")
    except ValueError as e:
        print(f"\n{e}")


def calcular_descuento_menu(empresa):
    """Menú para calcular descuento"""
    print("\nCALCULAR DESCUENTO")
    try:
        id_cliente = int(input("ID del cliente: "))
        monto = float(input("Monto de la compra: $"))
        
        resultado = empresa.aplicar_descuento(id_cliente, monto)
        cliente = empresa.obtener_cliente(id_cliente)
        
        print(f"\nDESGLOSE DE DESCUENTO:")
        print(f"   Cliente: {cliente.nombre}")
        print(f"   Nivel: {cliente.nivel}")
        print(f"   {'-'*40}")
        print(f"   Monto original:    ${resultado['monto_original']:.2f}")
        print(f"   Descuento ({resultado['porcentaje']}%):   -${resultado['descuento']:.2f}")
        print(f"   {'-'*40}")
        print(f"   TOTAL A PAGAR:     ${resultado['total_a_pagar']:.2f}")
    except ValueError as e:
        print(f"\n{e}")


def eliminar_cliente_menu(empresa):
    """Menú para eliminar cliente"""
    print("\nELIMINAR CLIENTE")
    try:
        id_cliente = int(input("ID del cliente a eliminar: "))
        cliente = empresa.obtener_cliente(id_cliente)
        
        confirmar = input(f"¿Seguro que deseas eliminar a '{cliente.nombre}'? (s/n): ")
        if confirmar.lower() == 's':
            empresa.eliminar_cliente(id_cliente)
            print(f"\nCliente eliminado exitosamente")
    except ValueError as e:
        print(f"\n{e}")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():
    """Función principal del programa"""
    print("\nBienvenido a MiClub")
    nombre_empresa = input("Nombre de tu empresa: ")
    
    empresa = Empresa(nombre_empresa)
    
    # Intentar cargar datos previos
    empresa.cargar_datos()
    
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción (1-9): ")
        
        if opcion == '1':
            agregar_cliente_menu(empresa)
        elif opcion == '2':
            listar_clientes_menu(empresa)
        elif opcion == '3':
            buscar_cliente_menu(empresa)
        elif opcion == '4':
            cambiar_nivel_menu(empresa)
        elif opcion == '5':
            calcular_descuento_menu(empresa)
        elif opcion == '6':
            eliminar_cliente_menu(empresa)
        elif opcion == '7':
            empresa.guardar_datos()
            print("\nDatos guardados exitosamente")
        elif opcion == '8':
            empresa.cargar_datos()
            print("\nDatos cargados exitosamente")
        elif opcion == '9':
            print("\nHasta pronto!")
            empresa.guardar_datos()  # Guardar antes de salir
            break
        else:
            print("\nOpción inválida")
        
        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()