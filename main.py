from utils import load_data, above_year_average, below_global_average, above_mean
from avl_tree import AVLTree
from node import Node
from visualizer import draw_tree

# Función auxiliar para recolectar métricas de medias en el árbol
def collect_means_map(tree, root):
    """Devuelve un diccionario con la cantidad de nodos por cada media encontrada"""
    m = {}
    for n in tree.get_all_nodes(root):
        m[n.mean] = m.get(n.mean, 0) + 1
    return m


# Programa principal
if __name__ == "__main__":
    # Carga inicial de datos desde el CSV
    countries = load_data()

    # Se crea el árbol AVL vacío
    tree = AVLTree()
    root = None

    # Construcción del árbol con los países
    for country, iso3, values in countries:
        node = Node(country, iso3, values)
        root = tree.insert(root, node)
        if root:
            root.parent = None  # se asegura que la raíz no tenga padre

    # Menú interactivo
    while True:
        print("\n--- MENÚ ---")
        print("1. Recorrido por niveles")
        print("2. Buscar nodo por media")
        print("3. Insertar un nuevo nodo")
        print("4. Eliminar nodo por media")
        print("5. Consulta: país en año > promedio global")
        print("6. Consulta: país en año < promedio global todos los años")
        print("7. Consulta: media >= valor dado")
        print("8. Mostrar árbol gráfico")
        print("0. Salir")

        opcion = input("Seleccione: ")

        # 1. Recorrido por niveles (nivel raíz = 0)
        if opcion == "1":
            niveles = tree.level_order(root)
            for iso3, mean, lvl in niveles:
                print(f"{iso3} ({mean:.2f}) → nivel {lvl}")

        # 2. Buscar nodos exactos por media
        elif opcion == "2":
            try:
                mean = round(float(input("Ingrese media exacta a buscar (ej. 0.61): ")), 2)
                nodes = tree.search_all(root, mean)

                if nodes:
                    print(f"🔍 Se encontraron {len(nodes)} nodos con media {mean:.2f}:")
                    for i, node in enumerate(nodes, 1):
                        print(f"{i}. {node.country} ({node.iso3}), media={node.mean:.2f}")

                    # Permite al usuario seleccionar un nodo en específico
                    sel = int(input("Seleccione un nodo por número: "))
                    if 1 <= sel <= len(nodes):
                        node = nodes[sel - 1]
                        print(f"\n📌 Información del nodo {node.iso3}:")
                        print("Nivel:", tree.get_level(root, node, level=0))
                        print("Factor balance:", tree.get_balance(node))
                        print("Padre:", node.parent.iso3 if node.parent else None)
                        g = tree.get_grandparent(node)
                        print("Abuelo:", g.iso3 if g else None)
                        u = tree.get_uncle(node)
                        print("Tío:", u.iso3 if u else None)
                else:
                    print("⚠️ No se encontró ningún nodo con esa media exacta.")
            except ValueError:
                print("❌ Por favor ingrese un número válido.")

        # 3. Insertar un nuevo nodo
        elif opcion == "3":
            try:
                country = input("Ingrese nombre del país: ")
                iso3 = input("Ingrese código ISO3: ").upper()
                values = list(map(float, input("Ingrese valores separados por comas (ej: 1.2,2.3,3.4): ").split(",")))

                # Crear e insertar nodo
                node = Node(country, iso3, values)
                root = tree.insert(root, node)
                if root:
                    root.parent = None

                print(f"✅ Nodo {iso3} insertado con media {node.mean:.2f}")
                draw_tree(root, "avl_tree")
                print("Árbol actualizado y exportado a avl_tree.png")
            except ValueError:
                print("❌ Valores inválidos.")

        # 4. Eliminar nodo por media
        elif opcion == "4":
            try:
                mean = round(float(input("Ingrese media a eliminar (ej. 0.61): ")), 2)
                nodes = tree.search_all(root, mean)

                if not nodes:
                    print("⚠️ No se encontraron nodos con esa media.")
                else:
                    print(f"Se encontraron {len(nodes)} nodos con media {mean:.2f}:")
                    for i, n in enumerate(nodes, 1):
                        print(f"{i}. {n.country} ({n.iso3}), media={n.mean:.2f}")

                    sel = int(input("Seleccione el número del nodo a eliminar: "))
                    if 1 <= sel <= len(nodes):
                        node_to_delete = nodes[sel - 1]

                        deleted_iso = node_to_delete.iso3
                        deleted_country = node_to_delete.country

                        key = (node_to_delete.mean, node_to_delete.iso3)
                        root = tree.delete_one_by_key(root, key)
                        if root:
                            root.parent = None

                        print(f"🗑 Nodo eliminado: {deleted_iso} ({deleted_country})")
                        draw_tree(root, "avl_tree")
                        print("✅ Árbol actualizado y exportado a avl_tree.png")
                    else:
                        print("⚠️ Selección inválida.")
            except ValueError:
                print("❌ Por favor ingrese un número válido.")

        # 5. Consulta: países en un año > promedio global de ese año
        elif opcion == "5":
            try:
                year = int(input("Ingrese año: "))
                resultados = above_year_average(year)

                if not resultados:
                    print("No hay países en el resultado.")
                    continue

                print(f"Se encontraron {len(resultados)} países (ISO3):")
                for i, iso in enumerate(resultados, 1):
                    n = tree.search_by_iso(root, iso)
                    if n:
                        print(f"{i}. {iso} - {n.country} (media={n.mean:.2f})")
                    else:
                        print(f"{i}. {iso}")

                # Permite ver detalles de un país
                elegir = input("¿Desea seleccionar uno para ver detalles? (s/n): ").strip().lower()
                if elegir == "s":
                    idx = int(input("Número del país: "))
                    if 1 <= idx <= len(resultados):
                        iso = resultados[idx - 1]
                        node = tree.search_by_iso(root, iso)
                        if node:
                            print("Nivel:", tree.get_level(root, node, level=0))
                            print("Factor balance:", tree.get_balance(node))
                            print("Padre:", node.parent.iso3 if node.parent else None)
                            g = tree.get_grandparent(node)
                            print("Abuelo:", g.iso3 if g else None)
                            u = tree.get_uncle(node)
                            print("Tío:", u.iso3 if u else None)
            except ValueError:
                print("Año inválido.")

        # 6. Consulta: países en un año < promedio global de todos los años
        elif opcion == "6":
            try:
                year = int(input("Ingrese año: "))
                resultados = below_global_average(year)

                if not resultados:
                    print("No hay países en el resultado.")
                    continue

                print(f"Se encontraron {len(resultados)} países (ISO3):")
                for i, iso in enumerate(resultados, 1):
                    n = tree.search_by_iso(root, iso)
                    if n:
                        print(f"{i}. {iso} - {n.country} (media={n.mean:.2f})")
                    else:
                        print(f"{i}. {iso}")

                # Permite ver detalles de un país
                elegir = input("¿Desea seleccionar uno para ver detalles? (s/n): ").strip().lower()
                if elegir == "s":
                    idx = int(input("Número del país: "))
                    if 1 <= idx <= len(resultados):
                        iso = resultados[idx - 1]
                        node = tree.search_by_iso(root, iso)
                        if node:
                            print("Nivel:", tree.get_level(root, node, level=0))
                            print("Factor balance:", tree.get_balance(node))
                            print("Padre:", node.parent.iso3 if node.parent else None)
                            g = tree.get_grandparent(node)
                            print("Abuelo:", g.iso3 if g else None)
                            u = tree.get_uncle(node)
                            print("Tío:", u.iso3 if u else None)
            except ValueError:
                print("Año inválido.")

        # 7. Consulta: países con media >= valor dado
        elif opcion == "7":
            try:
                th = float(input("Ingrese valor mínimo de media: "))
                resultados = above_mean(th)

                if not resultados:
                    print("No hay países en el resultado.")
                    continue

                print(f"Se encontraron {len(resultados)} países (ISO3):")
                for i, iso in enumerate(resultados, 1):
                    n = tree.search_by_iso(root, iso)
                    if n:
                        print(f"{i}. {iso} - {n.country} (media={n.mean:.2f})")
                    else:
                        print(f"{i}. {iso}")

                # Permite ver detalles de un país
                elegir = input("¿Desea seleccionar uno para ver detalles? (s/n): ").strip().lower()
                if elegir == "s":
                    idx = int(input("Número del país: "))
                    if 1 <= idx <= len(resultados):
                        iso = resultados[idx - 1]
                        node = tree.search_by_iso(root, iso)
                        if node:
                            print("Nivel:", tree.get_level(root, node, level=0))
                            print("Factor balance:", tree.get_balance(node))
                            print("Padre:", node.parent.iso3 if node.parent else None)
                            g = tree.get_grandparent(node)
                            print("Abuelo:", g.iso3 if g else None)
                            u = tree.get_uncle(node)
                            print("Tío:", u.iso3 if u else None)
            except ValueError:
                print("Valor inválido.")

        # 8. Mostrar árbol gráfico en PNG
        elif opcion == "8":
            draw_tree(root, "avl_tree")
            print("Árbol exportado a avl_tree.png")


        # 0. Salir del programa
        elif opcion == "0":
            break

        else:
            print("Opción inválida.")
