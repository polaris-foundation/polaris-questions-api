from typing import Any, Dict, Optional, Tuple

import connexion

from dhos_questions_api.models.survey import Survey


def survey_by_uuid_protection(
    jwt_claims: Dict, claims_map: Optional[Dict], **params: Any
) -> bool:
    try:
        user_type, user_id = get_user_type_and_id(jwt_claims)
        if user_type is False:
            return False

        survey_uuid = params.get("survey_uuid")
        if survey_uuid:
            return survey_matches_user(jwt_claims, survey_uuid, user_id, user_type)
        else:
            if not survey_uuid:
                request = connexion.request.get_json()
                if not request:
                    return False

                if type(request) == list:
                    for answer in request:
                        survey_uuid = answer.get("survey_uuid")
                        if (
                            survey_matches_user(
                                jwt_claims, survey_uuid, user_id, user_type
                            )
                            is False
                        ):
                            return False
                else:
                    survey_uuid = request.get("survey_uuid")
                    return survey_matches_user(
                        jwt_claims, survey_uuid, user_id, user_type
                    )

    except (AttributeError, ValueError):
        return False

    return True


def get_user_type_and_id(jwt_claims: Dict) -> Tuple:
    if jwt_claims.get("clinician_id"):
        user_type = "clinician"
        user_id = jwt_claims["clinician_id"]
    elif jwt_claims.get("patient_id"):
        user_type = "patient"
        user_id = jwt_claims["patient_id"]
    else:
        return False, False
    return user_type, user_id


def survey_matches_user(
    jwt_claims: Dict, survey_uuid: str, user_id: str, user_type: str
) -> bool:
    survey = Survey.query.filter_by(uuid=survey_uuid).first_or_404()

    if survey.user_type != user_type:
        return False

    if survey.user_id != user_id:
        return False

    return True
