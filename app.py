from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "securecorp_super_secret_key" # Necesario para guardar el progreso

# Lista de todas las banderas en orden
FLAGS = [
    {"id": 1, "title": "Flag 01: Banner Grabbing", "flag": "CORP{b4nn3r_gr4bb1ng_1337}", "hint": "El servidor tiene un puerto inusual abierto (1337). Usa Netcat para conectarte a él."},
    {"id": 2, "title": "Flag 02: Código Fuente", "flag": "CORP{html_c0mm3nt_f0und}", "hint": "Revisa el código fuente de la página principal. Los desarrolladores olvidan cosas en los comentarios HTML."},
    {"id": 3, "title": "Flag 03: Rutas Ocultas", "flag": "CORP{r0b0ts_txt_3xp0s3d}", "hint": "¿Has revisado el archivo robots.txt? Ahí esconden las rutas en desarrollo."},
    {"id": 4, "title": "Flag 04: Esteganografía", "flag": "CORP{4ud10_st3g0_f0und}", "hint": "Analiza el espectrograma del archivo de audio .wav en la carpeta /resources."},
    {"id": 5, "title": "Flag 05: Metadatos", "flag": "CORP{pdf_m3t4d4t4_l34k}", "hint": "Extrae los metadatos del manual PDF con la herramienta Exiftool."},
    {"id": 6, "title": "Flag 06: SQL Injection", "flag": "CORP{sql_1nj3ct10n_byp4ss_4uth3nt1c4t10n}", "hint": "El panel de login es vulnerable a inyección. Intenta anular la contraseña con admin'#."},
    {"id": 7, "title": "Flag 07: File Upload (Bajo)", "flag": "CORP{w3bsh3ll_upl04d3d_n0_f1lt3r_byp4ss}", "hint": "Sube una shell básica en PHP en el panel de carga de archivos (Nivel Bajo)."},
    {"id": 8, "title": "Flag 08: File Upload (Medio)", "flag": "CORP{burp_su1t3_byp4ss_c0nt3nt_typ3_f1lt3r}", "hint": "El nivel medio filtra por tipo de archivo. Engaña al servidor enviando el shell con Curl y Content-Type: image/jpeg."},
    {"id": 9, "title": "Flag 09: Command Injection", "flag": "CORP{c0mm4nd_1nj3ct10n_r3v3rs3_sh3ll_0wn3d}", "hint": "El panel de diagnóstico de red permite inyectar comandos de sistema usando una barra vertical (|)."},
    {"id": 10, "title": "Flag 10: Escalada (SSH)", "flag": "CORP{ssh_pr1v4t3_k3y_l34k_p7w_r00t}", "hint": "Usa la ejecución de comandos web para buscar una llave privada (id_rsa) expuesta en los directorios."},
    {"id": 11, "title": "Flag 11: Blue Team (Logs)", "flag": "CORP{l0g_4n4lys1s_r3v34ls_th3_4tt4ck3r}", "hint": "Ve a la terminal de Ubuntu y audita los logs en /var/log/apache2/access.log para cerrar la intrusión."},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicializar el progreso si es la primera vez
    if 'solved' not in session:
        session['solved'] = []
        
    mensaje = None
    clase_mensaje = None

    if request.method == 'POST':
        flag_ingresada = request.form.get('flag', '').strip()
        found = False
        
        # Buscar si la llave ingresada coincide con alguna bandera
        for f in FLAGS:
            if f['flag'] == flag_ingresada:
                if f['id'] not in session['solved']:
                    session['solved'].append(f['id'])
                    session.modified = True
                    mensaje = f"¡ACCESO CONCEDIDO! {f['title']} desencriptada."
                    clase_mensaje = "success"
                else:
                    mensaje = "Ya habías registrado esta llave en el sistema."
                    clase_mensaje = "info"
                found = True
                break
                
        if not found:
            mensaje = "FIRMA INCORRECTA. El payload fue rechazado."
            clase_mensaje = "error"

    return render_template('index.html', flags=FLAGS, solved=session['solved'], mensaje=mensaje, clase=clase_mensaje)

# Ruta oculta para reiniciar el progreso (útil para cuando presentes)
@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)