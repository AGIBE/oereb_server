import re
from pyramid.request import Request
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPSeeOther, HTTPBadRequest
from pyramid_oereb.contrib.stats.decorators import log_response


def check_code(code: str) -> bool:
    # Aus der Weisung DATA-EXTRACT (angepasst auf lowercase)
    pattern = r"^(ch\.[a-zA-Z][a-zA-Z0-9]*)|(ch\.[a-z]{2}\.[a-zA-Z][a-zA-Z0-9]*)|(ch\.[0-9]{4}\.[a-zA-Z][a-zA-Z0-9]*)|(fl\.[a-zA-Z][a-zA-Z0-9]*)$"
    return bool(re.fullmatch(pattern, code))


def is_valid_parameter(parameters: dict, parameter_to_validate: str) -> bool:
    is_valid = True
    if parameters.get(parameter_to_validate):
        parameter_value = parameters.get(parameter_to_validate)
        if parameter_to_validate == "lang":
            if parameter_value in ["de", "fr"]:
                is_valid = True
            else:
                is_valid = False
        elif parameter_to_validate == "code":
            is_valid = check_code(parameter_value)
        else:
            is_valid = False
    else:
        is_valid = False

    return is_valid


@view_config(route_name="legend_topic", decorator=log_response)
def legend_topic(request: Request):
    # Alle Parameter (Name und Wert) auf lowercase umstellen
    parameters = {k.lower(): v.lower() for k, v in request.params.items()}

    if is_valid_parameter(parameters, "lang"):
        lang = parameters["lang"]
    else:
        return HTTPBadRequest(detail="Parameter lang fehlt.")

    if is_valid_parameter(parameters, "code"):
        topic_code = parameters["code"]
    else:
        return HTTPBadRequest(detail="Parameter code fehlt.")

    # Der Einfachheit halber wird immer auf die produktive URL umgeleitet.
    legend_url = (
        f"https://oerebfiles.apps.be.ch/legenden/themen/{topic_code}_{lang}.html"
    )
    return HTTPSeeOther(location=legend_url)
