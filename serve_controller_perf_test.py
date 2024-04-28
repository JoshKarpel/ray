import asyncio
from asyncio import create_task, sleep, wait, wait_for
from time import monotonic

from ray import serve
from ray.serve.handle import DeploymentHandle


@serve.deployment(
    ray_actor_options={"num_cpus": 0, "memory": 0},
)
class Deployment:
    def __init__(self, id: str):
        self.id = id

    def __call__(self) -> str:
        return self.id


async def worker(target: str, worker_id: str) -> None:
    handle = DeploymentHandle(
        app_name=f"app-{target}", deployment_name=f"worker-{target}"
    )
    while True:
        remote_start = monotonic()
        await handle.remote()
        # print(f"Worker {worker_id}: {monotonic() - remote_start:.6f} seconds")


if __name__ == "__main__":
    for id in range(1):
        serve.run(
            Deployment.options(name=f"worker-{id}").bind(id),
            name=f"app-{id}",
            route_prefix=None,
        )

    async def main() -> None:
        await sleep(11)
        # await wait_for(
        #     wait(
        #         [
        #             create_task(worker(target=str(id), worker_id=str(worker_id)))
        #             for worker_id in range(1)
        #             for id in range(1)
        #         ]
        #     ),
        #     timeout=10,
        # )

    asyncio.run(main())
