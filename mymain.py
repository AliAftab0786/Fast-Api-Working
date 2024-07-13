from fastapi import FastAPI
import mysql.connector
# import json

app = FastAPI()

# MySQL Configuration
mysql_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'fastapidatabase'
}
@app.get("/")
async def getalltasks():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # Fetch data from MySQL
        cursor.execute("SELECT id, name, lastdate FROM myinfotable")
        tasks = cursor.fetchall()

        # Check if tasks exist
        if not tasks:
            return {"error": "No tasks found"}

        # Convert data to JSON format
        tasks_json = []
        for task in tasks:
            task_json = {"id": task[0], "name": str(task[1]), "lastdate": str(task[2])}
            tasks_json.append(task_json)

        # Close cursor and connection
        cursor.close()
        connection.close()

        return tasks_json

    except mysql.connector.Error as error:
        return {"error": f"Failed to fetch tasks from MySQL: {error}"}

    
@app.get("/gettask/{task_id}")
async def get_task(task_id: int):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # Fetch data from MySQL for the specific task_id
        cursor.execute("SELECT id, name, lastdate FROM myinfotable WHERE id=%s", (task_id,))
        task = cursor.fetchone()

        # Check if task exists
        if not task:
            return {"error": "Task not found"}

        # Convert data to JSON format
        task_json = {"id": task[0], "name": str(task[1]), "lastdate": str(task[2])}

        # Close cursor and connection
        cursor.close()
        connection.close()

        return task_json

    except mysql.connector.Error as error:
        return {"error": f"Failed to fetch task from MySQL: {error}"}
    
@app.get("/settask/{parameters}")
async def set_task(parameters: str):
    try:
        # Parse parameters
        params = parameters.split(',')
        if len(params) != 3:
            return {"error": "Invalid parameters format. Use id,name,lastdate"}

        task_id, task_name, task_lastdate = params

        # Connect to MySQL
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # Check if the task_id already exists in the database
        cursor.execute("SELECT id FROM myinfotable WHERE id = %s", (int(task_id),))
        existing_task = cursor.fetchone()

        if existing_task:
            cursor.close()
            connection.close()
            return {"message": f"Task with ID {task_id} is already registered"}

        # Insert data into MySQL
        cursor.execute("INSERT INTO myinfotable (id, name, lastdate) VALUES (%s, %s, %s)", (int(task_id), task_name, task_lastdate))
        connection.commit()

        # Close cursor and connection
        cursor.close()
        connection.close()

        return {"message": "Task inserted successfully"}

    except mysql.connector.Error as error:
        return {"error": f"Failed to insert task into MySQL: {error}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mymain:app", host="127.0.0.1", port=8000, reload=True)