from flask import Flask, render_template
import nbformat
import os

app = Flask(__name__)

def extraer_resultados(notebook_file):
    """
    Extrae las gráficas y el árbol de decisión de un archivo notebook.
    """
    with open(notebook_file, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)

    graficas = []
    arbol_svg = None

    # Procesar las celdas del notebook
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'code' and 'outputs' in cell:
            for output in cell['outputs']:
                # Capturar gráficos en formato PNG
                if output['output_type'] == 'display_data' and 'image/png' in output['data']:
                    img_base64 = output['data']['image/png']
                    graficas.append(img_base64)

                # Capturar árbol de decisión en formato SVG
                if output['output_type'] == 'display_data' and 'image/svg+xml' in output['data']:
                    arbol_svg = output['data']['image/svg+xml']

    return graficas, arbol_svg

@app.route('/')
def mostrar_resultados():
    # Procesar el primer notebook (ArbolesZ.ipynb)
    graficas_arboles, arbol_svg = extraer_resultados('ArbolesZ.ipynb')

    # Verificar si el archivo SVG del árbol existe en static/
    if not arbol_svg and os.path.exists('static/android_malware.svg'):
        arbol_svg = 'static/android_malware.svg'  # Usar archivo preexistente si no se extrae del notebook

    # Procesar el segundo notebook (regresion-forest.ipynb)
    graficas_regresion, _ = extraer_resultados('Random-ForestV2.ipynb')

    # Combinar las gráficas de ambos notebooks
    todas_las_graficas = graficas_arboles + graficas_regresion

    # Renderizar la plantilla con todas las gráficas y el árbol
    return render_template('resultados.html', graficas=todas_las_graficas, arbol_svg=arbol_svg)


if __name__ == '__main__':
    app.run(debug=True)

