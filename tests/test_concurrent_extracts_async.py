import asyncio
import httpx
import pytest

async def make_request(session, url, i=None, j=None):
    response = await session.get(url)
    tag = f"Task-{i} Run-{j}" if i is not None and j is not None else "Referenz"
    print(f"Request {tag} fertig")
    return response

async def fast_request_group(session, url, i, expected_length):
    tasks = [
        make_request(session, url, i, j)
        for j in range(6)
    ]
    responses = await asyncio.gather(*tasks)

    # Prüfen, ob alle Inhalte gleich lang sind wie erwartet
    for j, resp in enumerate(responses):
        actual = count_plr_in_json_extract(resp)
        legend_texts = []
        for plr in resp.json()["GetExtractByIdResponse"]["extract"]["RealEstate"]["RestrictionOnLandownership"]:
            legend_texts.append(plr['LegendText'][0]['Text'])
        assert actual == expected_length, f"fast_request: Länge {actual} != erwartet {expected_length} {legend_texts}"

    return responses

async def slow_request(session, url, expected_length):
    response = await make_request(session, url)
    actual = count_plr_in_json_extract(response)
    assert actual == expected_length, f"slow_request: Länge {actual} != erwartet {expected_length} {response.request.url}"
    return response

# ---------- Test ----------

@pytest.mark.asyncio
async def test_parallel_requests_with_reference_check(running_server_instance, egrids_for_concurrent_error):
    async with httpx.AsyncClient(timeout=None) as client:
        slow_egrid, fast_egrid = egrids_for_concurrent_error
        slow_extract_url = running_server_instance + "/extract/json?egrid=" + slow_egrid
        fast_extract_url = running_server_instance + "/extract/json?egrid=" + fast_egrid

        # Zuerst: Referenz-Responses holen (nacheinander)
        # fast_ref_response = await make_request(client, fast_extract_url)
        fast_ref_response = httpx.get(fast_extract_url)
        fast_ref_len = count_plr_in_json_extract(fast_ref_response)
        print(f"Fast Requests Expectend Nr of PLrs: {fast_ref_len}")

        #slow_ref_response = await make_request(client, slow_extract_url)
        slow_ref_response = httpx.get(slow_extract_url)
        slow_ref_len = count_plr_in_json_extract(slow_ref_response)
        print(f"Slow Requests Expectend Nr of PLrs: {slow_ref_len}")

        # Parallele Requests vorbereiten
        slow_task = asyncio.create_task(slow_request(client, slow_extract_url, slow_ref_len))

        fast_tasks = [
            asyncio.create_task(fast_request_group(client, fast_extract_url, i, fast_ref_len))
            for i in range(4)
        ]

        # Alle Tasks parallel ausführen
        await asyncio.gather(slow_task, *fast_tasks)

    print("✅ Alle Inhalte entsprechen den Referenzgrößen.")

def count_plr_in_json_extract(response: httpx.Response):
    json = response.json()
    number_of_plrs = len(
        json["GetExtractByIdResponse"]["extract"]["RealEstate"][
            "RestrictionOnLandownership"
        ]
    )
    return number_of_plrs
