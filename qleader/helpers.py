import ast
from qleader.models import QBatch, QResult


def create_qbatch(data):
    keys = ["tqversion", "optimizer", "basis_set", "transformation"]
    qbatch_dict = {key: data[key] for key in keys}
    return QBatch(**qbatch_dict)

def get_variables(data, i):
    return data["variables"][i]

def get_hamiltonian(data, i):
    return data["hamiltonian"][i]

def get_ansatz(data, i):
    return data["ansatz"][i]

def get_molecule(data, i):
    return data["molecule"][i]

def get_distance(data, i):
    return data["distances"][i]

def get_history(data, i):
    history_dict = {
        str(key): str(val)
        for key, val in ast.literal_eval(data["histories"][i]).items()
    }
    return history_dict

def get_scipy_results(data, i):
    return ast.literal_eval(data["scipy_results"][i])

def create_qresults(data, qbatch):
    sep_data = [{"energy": e} for e in data["energies"]]
    for i, entry in enumerate(sep_data):
        entry["variables"] = get_variables(data, i)
        entry["hamiltonian"] = get_hamiltonian(data, i)
        entry["ansatz"] = get_ansatz(data, i)
        entry["molecule"] = get_molecule(data, i)
        entry["distance"] = get_distance(data, i)
        entry.update(get_history(data, i))
        entry.update(get_scipy_results(data, i))
    QResults = [QResult(batch=qbatch, **entry) for entry in sep_data]
    return QResults
