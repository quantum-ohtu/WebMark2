import ast
from qleader.models.result import Result
from qleader.models.run_gradient import RunGradient
from qleader.models.run_scipy import RunScipyNelderMead, RunScipyBFGS, RunScipyLBFGSB, RunScipyCOBYLA
from qleader.fci.fci_H2 import get_fci_value_by_dist
from qleader.models.optimizers import gradient_optimizers
import numpy as np


def create_result(dict):
    try:
        keys = ["tqversion", "optimizer", "basis_set", "transformation"]
        result_dict = {key: dict[key] for key in keys}
        result = Result(**result_dict)
        result.save()
        runs_all = create_runs(result, dict, dict["optimizer"])
        lowest_energy = float("inf")
        lowest_delta = float("inf")
        lowest_energy_distance = 0
        lowest_delta_distance = 0
        for run in runs_all:
            if run.energy < lowest_energy:
                lowest_energy = run.energy
                lowest_energy_distance = run.distance
            delta = abs(run.energy - get_fci_value_by_dist("def2-QZVPPD", run.distance))
            if delta < lowest_delta:
                lowest_delta = delta
                lowest_delta_distance = run.distance
            run.save()
        result.min_energy = lowest_energy
        result.min_energy_distance = lowest_energy_distance
        result.min_delta = lowest_delta
        result.min_delta_distance = lowest_delta_distance
        result.variance_from_fci = np.var(
            [r.energy - get_fci_value_by_dist("def2-QZVPPD", r.distance) for r in runs_all]
        )
        result.save()
        return "NoErr"
    except Exception as e1:
        try:
            result.delete()
        except Exception as e2:
            return str(e2)
        return str(e1)


def add_extra_fields(sep_data, data, optimizer):
    if optimizer.upper() in ["NELDER-MEAD", "BFGS", "L-BFGS-B", "COBYLA"]:
        for i, entry in enumerate(sep_data):
            entry.update(get_scipy_results(data, i))
    elif optimizer.upper() in gradient_optimizers:
        for i, entry in enumerate(sep_data):
            entry.update(get_moments(data, i))
    return sep_data


def create_runs(result, data, optimizer):
    sep_data = [{"energy": e} for e in data["energies"]]
    for i, entry in enumerate(sep_data):
        entry["variables"] = get_variables(data, i)
        entry["hamiltonian"] = get_hamiltonian(data, i)
        entry["ansatz"] = get_ansatz(data, i)
        entry["molecule"] = get_molecule(data, i)
        entry["distance"] = get_distance(data, i)
        entry.update(get_history(data, i))
    sep_data = add_extra_fields(sep_data, data, optimizer)
    runs = create_runs_based_on_optimizer(result, sep_data)
    return runs


# Select correct class depending on the optimizer used.
def create_runs_based_on_optimizer(result, sep_data):
    if result.get_optimizer().upper() == "NELDER-MEAD":
        return [RunScipyNelderMead(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().upper() == "BFGS":
        return [RunScipyBFGS(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().upper() == "L-BFGS-B":
        return [RunScipyLBFGSB(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().upper() == "COBYLA":
        return [RunScipyCOBYLA(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().upper() in gradient_optimizers:
        return [RunGradient(result=result, **entry) for entry in sep_data]
    else:
        print("*** Unknown optimizer: " + result.get_optimizer())    # TODO: Handle unkown optimizer


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


def get_moments(data, i):
    return {"moments": data["moments"][i]}
