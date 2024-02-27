"""Example of submitting a docker job to the API."""
import asyncio
import requests
from bacalhau_apiclient.models.deal import Deal
from bacalhau_apiclient.models.job_spec_docker import JobSpecDocker
from bacalhau_apiclient.models.job_spec_language import JobSpecLanguage
from bacalhau_apiclient.models.publisher_spec import PublisherSpec
from bacalhau_apiclient.models.spec import Spec
from bacalhau_apiclient.models.storage_spec import StorageSpec

from bacalhau_sdk.api import submit, results
from bacalhau_sdk.config import get_client_id
from vector_search.src.entities import VectorSearchResult

IPFS_BASE_URL: str = "https://ipfs.io/ipfs/{}/stdout"


def _download(cid: str) -> str:
    response = requests.get(IPFS_BASE_URL.format(cid))
    return response.text


async def execute(cid: str, query: str) -> VectorSearchResult:
    data = dict(
        APIVersion="V1beta1",
        ClientID=get_client_id(),
        Spec=Spec(
            engine="Docker",
            publisher_spec=PublisherSpec(type="ipfs"),
            docker=JobSpecDocker(
                image="kgrofelnik/search:12",
                entrypoint=["python", "search.py", "--query", query, "--cid", cid],
                working_directory="/"
            ),
            inputs=[
                StorageSpec(
                    storage_source="IPFS",
                    cid=cid,
                    path=f"/inputs/{cid}",
                )
            ],
            language=JobSpecLanguage(job_context=None),
            wasm=None,
            resources=None,
            timeout=1800,
            outputs=[
                StorageSpec(
                    storage_source="IPFS",
                    name="outputs",
                    path="/outputs",
                )
            ],
            deal=Deal(concurrency=1),
            do_not_track=False,
        ),
    )
    job = submit(data)
    job_data = results(job_id=job.job.metadata.id)
    result = job_data.results
    while len(result) == 0:
        await asyncio.sleep(5)
        job_data = results(job_id=job.job.metadata.id)
        result = job_data.results
    cid = result[0].data.cid
    content = _download(cid)
    return VectorSearchResult(
        content=content,
        job_id=job.job.metadata.id,
    )
