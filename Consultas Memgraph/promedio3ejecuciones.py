import subprocess

def execute_and_calculate_averages(input_file, output_file):
    try:
        # Leer las consultas desde el archivo
        with open(input_file, 'r') as file:
            cypher_queries = file.readlines()

        # Inicializar arreglos para guardar los tiempos
        times_first_execution = []
        times_second_execution = []
        times_third_execution = []

        # Ejecutar todas las consultas una vez (sin almacenar nada)
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

        # Segunda ejecución: Guardar tiempos en el primer arreglo
        for query in cypher_queries:
            query = query.strip()
            if query:
                times_first_execution.append(execute_query_and_get_time(query))

        # Tercera ejecución: Guardar tiempos en el segundo arreglo
        for query in cypher_queries:
            query = query.strip()
            if query:
                times_second_execution.append(execute_query_and_get_time(query))

        # Cuarta ejecución: Guardar tiempos en el tercer arreglo
        for query in cypher_queries:
            query = query.strip()
            if query:
                times_third_execution.append(execute_query_and_get_time(query))

        # Calcular promedios y escribir en el archivo de salida
        with open(output_file, 'w') as out_file:
            for t1, t2, t3 in zip(times_first_execution, times_second_execution, times_third_execution):
                if None not in (t1, t2, t3):  # Verificar que no haya errores
                    avg_time = (t1 + t2 + t3) / 3
                    out_file.write(f"{avg_time}\n")
                else:
                    out_file.write("ERROR\n")  # Escribir error si alguna ejecución falló

    except FileNotFoundError:
        print(f"Error: El archivo {input_file} no existe.")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")


def execute_query_and_get_time(query):
    """
    Ejecuta una consulta en `mgconsole` y extrae el tiempo de ejecución.
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
    input_file = "consultas328enero"  # Archivo de entrada con las consultas
    output_file = "promedios_tiempos.txt"  # Archivo de salida con los promedios
    execute_and_calculate_averages(input_file, output_file)

