import functools
import pytest
from sqlmodel import SQLModel, Session, select
from klm_techcase import models
import sqlalchemy as sqla
import shutil
import socket
import os
from fastapi.testclient import TestClient
import re

from klm_techcase.main import app


@functools.cache
def get_docker_ip() -> str:
    if docker_host := os.getenv("DOCKER_HOST"):
        match = re.match(r"([^:/]+://)?(?P<host>[^:]+)(:\d+)?", docker_host)
        assert match, f"invalid DOCKER_HOST: {docker_host}"
        return socket.gethostbyname(match.group("host"))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    addr = sock.getsockname()[0]
    sock.close()
    return addr


os.environ["DB_URL"] = f"postgresql://postgres:password@{get_docker_ip()}:5432/klm"


@pytest.fixture(scope="session")
def docker_compose_command():
    return shutil.which("docker-compose") or "docker compose"


@pytest.fixture(scope="session")
def docker_compose_file():
    return "tests/compose.yml"


@pytest.fixture(scope="function")
def db(docker_ip, docker_services):
    """DB init, yield and teardown per test"""

    def is_responsive(eng):
        try:
            conn = eng.connect()
            conn.execute(sqla.text("SELECT 1"))
            return True
        except Exception:
            return False

    engine_kwargs = {
        "connect_args": {"connect_timeout": 10},
        "poolclass": sqla.pool.NullPool,
    }
    engine = sqla.create_engine(os.environ["DB_URL"], **engine_kwargs)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(engine)
    )
    meta = SQLModel.metadata
    meta.create_all(engine)
    yield engine
    meta.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def client(db):
    return TestClient(app)


def read_all_notes(db):
    with Session(db) as session:
        results = list(session.exec(select(models.Note)))
    return results
