#!/bin/bash
carpeta="/home/alex/pdfs"  # Ruta de la carpeta donde se realizará el grep

# Ruta de la carpeta "resultados"
carpeta_resultados="/home/alex/resultados"

# Comprobar si la carpeta existe
if [ ! -d "$carpeta_resultados" ]; then
    # Si no existe, crear la carpeta
    mkdir "$carpeta_resultados"
fi

# Función para generar un nuevo nombre para el archivo
function generar_nombre_archivo() {
    archivo_base="resultados$1.csv"
    contador=1
    nuevo_nombre="$archivo_base"
    while [ -e "$carpeta_resultados/$nuevo_nombre" ]; do
        nuevo_nombre="${archivo_base%.*}_$contador.csv"
        contador=$((contador+1))
    done
    echo "$nuevo_nombre"
}

# Generar el nombre del archivo para el primer texto
nombre_archivo_1=$(generar_nombre_archivo "$1")

# Ejecutar el primer comando grep con el primer texto ingresado como argumento
resultado_primer_grep=$(grep -r -i -n --include=\*.txt "$1" ./)
echo "$resultado_primer_grep" | tee >(cat) > "$nombre_archivo_1"

# Mover el archivo CSV del primer comando a la carpeta "resultados"
mv "$nombre_archivo_1" "$carpeta_resultados/"

# Verificar si se proporcionó el segundo parámetro
if [ "$2" ]; then
    # Generar el nombre del archivo para el segundo texto
    nombre_archivo_2=$(generar_nombre_archivo "$2")

    # Ejecutar el segundo comando grep con el resultado del primer comando grep y el segundo texto ingresado como argumento
    resultado_segundo_grep=$(echo "$resultado_primer_grep" | grep -i "$2")
    echo "$resultado_segundo_grep" | tee >(cat) > "$nombre_archivo_2"

    # Mover el archivo CSV del segundo comando a la carpeta "resultados"
    mv "$nombre_archivo_2" "$carpeta_resultados/"
fi

# Indicar que la ejecución ha finalizado
echo "Ejecución completada"

# Finalizar el script
exit 0