import subprocess
from pathlib import Path

import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy

IMAGE_TAG = "liine-take-home:e2e"
REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def base_url():
    subprocess.run(
        ["docker", "build", "-q", "-t", IMAGE_TAG, str(REPO_ROOT)],
        check=True,
    )
    container = (
        DockerContainer(IMAGE_TAG)
        .with_exposed_ports(8000)
        .waiting_for(LogMessageWaitStrategy("Application startup complete").with_startup_timeout(30))
    )
    with container:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(8000)
        yield f"http://{host}:{port}"
