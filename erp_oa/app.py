from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oa_agroquimicos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'cambiar-en-produccion-2024'

    from models import db
    db.init_app(app)

    Migrate(app, db)

    from routes.oas import oas_bp
    from routes.maestros import maestros_bp
    from routes.importacion import importacion_bp

    app.register_blueprint(oas_bp, url_prefix='/oas')
    app.register_blueprint(maestros_bp, url_prefix='/maestros')
    app.register_blueprint(importacion_bp, url_prefix='/importar')

    @app.route('/')
    def index():
        return redirect(url_for('oas.lista'))

    import seed
    seed.init_app(app)

    @app.shell_context_processor
    def shell_ctx():
        from models import Agricola, Cuartel, Producto, OrdenAplicacion, OAProducto, OACuartel, TipoAplicacion
        return dict(db=db, Agricola=Agricola, Cuartel=Cuartel, Producto=Producto,
                    OrdenAplicacion=OrdenAplicacion, OAProducto=OAProducto, OACuartel=OACuartel,
                    TipoAplicacion=TipoAplicacion)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
