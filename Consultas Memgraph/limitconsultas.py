import subprocess

def execute_cypher_queries_one_by_one(file_path):
    try:
        with open(file_path, 'r') as file:
            cypher_queries = file.readlines()

        for query in cypher_queries:
            query = query.strip()
            if query:
                print(f"Ejecutando consulta: {query}")
                
                # List to store the times of the three executions
                execution_times = []

                # Run the query 3 times and collect the best time
                for _ in range(3):
                    process = subprocess.Popen(
                        ['mgconsole'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    stdout, stderr = process.communicate(input=query + '\n')

                    if stderr:
                        print("Errores:", stderr)
                    
                    # Extracting time from stdout
                    x = stdout.split("ms")
                    y = []
                    for l in x:
                        y.append(l.split(" "))
                    total_time = 0
                    for i, j in enumerate(y):
                        if j[-2] != '':
                            total_time += float(j[-2])
                    
                    # Convert time to seconds and add to the list
                    execution_times.append(total_time / 1000)

                # Get the best (minimum) time from the 3 executions
                best_time = min(execution_times)
                print(f"Mejor tiempo: {best_time} segundos")
                
                # Fourth execution without PROFILE and print the full output
                query_without_profile = query.replace("profile", "")  # Remove PROFILE part
                print("Ejecutando la consulta sin PROFILE para obtener el resultado completo:")
                process = subprocess.Popen(
                    ['mgconsole'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(input=query_without_profile + '\n')

                if stderr:
                    print("Errores:", stderr)

                # Print the full output of the query without processing it
                print("Resultado completo de la consulta:")
                print(stdout)

                print("=" * 50)
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no existe.")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

if __name__ == "__main__":
    file_path = "consultastimebd03"
    execute_cypher_queries_one_by_one(file_path)

