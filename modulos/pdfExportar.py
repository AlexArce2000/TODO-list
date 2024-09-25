from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from modulos.tareasManager import load_tasks

def export_to_pdf():
    tasks = load_tasks()
    if not tasks:
        return "No hay tareas para exportar."

    pdf_file_path = "json-list/todo_list.pdf"  
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    # Establecer fuentes para los encabezados
    c.setFont("Helvetica-Bold", 14)  # Negrita para encabezados
    c.drawString(100, height - 50, "Lista de Tareas")
    c.drawString(100, height - 70, "ID")
    c.drawString(150, height - 70, "Tarea")
    c.drawString(300, height - 70, "Estado")

    # Dibuja línea horizontal para encabezados
    c.line(100, height - 75, 500, height - 75)

    # Regresar a la fuente normal para el contenido
    c.setFont("Times-Roman", 12)  # Fuente normal para las tareas

    y = height - 100
    for task in tasks:
        status = "Completada" if task["completed"] else "Pendiente"
        
        # Dibuja cuadro para cada tarea
        if task["completed"]:
            c.setFillColor(colors.green)
        else:
            c.setFillColor(colors.red)

        c.rect(95, y - 12, 410, 25, stroke=1, fill=1)  # Rectángulo alrededor de la tarea

        # Cambiar color del texto según el estado
        c.setFillColor(colors.white)  # Texto en blanco
        c.drawString(100, y, str(task['id']))  # ID
        c.drawString(150, y, task['task'])     # Tarea
        c.drawString(300, y, status)           # Estado
        
        y -= 30  # Espacio entre líneas (ajustado para el alto del cuadro)

    c.save()
    return f"Lista de tareas exportada a {pdf_file_path}"
