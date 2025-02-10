import subprocess

def execute_and_calculate_averages(input_file, output_file):
    try:
        # Leer las consultas desde el archivo
        with open(input_file, 'r') as file:
            cypher_queries = file.readlines()

        # Inicializar arreglos para guardar los tiempos
        times_execution_1 = []
        times_execution_2 = []
        times_execution_3 = []
        times_execution_4 = []
        times_execution_5 = []

        # Primera ejecución: No se guarda nada
        for query in cypher_queries:
            query = query.strip()
            if query:  # Ignorar líneas vacías
                process = subprocess.Popen(
                    ['mgconsole'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                process.communicate(input=query + '\n')  # Solo ejecutar

        # Segunda ejecución: Guardar tiempos
        for query in cypher_queries:
            query = query.strip()
            if query:
                times_execution_1.append(execute_query_and_get_time(query))

        # Tercera ejecución: Guardar tiempos
        for query in cypher_queries:
            query = query.strip()
            if query:
                times_execution_2.append(execute_query_and_get_time(query))

        # Cuarta ejecución: Guardar tiempos
        for query in cypher_queries:
            query = query.strip()
            if query:
                times_execution_3.append(execute_query_and_get_time(query))

        # Quinta ejecución: Guardar tiempos
        for query in cypher_queries:
            query = query.strip()
            if query:
                times_execution_4.append(execute_query_and_get_time(query))

        # Sexta ejecución: Guardar tiempos
        for query in cypher_queries:
            query = query.strip()
            if query:
                times_execution_5.append(execute_query_and_get_time(query))

        # Calcular promedios, eliminar el mayor y el menor de cada consulta
        with open(output_file, 'w') as out_file:
            for t1, t2, t3, t4, t5 in zip(times_execution_1, times_execution_2, times_execution_3, times_execution_4, times_execution_5):
                if None not in (t1, t2, t3, t4, t5):  # Verificar que no haya errores
                    times = [t1, t2, t3, t4, t5]
                    times.sort()  # Ordenar los tiempos para eliminar el mayor y el menor
                    avg_time = sum(times[1:4]) / 3  # Promedio de los 3 tiempos restantes
                    out_file.write(f"{avg_time}\n")
                else:
                    out_file.write("ERROR\n")  # Escribir error si alguna ejecución falló

    except FileNotFoundError:
        print(f"Error: El archivo {input_file} no existe.")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")


def execute_query_and_get_time(query):
    """
    Ejecuta una consulta en mgconsole y extrae el tiempo de ejecución.
    Retorna el tiempo en segundos o None si ocurre un error.
    """
    try:
        process = subprocess.Popen(
            ['mgconsole'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=query + '\n')

        if stderr:
            print(f"Errores en la consulta '{query}': {stderr}")

        # Extraer tiempo desde stdout
        x = stdout.split("ms")
        y = [l.split(" ") for l in x]
        total_time = 0
        for i, j in enumerate(y):
            if j[-2] != '':
                total_time += float(j[-2])

        return total_time / 1000  # Convertir a segundos
    except Exception as e:
        print(f"Error procesando la consulta '{query}': {e}")
        return None


if __name__ == "__main__":
    input_file = "Consultas10"  # Archivo de entrada con las consultas
    output_file = "promedios_tiemposversion2.txt"  # Archivo de salida con los promedios
    execute_and_calculate_averages(input_file, output_file)

