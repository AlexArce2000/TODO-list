import tkinter as tk
import re
from tkinter import messagebox
from PIL import Image, ImageTk
from modulos.tareasManager import add_task, load_tasks, complete_task, delete_task
from modulos.pdfExportar import export_to_pdf

# Función para añadir tarea
def add_task_wrapper():
    task_description = task_entry.get()
    if not task_description:
        messagebox.showwarning("Advertencia", "No puedes añadir una tarea vacía.")
        return
    
    if add_task(task_description):
        task_entry.delete(0, tk.END)  # Limpiar campo de texto
        update_task_list()

# Función para actualizar la lista de tareas
def update_task_list():
    task_listbox.delete(0, tk.END)  # Limpiar la lista actual
    tasks = load_tasks()
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        color = "green" if task["completed"] else "red"
        date = re.compile(r'(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2})')
        match = date.search(task['created_at'])
        display_text = f"{task['id']}. {task['task']} [{status}] {match.group(1)} {match.group(2)}"
        task_listbox.insert(tk.END, display_text)
        
        # Cambiar el color según el estado
        task_listbox.itemconfig(tk.END, {'fg': color})

# Función para marcar tarea como completada
def complete_task_wrapper():
    try:
        selected_task_index = task_listbox.curselection()[0]  # Selección en la lista
        task_id = selected_task_index + 1  # El ID es el índice + 1
        if complete_task(task_id):
            update_task_list()
    except IndexError:
        pass  # No mostrar advertencia aquí

# Función para eliminar tarea
def delete_task_wrapper():
    try:
        selected_task_index = task_listbox.curselection()[0]  # Selección en la lista
        task_id = selected_task_index + 1  # El ID es el índice + 1
        if delete_task(task_id):
            update_task_list()
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para eliminar.")
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para eliminar.")

# Función para exportar tareas a PDF
def export_tasks():
    result = export_to_pdf()
    messagebox.showinfo("Éxito", result)

# Configuración de la ventana principal
def setup_gui():
    global task_entry, task_listbox

    root = tk.Tk()
    root.title("Gestor de Tareas")
    root.geometry("400x400")
    root.resizable(False, False)  # Evitar que la ventana cambie de tamaño
    root.configure(bg="lightblue")

    # Cargar iconos (ajusta las rutas según sea necesario)
    icon_add_path = "image/add.png"
    icon_delete_path = "image/delete.png"
    icon_complete_path = "image/complete.png"
    icon_pdf_path = "image/pdf.png"  # Reemplaza con la ruta de tu ícono de PDF

    # Crear objetos PhotoImage
    img_add = Image.open(icon_add_path).resize((20, 20))
    icon_add = ImageTk.PhotoImage(img_add)

    img_delete = Image.open(icon_delete_path).resize((20, 20))
    icon_delete = ImageTk.PhotoImage(img_delete)

    img_complete = Image.open(icon_complete_path).resize((20, 20))
    icon_complete = ImageTk.PhotoImage(img_complete)

    img_pdf = Image.open(icon_pdf_path).resize((20, 20))
    icon_pdf = ImageTk.PhotoImage(img_pdf)
    # Cargar la imagen de fondo
    bg_image_path = "image/fondo.jpg"  # Reemplaza con la ruta de tu imagen
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((400, 400))  # Ajustar el tamaño de la imagen
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Crear un Label con la imagen de fondo
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Colocar el Label en toda la ventana
    
    # Campo de entrada para añadir tareas
    task_entry = tk.Entry(root, width=40)
    task_entry.pack(pady=10)

    # Asocia el evento de la tecla Enter con la función add_task
    task_entry.bind("<Return>", lambda event: add_task_wrapper())

    # Botón con ícono para añadir tarea
    add_button = tk.Button(root, text="Añadir tarea", command=add_task_wrapper, image=icon_add, compound=tk.LEFT)
    add_button.pack(pady=5)

    # Listbox para mostrar las tareas
    task_listbox = tk.Listbox(root, width=50, height=10)
    task_listbox.pack(pady=10)

    # Botón para marcar como completada
    complete_button = tk.Button(root, text="Marcar como completada", command=complete_task_wrapper, image=icon_complete, compound=tk.LEFT)
    complete_button.pack(pady=5)

    # Botón para eliminar tarea
    delete_button = tk.Button(root, text="Eliminar tarea", command=delete_task_wrapper, image=icon_delete, compound=tk.LEFT)
    delete_button.pack(pady=5)

    # Botón para exportar a PDF
    export_button = tk.Button(root, text="Exportar a PDF", command=export_tasks, image=icon_pdf, compound=tk.LEFT)
    export_button.pack(pady=5)

    update_task_list()  # Cargar tareas al inicio
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
