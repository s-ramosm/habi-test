from flask import Flask, request
from src.controlers.immovables import ImmovableControler
from src.core.exceptions import FilterNotAllowed

app = Flask(__name__)


@app.route('/')
def get_all_immovables():
    """Retrieve all immovables based on query parameters."""

    immovable_controller = ImmovableControler()
    query_params = request.args.to_dict()

    try:
        immovables_data = immovable_controller.get_all(**query_params)
    except FilterNotAllowed:
        return {"msg": "One or more filters in your request are not allowed"}, 400
    except ValueError:
        return {"msg": "Year format incorrect"}, 400
    except Exception:
        return {"msg": "Server error"}, 500

    return immovables_data

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
