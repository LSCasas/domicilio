from flask import Flask, jsonify, request, render_template
import psycopg2

app = Flask(__name__)

DATABASE_URL = "postgres://postgres@localhost:5432/domicilio"

@app.route('/', methods=['GET', 'POST'])
def index():
    cp = None
    colonias = []
    municipio = ""
    ciudad = ""
    estado = ""
    mensaje = ""
    persona = ""
    calle = ""
    no_ext = ""
    no_int = ""

    # Buscar persona por ID
    if request.method == 'POST' and 'buscar_persona' in request.form:
        id_persona = request.form.get('id_persona')
        if id_persona:
            try:
                conn = psycopg2.connect(DATABASE_URL)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.nombre, p.calle, p.ne, p.ni, p.cp, 
                           c.descripcion AS colonia, m.descripcion AS municipio, 
                           ci.descripcion AS ciudad, e.descripcion AS estado
                    FROM personas p
                    LEFT JOIN colonias c ON p.id_colonia = c.id_colonia
                    LEFT JOIN municipios m ON c.id_municipio = m.id_municipio
                    LEFT JOIN ciudades ci ON m.id_municipio = ci.id_municipio
                    LEFT JOIN estados e ON ci.id_estado = e.id_estado
                    WHERE p.id_persona = %s
                """, (id_persona,))

                persona_data = cursor.fetchone()
                if persona_data:
                    persona, calle, no_ext, no_int, cp, colonia, municipio, ciudad, estado = persona_data
                else:
                    mensaje = "No se encontró persona con ese ID."
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error al obtener persona: {e}")
                mensaje = "Error al buscar la persona."

    # Buscar ubicación por C.P.
    if request.method == 'POST' and 'buscar_ubicacion' in request.form:
        cp = request.form.get('cp')
        if cp and len(cp) == 5:  
            try:
                conn = psycopg2.connect(DATABASE_URL)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.descripcion AS colonia, m.descripcion AS municipio, 
                           ci.descripcion AS ciudad, e.descripcion AS estado
                    FROM cp cp
                    JOIN colonias c ON cp.id_colonia = c.id_colonia
                    JOIN municipios m ON c.id_municipio = m.id_municipio AND c.id_estado = m.id_estado
                    JOIN ciudades ci ON ci.id_municipio = m.id_municipio AND ci.id_estado = m.id_estado
                    JOIN estados e ON e.id_estado = m.id_estado
                    WHERE cp.cp = %s
                """, (cp,))

                resultados = cursor.fetchall()
                cursor.close()
                conn.close()

                if resultados:
                    colonias = list(set(row[0] for row in resultados))  # Evita duplicados
                    municipio = resultados[0][1]
                    ciudad = resultados[0][2]
                    estado = resultados[0][3]
                else:
                    mensaje = "No se encontró información para ese C.P."
            except Exception as e:
                print(f"Error al conectar con la base de datos: {e}")
                return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

 # Procesar el formulario de registro de persona
    if request.method == 'POST' and 'enviar_registro' in request.form:
        nombre = request.form.get('persona')
        calle = request.form.get('calle')
        no_ext = request.form.get('no_ext')
        no_int = request.form.get('no_int')
        colonia = request.form.get('colonia')
        cp = request.form.get('cp')

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            
            cursor.execute("""
                SELECT id_colonia FROM colonias WHERE descripcion = %s LIMIT 1
            """, (colonia,))
            id_colonia = cursor.fetchone()

            if id_colonia:
               
                cursor.execute("""
                    INSERT INTO personas (nombre, calle, ne, ni, cp, id_colonia)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nombre, calle, no_ext, no_int, cp, id_colonia[0]))
                conn.commit()
                mensaje = "Persona registrada exitosamente."
                
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error al insertar datos: {e}")
            mensaje = "Error al registrar la persona."

    return render_template('index.html', cp=cp, colonias=colonias, municipio=municipio, ciudad=ciudad, estado=estado, persona=persona, calle=calle, no_ext=no_ext, no_int=no_int, mensaje=mensaje)
if __name__ == '__main__':
    app.run(debug=True)
