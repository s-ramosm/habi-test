from flask import Flask, request
from src.controlers.immovables import ImmovableControler, StatusControler

app = Flask(__name__)


@app.route('/')
def get_all_immovables():

    _ImmovableControler = ImmovableControler()

    _statusControler = StatusControler() 
    
    immovables_data = _ImmovableControler.get_all()
    
    data_status = _statusControler.get_status_by_property_ids(
        ids = [immovable.get("id") for immovable in immovables_data ]
    )
    
    for immovable in immovables_data:
        immovable["status"] = data_status.get(immovable["id"] , [{}])[0]  
    
    print(data_status)

    query_params = request.args.to_dict()
    return immovables_data

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
