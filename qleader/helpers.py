import ast
from qleader.models import QBatch, QResult


def create_qbatch(data):
    keys = ["tqversion", "optimizer", "basis_set", "transformation"]
    qbatch_dict = {key: data[key] for key in keys}
    return QBatch(**qbatch_dict)


def create_qresults(data, qbatch):
    sep_data = [{"energy": e} for e in data["energies"]]

    # TODO parse variables, ansatz and molecule more thoroughly.
    for i, entry in enumerate(sep_data):
        entry["variables"] = data["variables"][i]
        entry["hamiltonian"] = data["hamiltonian"][i]
        entry["ansatz"] = data["ansatz"][i]
        entry["molecule"] = data["molecule"][i]
        entry["distance"] = data["distances"][i]
        history_dict = {
            str(key): str(val)
            for key, val in ast.literal_eval(data["histories"][i]).items()
        }
        entry.update(history_dict)
        scipy_results_dict = ast.literal_eval(data["scipy_results"][i])
        entry.update(scipy_results_dict)

    QResults = [QResult(batch=qbatch, **entry) for entry in sep_data]
    return QResults
