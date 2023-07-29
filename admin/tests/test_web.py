from src.web import create_app

app = create_app()
app.testing = True
client = app.test_client()


def test_home():
    response = client.get("/")
    assert b"<title>MiWebClub</title>" in response.data


def test_issues():
    response = client.get("/consultas/")
    assert b"<h1>Consultas</h1>" in response.data
