import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Cargar el inventario desde Excel
archivo = "inventario_ferreteria.xlsx"
df = pd.read_excel(archivo)
IVA = 0.16  # 16% de IVA
total_general = 0  # Variable global para acumular el total

def calcular_total():
    global total_general
    try:
        producto_id = int(combo_productos.get().split(" - ")[0])
        cantidad = int(entry_cantidad.get())
        producto = df[df["ID"] == producto_id]
        
        if producto.empty:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
        
        stock_actual = producto.iloc[0]["Cantidad"]
        if cantidad > stock_actual:
            messagebox.showwarning("Stock insuficiente", "No hay suficiente stock disponible.")
            return
        
        precio = producto.iloc[0]["Precio"]
        subtotal = cantidad * precio
        total_iva = subtotal * (1 + IVA)
        total_general += total_iva
        
        label_total.config(text=f"Total con IVA: ${total_iva:.2f}")
        label_total_general.config(text=f"Total acumulado: ${total_general:.2f}")
        
        # Actualizar el stock
        df.loc[df["ID"] == producto_id, "Cantidad"] -= cantidad
        df.to_excel(archivo, index=False)
        
        if df.loc[df["ID"] == producto_id, "Cantidad"].values[0] == 0:
            messagebox.showinfo("Producto agotado", f"El producto '{producto.iloc[0]['Nombre']}' se ha agotado.")
    except ValueError:
        messagebox.showerror("Error", "Ingrese una cantidad válida.")

# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Inventario")

# Dropdown para seleccionar producto
ttk.Label(root, text="Seleccione un producto:").pack()
combo_productos = ttk.Combobox(root, values=[f"{row['ID']} - {row['Nombre']}" for _, row in df.iterrows()])
combo_productos.pack()

# Entrada para cantidad
ttk.Label(root, text="Ingrese cantidad:").pack()
entry_cantidad = ttk.Entry(root)
entry_cantidad.pack()

# Botón para calcular total
btn_calcular = ttk.Button(root, text="Calcular Total", command=calcular_total)
btn_calcular.pack()

# Etiqueta para mostrar el total de la última compra
label_total = ttk.Label(root, text="Total con IVA: $0.00")
label_total.pack()

# Etiqueta para mostrar el total acumulado
label_total_general = ttk.Label(root, text="Total acumulado: $0.00")
label_total_general.pack()

# Ejecutar la interfaz
tk.mainloop()
