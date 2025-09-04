import pytest
import asyncio
import httpx

REPEATS_SLOW_EXTRACT = 1   # Anzahl Wiederholungen in Strang A
THREADS_FAST_EXTRACT = 5   # parallele Stränge für Request B
REPEATS_FAST_EXTRACT = 2   # Anzahl Wiederholungen pro Strang in Strang B


@pytest.mark.asyncio
async def test_api_parallel_with_reference_check_async(running_server_instance, egrids_for_concurrent_error):
    async with httpx.AsyncClient(timeout=None) as client:
        slow_egrid, fast_egrid = egrids_for_concurrent_error
        slow_extract_url = running_server_instance + "/extract/json?egrid=" + slow_egrid
        fast_extract_url = running_server_instance + "/extract/json?egrid=" + fast_egrid

        # 1. Referenzwerte holen
        slow_ref_response = await client.get(slow_extract_url)
        slow_ref_response.raise_for_status()
        slow_ref_len = count_plr_in_json_extract(slow_ref_response)

        fast_ref_response = await client.get(fast_extract_url)
        fast_ref_response.raise_for_status()
        fast_ref_len = count_plr_in_json_extract(fast_ref_response)

        # 2. Hilfsfunktionen für wiederholte Requests
        async def run_slow_extract():
            for i in range(REPEATS_SLOW_EXTRACT):
                r = await client.get(slow_extract_url)
                r.raise_for_status()
                number_of_plrs = count_plr_in_json_extract(r)
                assert number_of_plrs == slow_ref_len, (
                    f"Slow Extract Durchlauf {i+1} hat abweichende Antwort (erwartet: {slow_ref_len}; effektiv: {number_of_plrs})"
                )

        async def run_fast_extract():
            for i in range(REPEATS_FAST_EXTRACT):
                r = await client.get(fast_extract_url)
                r.raise_for_status()
                number_of_plrs = count_plr_in_json_extract(r)
                assert number_of_plrs == fast_ref_len, (
                    f"Fast Extract Durchlauf {i+1} hat abweichende Antwort (erwartet: {fast_ref_len}; effektiv: {number_of_plrs})"
                )

        # 3. Parallele Ausführung:
        #    - Strang A (3x A nacheinander)
        #    - Strang B (5 parallele Stränge, je 3x B)
        tasks = [asyncio.create_task(run_slow_extract())]
        for _ in range(THREADS_FAST_EXTRACT):
            tasks.append(asyncio.create_task(run_fast_extract()))

        await asyncio.gather(*tasks)

def count_plr_in_json_extract(response: httpx.Response):
    js = response.json()
    number_of_plrs = len(
        js["GetExtractByIdResponse"]["extract"]["RealEstate"][
            "RestrictionOnLandownership"
        ]
    )
    return number_of_plrs
