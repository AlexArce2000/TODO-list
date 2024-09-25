from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from tkinter import messagebox
import os
import json

TODO_FILE = "json-list/todo_list.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as file:
        return json.load(file)

# Función para exportar tareas a PDF
def export_to_pdf():
    tasks = load_tasks()
    if not tasks:
        messagebox.showwarning("Advertencia", "No hay tareas para exportar.")
        return

    pdf_file_path = "json-list/todo_list.pdf"  
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    # Encabezados
    c.setFont("Helvetica-Bold", 14)  # Negrita
    c.drawString(100, height - 50, "Lista de Tareas")
    c.drawString(100, height - 70, "ID")
    c.drawString(150, height - 70, "Tarea")
    c.drawString(300, height - 70, "Estado")

    # Línea horizontal
    c.line(100, height - 75, 500, height - 75)

    # Tareas
    c.setFont("Times-Roman", 12)  # Fuente normal
    y = height - 100
    for task in tasks:
        status = "Completada" if task["completed"] else "Pendiente"
        if task["completed"]:
            c.setFillColor(colors.green)
        else:
            c.setFillColor(colors.red)
        c.rect(95, y - 12, 410, 25, stroke=1, fill=1)  # Cuadro
        c.setFillColor(colors.white)  # Texto en blanco
        c.drawString(100, y, str(task['id']))
        c.drawString(150, y, task['task'])
        c.drawString(300, y, status)
        y -= 30

    c.save()
    messagebox.showinfo("Éxito", f"Lista de tareas exportada a {pdf_file_path}")
