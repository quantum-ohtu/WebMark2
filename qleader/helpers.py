import ast
from qleader.models import QBatch, QResult


def create_qbatch(data):
    keys = ['tqversion', 'optimizer', 'basis_set', 'transformation']
    qbatch_dict = {key: data[key] for key in keys}
    return QBatch(**qbatch_dict)


def create_qresults(data, qbatch):

    # Separate energies DONE
    sep_data = [{'energy': e} for e in data['energies']]

    # TODO, figure out what do with variables when hardware accelerated
    # ansatz is used. Just dump variables for now.
    for i, entry in enumerate(sep_data):
        entry['variables'] = data['variables'][i]

    # TODO, should the history of a run be broken down into a separate db table?
    # Separate histories
    for i, entry in enumerate(sep_data):
        history_dict = ast.literal_eval(data['histories'][i])
        history_dict = {key: str(val) for key, val in history_dict.items()}
        entry.update(history_dict)

    # TODO, investigate field 'x'
    # Separate scipy_results
    for i, entry in enumerate(sep_data):
        scipy_results_dict = ast.literal_eval(data['scipy_results'][i])
        entry.update(scipy_results_dict)

    # Separate hamiltonians
    for i, entry in enumerate(sep_data):
        entry['hamiltonian'] = data['hamiltonian'][i]

    # TODO, nothing special has been done here yet
    # Separate ansatz
    for i, entry in enumerate(sep_data):
        entry['ansatz'] = data['ansatz'][i]

    # TODO, nothing special has been done here yet
    # Separate molecule
    for i, entry in enumerate(sep_data):
        entry['molecule'] = data['molecule'][i]
        entry['distance'] = data['distances'][i]

    # Create django models
    QResults = []
    for entry in sep_data:
        qres = QResult(batch=qbatch, **entry)
        QResults.append(qres)

    return QResults
