from collections import deque

class AVLTree:

    # -------------------------------
    # Utilidades básicas
    # -------------------------------
    def get_height(self, root):
        return 0 if not root else root.height

    def get_balance(self, root):
        return 0 if not root else self.get_height(root.left) - self.get_height(root.right)

    # -------------------------------
    # Rotaciones
    # -------------------------------
    def right_rotate(self, y):
        if not y or not y.left:
            return y
        x = y.left
        T2 = x.right

        # rotación
        x.right = y
        y.left = T2

        # actualizar padres
        prev_parent = y.parent
        x.parent = prev_parent
        y.parent = x
        if T2:
            T2.parent = y

        # reconectar con el padre previo
        if prev_parent:
            if prev_parent.left is y:
                prev_parent.left = x
            else:
                prev_parent.right = x

        # actualizar alturas
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        if not x or not x.right:
            return x
        y = x.right
        T2 = y.left

        # rotación
        y.left = x
        x.right = T2

        # actualizar padres
        prev_parent = x.parent
        y.parent = prev_parent
        x.parent = y
        if T2:
            T2.parent = x

        # reconectar con el padre previo
        if prev_parent:
            if prev_parent.left is x:
                prev_parent.left = y
            else:
                prev_parent.right = y

        # actualizar alturas
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    # -------------------------------
    # Inserción
    # -------------------------------
    def insert(self, root, node):
        if not root:
            return node

        # clave compuesta (mean, iso3) para evitar problemas con duplicados
        if (node.mean, node.iso3) < (root.mean, root.iso3):
            root.left = self.insert(root.left, node)
            if root.left:
                root.left.parent = root
        else:
            root.right = self.insert(root.right, node)
            if root.right:
                root.right.parent = root

        # actualizar altura
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # re-balancear
        if balance > 1 and (node.mean, node.iso3) < (root.left.mean, root.left.iso3):
            return self.right_rotate(root)
        if balance < -1 and (node.mean, node.iso3) > (root.right.mean, root.right.iso3):
            return self.left_rotate(root)
        if balance > 1 and (node.mean, node.iso3) > (root.left.mean, root.left.iso3):
            root.left = self.left_rotate(root.left)
            if root.left:
                root.left.parent = root
            return self.right_rotate(root)
        if balance < -1 and (node.mean, node.iso3) < (root.right.mean, root.right.iso3):
            root.right = self.right_rotate(root.right)
            if root.right:
                root.right.parent = root
            return self.left_rotate(root)

        return root

    # -------------------------------
    # Recorridos y búsquedas
    # -------------------------------
    def level_order(self, root):
        """Recorrido por niveles con raíz en nivel 0"""
        if not root:
            return []
        result = []
        queue = deque([(root, 0)])
        while queue:
            node, level = queue.popleft()
            result.append((node.iso3, node.mean, level))
            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))
        return result

    def search_all(self, root, mean, tol=1e-9):
        """Devuelve todos los nodos cuya media coincide exactamente (tol por flotantes)."""
        if not root:
            return []
        res = []
        if abs(root.mean - mean) < tol:
            res.append(root)
        res.extend(self.search_all(root.left, mean, tol))
        res.extend(self.search_all(root.right, mean, tol))
        return res

    def search_by_iso(self, root, iso3):
        """Busca un nodo por ISO3 recorriendo todo el árbol."""
        if not root:
            return None
        if root.iso3 == iso3:
            return root
        left = self.search_by_iso(root.left, iso3)
        if left:
            return left
        return self.search_by_iso(root.right, iso3)

    def get_all_nodes(self, root):
        """Recorrido inorder (para depuración)."""
        if not root:
            return []
        res = []
        res.extend(self.get_all_nodes(root.left))
        res.append(root)
        res.extend(self.get_all_nodes(root.right))
        return res

    # -------------------------------
    # Eliminación
    # -------------------------------
    def get_min_value_node(self, node):
        current = node
        while current and current.left:
            current = current.left
        return current

    def delete_one_by_key(self, root, key):
        """Elimina un nodo por clave exacta (mean, iso3)."""
        if not root:
            return None

        if key < (root.mean, root.iso3):
            root.left = self.delete_one_by_key(root.left, key)
            if root.left:
                root.left.parent = root
        elif key > (root.mean, root.iso3):
            root.right = self.delete_one_by_key(root.right, key)
            if root.right:
                root.right.parent = root
        else:
            # nodo encontrado
            if not root.left:
                temp = root.right
                if temp:
                    temp.parent = root.parent
                return temp
            elif not root.right:
                temp = root.left
                if temp:
                    temp.parent = root.parent
                return temp
            else:
                temp = self.get_min_value_node(root.right)
                root.country, root.iso3, root.values, root.mean = (
                    temp.country, temp.iso3, temp.values, temp.mean
                )
                root.right = self.delete_one_by_key(root.right, (temp.mean, temp.iso3))
                if root.right:
                    root.right.parent = root

        # actualizar altura y balancear
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            if root.left:
                root.left.parent = root
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            if root.right:
                root.right.parent = root
            return self.left_rotate(root)

        return root

    def delete_all(self, root, mean, tol=1e-9):
        """Elimina TODOS los nodos con la media exacta."""
        nodes = self.search_all(root, mean, tol)
        eliminados = []
        for n in nodes:
            key = (n.mean, n.iso3)
            root = self.delete_one_by_key(root, key)
            eliminados.append(n.iso3)
            if root:
                root.parent = None
        return root, eliminados

    # -------------------------------
    # Operaciones de nivel familiar
    # -------------------------------
    def get_level(self, root, node, level=0):
        if not root:
            return -1
        if root == node:
            return level
        down = self.get_level(root.left, node, level + 1)
        if down != -1:
            return down
        return self.get_level(root.right, node, level + 1)

    def get_parent(self, node):
        return node.parent if node else None

    def get_grandparent(self, node):
        return node.parent.parent if node and node.parent else None

    def get_uncle(self, node):
        g = self.get_grandparent(node)
        if not g:
            return None
        if g.left == node.parent:
            return g.right
        return g.left
