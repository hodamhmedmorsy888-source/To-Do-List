from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

tasks = []


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Task Manager</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #e9e7ff, #f5eaff);
            min-height: 100vh;
            margin: 0;
            padding: 50px 15px;
            color: #333;
        }

        .container {
            max-width: 550px;
            margin: auto;
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 10px 35px rgba(80, 60, 140, 0.12);
        }

        h1 {
            text-align: center;
            color: #5946a5;
            margin-bottom: 8px;
        }

        .subtitle {
            text-align: center;
            color: #999;
            margin-bottom: 30px;
        }

        h2 {
            color: #51428b;
            font-size: 20px;
            margin-top: 30px;
        }

        .add-form {
            display: flex;
            gap: 10px;
        }

        input[type=text] {
            flex: 1;
            min-width: 0;
            padding: 13px;
            border: 1px solid #ddd8f5;
            border-radius: 10px;
            outline: none;
            font-size: 14px;
        }

        input[type=text]:focus {
            border-color: #8069d5;
        }

        button {
            border: none;
            padding: 11px 14px;
            border-radius: 9px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
        }

        button:hover {
            opacity: 0.85;
            transform: translateY(-1px);
        }

        .add-btn {
            background: #7056c9;
            color: white;
        }

        ul {
            list-style: none;
            padding: 0;
        }

        li {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #f8f7ff;
            padding: 13px;
            margin-bottom: 12px;
            border-radius: 12px;
            border: 1px solid #eeebfa;
        }

        .task-name {
            flex: 1;
            overflow-wrap: anywhere;
        }

        .done {
            text-decoration: line-through;
            color: #aaa;
        }

        .task-form {
            display: inline;
        }

        .complete-btn {
            background: #dff5e7;
            color: #27834b;
        }

        .delete-btn {
            background: #ffe5e5;
            color: #d34c4c;
        }

        .empty {
            text-align: center;
            color: #aaa;
            padding: 25px;
            background: #faf9ff;
            border-radius: 12px;
        }

        @media (max-width: 480px) {
            .container {
                padding: 22px 16px;
            }

            li {
                flex-wrap: wrap;
            }
        }
    </style>
</head>

<body>

    <div class="container">

        <h1>My Task Manager</h1>
        <p class="subtitle">Organize your day, one task at a time ✨</p>

        <form action="/add" method="post" class="add-form">
            <input type="text" name="task"
                   placeholder="What do you need to do?" required>
            <button class="add-btn" type="submit">+ Add</button>
        </form>

        <h2>My Tasks 📝</h2>

        <ul>
            {% for task in tasks %}
            <li>
                <span class="task-name {{ 'done' if task.done else '' }}">
                    {{ task.name }}
                </span>

                <form action="/toggle/{{ task.id }}" method="post"
                      class="task-form">
                    <button class="complete-btn" type="submit">
                        {{ 'Undo' if task.done else 'Done' }}
                    </button>
                </form>

                <form action="/delete/{{ task.id }}" method="post"
                      class="task-form">
                    <button class="delete-btn" type="submit">
                        Delete
                    </button>
                </form>
            </li>
            {% else %}
            <p class="empty">No tasks yet. Add your first task! 🌸</p>
            {% endfor %}
        </ul>

    </div>

</body>
</html>
"""



@app.route("/")
def home():
    return render_template_string(HTML, tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    name = request.form.get("task", "").strip()

    if name:
        tasks.append({
            "id": max((t["id"] for t in tasks), default=0) + 1,
            "name": name,
            "done": False
        })

    return redirect("/")


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break

    return redirect("/")


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)