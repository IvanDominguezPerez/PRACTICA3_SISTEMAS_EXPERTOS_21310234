import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

# Clase que representa el sistema Akinator
class Akinator:
    # Constructor de la clase, carga el archivo de conocimiento si existe, o crea uno nuevo
    def __init__(self, knowledge_file="akinator_knowledge.json"):
        self.knowledge_file = knowledge_file
        try:
            # Intenta abrir el archivo de conocimiento existente
            with open(knowledge_file, "r") as file:
                self.knowledge = json.load(file)
        except FileNotFoundError:
            # Si no encuentra el archivo, inicia un conocimiento base con una pregunta inicial
            self.knowledge = {"question": "¿Es un piloto de la parrilla actual?", "yes": {}, "no": {}}

    # Método para guardar el conocimiento actualizado en el archivo
    def save_knowledge(self):
        with open(self.knowledge_file, "w") as file:
            json.dump(self.knowledge, file, indent=4)

    # Método principal para jugar
    def play(self):
        self.current_node = self.knowledge  # Nodo actual del árbol de conocimiento
        self.parent_node = None  # Nodo padre, para recordar la posición anterior
        self.last_answer = ""  # Última respuesta dada (sí o no)

        # Configurar la interfaz gráfica
        self.root = tk.Tk()
        self.root.title("Akinator")

        # Cargar la imagen proporcionada
        self.image = Image.open("imagen_akinator.jpg")  # Asegúrate de proporcionar la ruta correcta de la imagen
        self.image = self.image.resize((200, 200))
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.pack()

        # Configurar el label de pregunta y los botones
        self.question_label = tk.Label(self.root, text=self.current_node["question"], font=("Arial", 14))
        self.question_label.pack(pady=10)

        self.yes_button = tk.Button(self.root, text="Sí", command=lambda: self.next_step("sí"))
        self.yes_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.no_button = tk.Button(self.root, text="No", command=lambda: self.next_step("no"))
        self.no_button.pack(side=tk.RIGHT, padx=20, pady=10)

        self.root.mainloop()

    # Método para manejar la lógica del siguiente paso basado en la respuesta
    def next_step(self, answer):
        if "question" in self.current_node and self.current_node:
            if answer == "sí":
                self.parent_node = self.current_node
                self.last_answer = "yes"
                self.current_node = self.current_node.get("yes", {})
            elif answer == "no":
                self.parent_node = self.current_node
                self.last_answer = "no"
                self.current_node = self.current_node.get("no", {})

            if "question" in self.current_node:
                self.question_label.config(text=self.current_node["question"])
            elif "name" in self.current_node:
                self.guess_character()
            else:
                self.learn()
        else:
            self.learn()

    # Método para adivinar el personaje y preguntar si es correcto
    def guess_character(self):
        guess = self.current_node["name"]
        answer = messagebox.askyesno("Akinator", f"¿Tu personaje es {guess}?")
        if answer:
            messagebox.showinfo("Akinator", "¡Genial! ¡Lo adiviné!")
            self.root.destroy()
        else:
            self.learn()

    # Método para aprender un nuevo personaje cuando no se adivina correctamente
    def learn(self):
        new_character = simpledialog.askstring("Aprender", "¡Me rindo! ¿Quién era tu personaje?:")
        new_question = simpledialog.askstring("Aprender", f"Proporciona una pregunta que distinga a {new_character} de otros:")
        correct_answer = messagebox.askyesno("Aprender", f"¿Cuál sería la respuesta a esta pregunta para {new_character}? (sí/no)")

        new_node = {
            "question": new_question,
            "yes": {"name": new_character} if correct_answer else {},
            "no": {"name": new_character} if not correct_answer else {}
        }

        if self.last_answer == "yes":
            self.parent_node["yes"] = new_node
        elif self.last_answer == "no":
            self.parent_node["no"] = new_node

        self.save_knowledge()
        messagebox.showinfo("Akinator", "Gracias, ¡he aprendido algo nuevo!")
        self.root.destroy()

# Función principal para iniciar el juego
def main():
    akinator = Akinator()  # Crea una instancia del juego Akinator
    play_again = True  # Variable para controlar si el usuario quiere jugar nuevamente
    while play_again:
        akinator.play()  # Inicia el juego
        play_again = messagebox.askyesno("Akinator", "¿Quieres jugar de nuevo?")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
