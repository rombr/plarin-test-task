def test_empty_list(test_client):
    response = test_client.get('/api/v1/employees')
    assert response.status_code == 200, response.json()
    assert response.json() == {
        'objects': [],
        'total': 0, 'offset': 0, 'limit': 20
    }


def test_full_list(test_client, employees_fixture):
    response = test_client.get('/api/v1/employees')
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data['total'] == 600
    assert data['offset'] == 0
    assert data['limit'] == 20


def test_pagination(test_client, employees_fixture):
    response = test_client.get('/api/v1/employees?offset=10&limit=30')
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data['total'] == 600
    assert data['offset'] == 10
    assert data['limit'] == 30


def test_bad_pagination(test_client, employees_fixture):
    response = test_client.get('/api/v1/employees?offset=10&limit=200')
    assert response.status_code == 422, response.json()


def test_gender_filter(test_client, employees_fixture):
    response = test_client.get('/api/v1/employees?gender=other')
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data['total'] == 194
    assert data['offset'] == 0
    assert data['limit'] == 20
    for item in data['objects']:
        assert item['gender'] == 'other'


def test_invalid_gender_filter(test_client, employees_fixture):
    response = test_client.get('/api/v1/employees?gender=fail')
    assert response.status_code == 422, response.json()


def test_company_filter(test_client, employees_fixture):
    '''
    Test regex filters for DB
    '''
    response = test_client.get('/api/v1/employees?company=Tw')
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data['total'] == 75
    assert data['offset'] == 0
    assert data['limit'] == 20
    for item in data['objects']:
        assert item['gender'] == 'Twitter'
