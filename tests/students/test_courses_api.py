import pytest


@pytest.mark.django_db
def test_course_retrieve(api_client, course_factory):
    course = course_factory(_quantity=1)
    url = f'http://127.0.0.1:8000/api/v1/courses/{course[0].id}/'
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert resp.data['name'] == course[0].name


@pytest.mark.django_db
def test_course_list(api_client, course_factory):
    courses = course_factory(_quantity=10)
    url = 'http://127.0.0.1:8000/api/v1/courses/'
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert len(resp.data) == 10


@pytest.mark.django_db
def test_course_id_filter(api_client, course_factory):
    courses = course_factory(_quantity=3)
    url = 'http://127.0.0.1:8000/api/v1/courses/'
    resp = api_client.get(url, {'id': courses[0].id})
    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert resp.data[0]['id'] == courses[0].id


@pytest.mark.django_db
def test_course_name_filter(api_client, course_factory):
    courses = course_factory(_quantity=3)
    url = 'http://127.0.0.1:8000/api/v1/courses/'
    resp = api_client.get(url, {'name': courses[0].name})
    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert resp.data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_course_create(api_client):
    url = 'http://127.0.0.1:8000/api/v1/courses/'
    course = {'name': 'Python'}
    resp = api_client.post(url, course)
    assert resp.status_code == 201
    assert resp.data['name'] == course['name']


@pytest.mark.django_db
def test_course_update(api_client, course_factory):
    course = course_factory(_quantity=1)
    updated_course = {'name': 'Python'}
    url = f'http://127.0.0.1:8000/api/v1/courses/{course[0].id}/'
    resp = api_client.patch(url, updated_course)
    assert resp.status_code == 200
    assert resp.data['name'] == updated_course['name']


@pytest.mark.django_db
def test_course_delete(api_client, course_factory):
    course = course_factory(_quantity=1)
    url = f'http://127.0.0.1:8000/api/v1/courses/{course[0].id}/'
    resp = api_client.delete(url)
    assert resp.status_code == 204


@pytest.mark.parametrize(
    ['quantity', 'status_code'],
    (
            (0, 400),
            (1, 200)
    )
)
@pytest.mark.django_db
def test_max_students_per_course_validation(
        api_client, course_factory, student_factory, settings, quantity, status_code
):
    course = course_factory(_quantity=1)
    student = student_factory(_quantity=1)
    url = f'http://127.0.0.1:8000/api/v1/courses/{course[0].id}/'
    settings.MAX_STUDENTS_PER_COURSE = quantity
    resp = api_client.patch(url, {'name': 'Python', 'students': [student[0].id]})
    assert resp.status_code == status_code
