from collections.abc import AsyncGenerator
from uuid import UUID

import pytest
from litestar.testing import AsyncTestClient

PROJECT_INIT_TITLE = "First Project"
PROJECT_UPDATED_TITLE = "First Investigation"
PROJECT_UPDATED_DESCRIPTION = "Project Description"

# Investigation fixture


@pytest.fixture(scope="function")
async def setup_investigation(test_client: AsyncTestClient) -> AsyncGenerator[UUID, None]:
    response = await test_client.post("/investigation", json={"title": PROJECT_INIT_TITLE})
    assert response.status_code == 201
    response_id = response.json()["id"]
    yield response_id

    await test_client.delete(f"investigation/{response_id}")


@pytest.fixture(scope="function")
async def setup_investigation_no_cleanup(test_client: AsyncTestClient) -> AsyncGenerator[UUID, None]:
    response = await test_client.post(
        "/investigation", json={"title": PROJECT_UPDATED_TITLE, "description": PROJECT_UPDATED_DESCRIPTION}
    )
    assert response.status_code == 201
    response_id = response.json()["id"]
    yield response_id


@pytest.fixture(scope="function")
async def setup_investigation_with_cleanup(test_client: AsyncTestClient) -> AsyncGenerator[UUID, None]:
    response = await test_client.post(
        "/investigation", json={"title": PROJECT_UPDATED_TITLE, "description": PROJECT_UPDATED_DESCRIPTION}
    )
    assert response.status_code == 201
    response_id = response.json()["id"]
    yield response_id

    await test_client.delete(f"investigation/{response_id}")


# Study fixture
STUDY_INIT_TITLE = "First study"
STUDY_INIT_OBJECTIVE = "Study Objective"
STUDY_INIT_START_DATE = "2020-01-01T00:00:00"
STUDY_INIT_END_DATE = "2020-05-01T00:00:00"

STUDY_UPDATED_TITLE = "First study updated"
STUDY_UPDATED_OBJECTIVE = "Study Objective updated"
STUDY_UPDATED_START_DATE = "2020-01-05T00:00:00"
STUDY_UPDATED_END_DATE = "2020-05-05T00:00:00"


@pytest.fixture(scope="function")
async def setup_study(
    setup_investigation: UUID, test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID], None]:
    project_id = setup_investigation
    response = await test_client.post(
        "study",
        json={
            "title": STUDY_INIT_TITLE,
            "objective": STUDY_INIT_OBJECTIVE,
            "startDate": STUDY_INIT_START_DATE,
            "endDate": STUDY_INIT_END_DATE,
            "investigationId": project_id,
        },
    )
    assert response.status_code == 201
    study_id = response.json()["id"]
    yield (project_id, study_id)
    await test_client.delete(f"study/{study_id}")


@pytest.fixture(scope="function")
async def setup_second_study(
    setup_investigation: UUID, test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID], None]:
    project_id = setup_investigation
    response = await test_client.post(
        "study",
        json={
            "title": STUDY_UPDATED_TITLE,
            "objective": STUDY_UPDATED_OBJECTIVE,
            "startDate": STUDY_UPDATED_START_DATE,
            "endDate": STUDY_UPDATED_END_DATE,
            "investigationId": project_id,
        },
    )
    assert response.status_code == 201
    study_id = response.json()["id"]
    yield (project_id, study_id)
    await test_client.delete(f"study/{study_id}")


@pytest.fixture(scope="function")
async def update_study(
    setup_study: tuple[UUID, UUID], setup_investigation_with_cleanup: UUID, test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID], None]:
    project_id = setup_investigation_with_cleanup
    _, study_id = setup_study
    response = await test_client.put(
        f"study/{study_id}",
        json={
            "title": STUDY_UPDATED_TITLE,
            "objective": STUDY_UPDATED_OBJECTIVE,
            "startDate": STUDY_UPDATED_START_DATE,
            "endDate": STUDY_UPDATED_END_DATE,
            "investigationId": project_id,
        },
    )
    assert response.status_code == 200
    yield (project_id, study_id)


# Vocabulary Fixture
INSTITUTION_TYPE_NAMESPACE = "Institution"
RESEARCH_UNIVERSITY = "Research University"
RESEARCH_DEPARTMENT = "Research Department"


@pytest.fixture(scope="function")
async def setup_vocab_university_and_department(
    test_client: AsyncTestClient,
) -> AsyncGenerator[tuple[UUID, UUID], None]:
    uni_response = await test_client.post(
        "vocabulary", json={"title": RESEARCH_UNIVERSITY, "namespace": INSTITUTION_TYPE_NAMESPACE}
    )
    assert uni_response.status_code == 201
    uni_id = uni_response.json()["id"]

    department_response = await test_client.post(
        "vocabulary", json={"title": RESEARCH_DEPARTMENT, "namespace": INSTITUTION_TYPE_NAMESPACE}
    )
    assert department_response.status_code == 201
    department_id = department_response.json()["id"]

    yield (uni_id, department_id)

    await test_client.delete(f"vocabulary/{uni_id}")
    await test_client.delete(f"vocabulary/{department_id}")


# Institution Fixture
UOA_TITLE = "The University of Adelaide"
COUNTRY = "Australia"
TPA_TITLE = "The Plant Accelerator"
APPN_TITLE = "Australian Plant Phenomic Network"


@pytest.fixture(scope="function")
async def setup_UOA(
    setup_vocab_university_and_department: tuple[UUID, UUID], test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID, UUID], None]:
    uni_id, department_id = setup_vocab_university_and_department
    response = await test_client.post(
        "institution", json={"title": UOA_TITLE, "institutionTypeId": uni_id, "country": COUNTRY}
    )
    assert response.status_code == 201
    uoa_id = response.json()["id"]
    yield uoa_id, uni_id, department_id

    await test_client.delete(f"institution/{uoa_id}")


@pytest.fixture(scope="function")
async def setup_APPN(
    setup_UOA: tuple[UUID, UUID, UUID], test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID, UUID, UUID], None]:
    uoa_id, uni_id, department_id = setup_UOA
    response = await test_client.post(
        "institution",
        json={"title": APPN_TITLE, "institutionTypeId": department_id, "country": COUNTRY, "parentId": [uoa_id]},
    )
    assert response.status_code == 201
    appn_id = response.json()["id"]
    yield appn_id, uoa_id, uni_id, department_id

    await test_client.delete(f"institution/{appn_id}")


@pytest.fixture(scope="function")
async def setup_TPA(
    setup_APPN: tuple[UUID, UUID, UUID, UUID], test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID, UUID, UUID, UUID], None]:
    appn_id, uoa_id, uni_id, department_id = setup_APPN
    response = await test_client.post(
        "institution",
        json={"title": TPA_TITLE, "institutionTypeId": department_id, "country": COUNTRY, "parentId": [uoa_id]},
    )
    assert response.status_code == 201
    tpa_id = response.json()["id"]
    yield tpa_id, appn_id, uoa_id, uni_id, department_id
    await test_client.delete(f"institution/{tpa_id}")


@pytest.fixture(scope="function")
async def update_TPA(
    setup_TPA: tuple[UUID, UUID, UUID, UUID, UUID], test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID, UUID, UUID, UUID], None]:
    tpa_id, appn_id, uoa_id, uni_id, department_id = setup_TPA
    response = await test_client.put(
        f"institution/{tpa_id}",
        json={
            "title": TPA_TITLE,
            "institutionTypeId": department_id,
            "country": COUNTRY,
            "parentId": [uoa_id, appn_id],
        },
    )
    assert response.status_code == 200
    yield tpa_id, appn_id, uoa_id, uni_id, department_id


@pytest.fixture(scope="function")
async def delete_APPN(
    update_TPA: tuple[UUID, UUID, UUID, UUID, UUID], test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID, UUID, UUID, UUID], None]:
    tpa_id, appn_id, uoa_id, uni_id, department_id = update_TPA
    response = await test_client.delete(f"institution/{appn_id}")
    assert response.status_code == 204
    yield tpa_id, appn_id, uoa_id, uni_id, department_id


# Data file fixture
DATA_FILE_TITLE = "Images"
DATA_FILE_DESCRIPTION = "Barley Images"
DATA_FILE_LINK = "DOI:12444"
DATA_FILE_VERSION = "1.0.0"


@pytest.fixture(scope="function")
async def setup_data_file(
    setup_study: tuple[UUID, UUID], setup_second_study: tuple[UUID, UUID], test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID, UUID], None]:
    _, first_id = setup_study
    _, second_id = setup_second_study
    response = await test_client.post(
        "dataFile",
        json={
            "title": DATA_FILE_TITLE,
            "dataFileDescription": DATA_FILE_DESCRIPTION,
            "dataFileLink": DATA_FILE_LINK,
            "dataFileVersion": DATA_FILE_VERSION,
            "studyId": [first_id, second_id],
        },
    )
    assert response.status_code == 201
    data_file_id = response.json()["id"]
    yield data_file_id, first_id, second_id
    await test_client.delete(f"dataFile/{data_file_id}")


@pytest.fixture(scope="function")
async def update_data_file(
    setup_data_file: tuple[UUID, UUID, UUID], test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID, UUID], None]:
    data_file_id, first_id, second_id = setup_data_file
    response = await test_client.put(
        f"dataFile/{data_file_id}",
        json={
            "title": DATA_FILE_TITLE,
            "dataFileDescription": DATA_FILE_DESCRIPTION,
            "dataFileLink": DATA_FILE_LINK,
            "dataFileVersion": DATA_FILE_VERSION,
            "studyId": [first_id],
        },
    )
    assert response.status_code == 200
    yield data_file_id, first_id, second_id


@pytest.fixture(scope="function")
async def delete_first_study_get_data_file(
    setup_data_file: tuple[UUID, UUID, UUID], test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID, UUID], None]:
    data_file_id, first_id, second_id = setup_data_file
    response = await test_client.delete(f"study/{first_id}")
    assert response.status_code == 204
    yield data_file_id, first_id, second_id
