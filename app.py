from flask import Flask
from pages.autenticacion import autenticacion_bp
from pages.usuario import usuario_bp
from pages.mascota import mascota_bp
from pages.reserva import reserva_bp
from pages.publico import publico_bp

app = Flask(__name__)
app.secret_key = "111"

# Registrar blueprints
app.register_blueprint(autenticacion_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(mascota_bp)
app.register_blueprint(reserva_bp)
app.register_blueprint(publico_bp)

if __name__ == "__main__":
    from threading import Timer
    import webbrowser

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000/")

    Timer(1, open_browser).start()
    app.run(debug=True)
