from flask import Flask, request, jsonify

# Define os parametros utilizadas na API
app = Flask(__name__)
tasks = []  # Lista para armazenar as tarefas
task_id_control = 1  # Controlador de IDs para garantir unicidade

# Algoritimo para uma rota basica '/' para teste
@app.route("/", methods=["GET"])
def hello():
    return "Hello, World!"

# Algoritimo para rota '/tasks' sendo um algoritimo simples de gravação de cabeçalho para depois ser consultado por metodo GET
@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control
    data = request.get_json()  # Pega os dados enviados no corpo da requisição
    new_task = {
        "id": task_id_control,
        "title": data.get("title"),  # Obtém o título enviado
        "description": data.get("description", ""),  # Descrição opcional
        "completed": False  # Define que a tarefa começa como incompleta
    }
    tasks.append(new_task)  # Adiciona a nova tarefa à lista
    task_id_control += 1  # Incrementa o ID para a próxima tarefa
    return jsonify({"message": "Tarefa criada com sucesso!", "task": new_task}), 201

# Algoritmo simples para consulta simples para consulta de total de "tasks" gravadas na API
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks, "total": len(tasks)})

# Algoritimo simples para consulta do dado gravado dado um "ID" de valor inteiro para consulta
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    # Procura a tarefa pelo ID
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    return jsonify(task)

# Algoritimo simples para atualizar dados de uma tarefa já gravada utilizando o "ID" da tarefa a ser editada
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    data = request.get_json()
    # Atualiza os campos da tarefa com os dados enviados
    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["completed"] = data.get("completed", task["completed"])
    return jsonify({"message": "Tarefa atualizada com sucesso!", "task": task})

# Algoritimo simples para deletar uma tarefa pela "ID"
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tarefa deletada com sucesso!"})

# Essa parte do código deverá estar no final do projeto para realizar o algoritimo acima
if __name__ == "__main__":
    app.run(debug=True)