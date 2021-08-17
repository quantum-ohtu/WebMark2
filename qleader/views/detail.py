from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import Result
import qleader.fci.fci_H2 as fci


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def detail(request, result_id):

    try:
        result = Result.objects.get(id=result_id)
    except Exception as error:
        return Response({"error": repr(error)}, status.HTTP_404_NOT_FOUND, template_name="detail.html")

    if not result.public and result.user != request.user:
        raise PermissionDenied

    if request.method == "GET":
        runs = result.get_runs()
        distances = [results.distance for results in runs]
        energies = [results.energy for results in runs]
        iteration_energies = [results.get_iteration_energies() for results in runs]
        fci_distances, fci_energies = zip(*fci.get_fci("def2-QZVPPD"))
        name = " ".join([result.basis_set, result.transformation])

        return Response(
            {
                "result": result,
                "runs": runs,
                "name": name,
                "energies": energies,
                "distances": distances,
                "iterationEnergies": iteration_energies,
                "fci_distances": list(fci_distances),
                "fci_energies": list(fci_energies),
            },
            template_name="detail.html",
        )
