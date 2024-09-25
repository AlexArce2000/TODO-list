import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from modulos.tareasManager import add_task, delete_task, complete_task, update_task_list
from modulos.pdfExportar import export_to_pdf

# Función para deseleccionar la tarea
def deselect_task(event, task_listbox, delete_button, complete_button):
    global clicked_button
    if not clicked_button and task_listbox.winfo_containing(event.x_root, event.y_root) != task_listbox:
        if not (event.widget == delete_button or event.widget == complete_button):
            task_listbox.selection_clear(0, tk.END)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestor de Tareas")
root.geometry("400x400")
root.resizable(False, False)
root.configure(bg="lightblue")

# Cargar el ícono
icon_path = "image/icon-app.png"
icon_img = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_img)
root.iconphoto(False, icon_photo)

# Cargar la imagen de fondo
bg_image_path = "image/fondo.jpg"
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((400, 400))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Crear widgets
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

# Botón con ícono para añadir tarea
icon_add_path = "image/add.png"
img_add = Image.open(icon_add_path).resize((20, 20))
icon_add = ImageTk.PhotoImage(img_add)

add_button = tk.Button(root, text="Añadir tarea", command=lambda: add_task(task_entry, task_listbox), image=icon_add, compound=tk.LEFT)
add_button.pack(pady=5)

task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.pack(pady=10)

# Botones con íconos
icon_delete_path = "image/delete.png"
icon_complete_path = "image/complete.png"
icon_pdf_path = "image/pdf.png"

img_delete = Image.open(icon_delete_path).resize((20, 20))
icon_delete = ImageTk.PhotoImage(img_delete)

img_complete = Image.open(icon_complete_path).resize((20, 20))
icon_complete = ImageTk.PhotoImage(img_complete)

img_pdf = Image.open(icon_pdf_path).resize((20, 20))
icon_pdf = ImageTk.PhotoImage(img_pdf)

complete_button = tk.Button(root, text="Marcar como completada", command=lambda: complete_task(task_listbox), image=icon_complete, compound=tk.LEFT)
complete_button.pack(pady=5)

delete_button = tk.Button(root, text="Eliminar tarea", command=lambda: delete_task(task_listbox), image=icon_delete, compound=tk.LEFT)
delete_button.pack(pady=5)

export_button = tk.Button(root, text="Exportar a PDF", command=export_to_pdf, image=icon_pdf, compound=tk.LEFT)
export_button.pack(pady=5)

# Actualizar la lista de tareas al inicio
update_task_list(task_listbox)

# Conectar la tecla Enter para añadir tareas
task_entry.bind("<Return>", lambda event: add_task(task_entry, task_listbox))

# Función para manejar el clic en el botón "Marcar como completada"
clicked_button = False
root.bind("<Button-1>", lambda event: deselect_task(event, task_listbox, delete_button, complete_button))

# Ejecutar la aplicación
root.mainloop()
