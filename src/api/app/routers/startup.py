import logging

import aiohttp
import psycopg2
from fastapi import APIRouter, Response
from opentelemetry import trace

from ..config import get_settings

tracer = trace.get_tracer(__name__)

router = APIRouter()
logger = logging.getLogger("uvicorn.error")


@tracer.start_as_current_span(name="startup")
@router.get("/startup")
async def startup_probe(response: Response):
    azure_openai_status_dict = await check_azure_openai()

    database_status_dict = check_database_status()

    return_value = {
        "azure_openai": azure_openai_status_dict,
        "database": database_status_dict,
    }

    response.status_code = 200

    # Set the response status code to 503 if any of the checks failed
    for key, value in return_value.items():
        if value["status"] != 200:
            response.status_code = 503
            break

    return_value["status"] = response.status_code

    logger.info(return_value)

    return return_value


@tracer.start_as_current_span(name="check_azure_openai")
async def check_azure_openai():
    headers = {
        "Content-Type": "application/json",
        "api-key": get_settings().azure_openai_api_key,
    }

    body = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ]
    }
    async with aiohttp.ClientSession() as session:
        azure_openai_status = await session.post(
            url=(
                f"{get_settings().azure_openai_endpoint}openai/deployments/"
                f"{get_settings().openai_model_id}/chat/completions?"
                f"api-version={get_settings().openai_api_version}"
            ),
            json=body,
            headers=headers,
        )

        status_dict = {}

        if azure_openai_status.status == 200:
            status_dict = {"status": 200}
        else:
            status_dict = {
                "status": 503,
                "error": f"Error: {azure_openai_status.status} - {azure_openai_status.reason}",
            }

    return status_dict


@tracer.start_as_current_span(name="check_database_status")
def check_database_status():
    try:
        with psycopg2.connect(get_settings().postgresql_connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                status = cursor.fetchone()
    except psycopg2.Error as e:
        status = (0, e)

    return_value = {}

    if status[0] == 1:
        return_value = {"status": 200}
    else:
        return_value = {
            "status": 503,
            "error": f"Error: {status[1]}",
        }

    return return_value
