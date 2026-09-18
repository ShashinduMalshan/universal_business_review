import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.pipeline_manager import PipelineManager
from backend.app.db.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    init_db()
    PipelineManager.get_instance()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_positive_review():
    return "I had a wonderful experience at this restaurant. The food was fresh, flavorful, and beautifully presented, and every dish we tried was delicious. The staff were friendly, attentive, and professional, making us feel very welcome throughout our visit. The atmosphere was comfortable, clean, and relaxing."

@pytest.fixture
def sample_neutral_review():
    return "The food was decent, and the service was acceptable. Nothing was particularly special, but it was an okay place for a casual meal."

@pytest.fixture
def sample_negative_review():
    return "The food was disappointing, and the service was very slow. The staff were not friendly, and the overall experience was not worth the price."

@pytest.fixture
def sample_critical_review():
    return "Severe food poisoning after eating the raw seafood platter! Had to visit the emergency clinic. Total scam and dangerous hygiene!"
