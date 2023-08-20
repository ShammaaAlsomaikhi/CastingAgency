import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from app import create_app

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):

        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql+psycopg2://{}@{}/{}'.format("shammaaas", "127.0.0.1:5432", "casting_agency_test")
        setup_db(self.app, self.database_path)

        ASSISTANT_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkF6X2o1TXhQM1F1SFlialVVYkRFciJ9.eyJpc3MiOiJodHRwczovL3NoYW1tYWEtY29mZmUtc2hvcC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRkMWYwZTczNTdmOGMzNGM3MmJkNmQ3IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE2OTE1ODI0ODgsImV4cCI6MTY5MTU4OTY4OCwiYXpwIjoiSkFnSlVvakhnQ2lDTklXalY3Q1JUaElkaEhYY2N5bEMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.fQcae2ZaufX5QEDJ3d04p66HoQUvU0DUtJt6khT9lHrGkdp7bvAYcR54Pi0v3epjYOnOhXN4QQYv9CUYPHf0Rlb82obKkEu4oJtmfCuwpi_RC_9ibl7bpNFfVhYO5lDrJ9GEHQLXmKRgnFr1IWsSyPTj8vMvkTGT4SF_y2Zxf40TlvHHNU5--Q4_q900k_AMtQgQ2y-A310qcDMQc1w3GCuk-fTOgPEtZ3WXpLmcHU_8Ioth5lJkZQeUN2lnHM7sWUqea-ia5evS4n2uL8awIhJD5QFnRsszIOi5oSejlMAxUyqBpE9F1OIZ0yRDQAd5K897hKcMPvtrpZ947xj3Dw'
        PRODUCER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkF6X2o1TXhQM1F1SFlialVVYkRFciJ9.eyJpc3MiOiJodHRwczovL3NoYW1tYWEtY29mZmUtc2hvcC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRkMWZlMDM4NzRkZTc4ZDJlYTFhYzAzIiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE2OTE1ODIxNTgsImV4cCI6MTY5MTU4OTM1OCwiYXpwIjoiSkFnSlVvakhnQ2lDTklXalY3Q1JUaElkaEhYY2N5bEMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.7Z1u7cWkWVaJqR5IbGu3g6veDas4r-thzFKpBL1w1rNMIrYeu9ck79znUD_-oX9rcKcTpInNs9oAZ2-nChBgdxawTvWMepKoGrqXdHWtAGnpHc4e-6_wcBTxGhknox0eKdN3vky1VAS_O5aNcLPkkOPq8yz66UmLDmIKBieXSUrQ7IX__4rh5k4z2cpp6qH4ufsEOTrBNCax_4hCyDFM6xzvaTas5S5yo1hbPWTIa-evmoBxTewhvv50Xvuw5RosahEKEbP0J-ZrAcPylEUO9QsbZEgvUf6ANgmKEJ_6LFvhTv9fViMEOWfmKm0k8Lc8EQeCw8DDi9AEVnTWSYyGYg'
        DIRECTOR_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkF6X2o1TXhQM1F1SFlialVVYkRFciJ9.eyJpc3MiOiJodHRwczovL3NoYW1tYWEtY29mZmUtc2hvcC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRkMWZlMDM4NzRkZTc4ZDJlYTFhYzAzIiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE2OTE1ODIxNTgsImV4cCI6MTY5MTU4OTM1OCwiYXpwIjoiSkFnSlVvakhnQ2lDTklXalY3Q1JUaElkaEhYY2N5bEMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.7Z1u7cWkWVaJqR5IbGu3g6veDas4r-thzFKpBL1w1rNMIrYeu9ck79znUD_-oX9rcKcTpInNs9oAZ2-nChBgdxawTvWMepKoGrqXdHWtAGnpHc4e-6_wcBTxGhknox0eKdN3vky1VAS_O5aNcLPkkOPq8yz66UmLDmIKBieXSUrQ7IX__4rh5k4z2cpp6qH4ufsEOTrBNCax_4hCyDFM6xzvaTas5S5yo1hbPWTIa-evmoBxTewhvv50Xvuw5RosahEKEbP0J-ZrAcPylEUO9QsbZEgvUf6ANgmKEJ_6LFvhTv9fViMEOWfmKm0k8Lc8EQeCw8DDi9AEVnTWSYyGYg'

        self.assistant_auth_header = {'Authorization':
                                      'Bearer ' + ASSISTANT_TOKEN}
        self.director_auth_header = {'Authorization':
                                     'Bearer ' + DIRECTOR_TOKEN}
        self.producer_auth_header = {'Authorization':
                                     'Bearer ' + PRODUCER_TOKEN}

        self.new_movie = {
            'title':'Iron Man',
            'release_date':'02/05/2008'
        }

        self.new_actor = {
            'name':'Robert Downey Jr.',
            "age": 58,
            "gender": 'male',
            "movie_id": 4
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    


    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Movie APIs
 
    """

    def test_get_movies_success(self):
        res = self.client().get('/movies',headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    def test_get_movies_unauthorized(self):
        res = self.client().get('/movies', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    

    def test_add_movie_success(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    

    def test_add_movie_empty_obj(self):
        res = self.client().post('/movies', json=None, headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    
    def test_update_movie_success(self):
        movie = {
            'title': None,
            'release_date': '2023/08/08'
        }
        res = self.client().patch('/movies/3', json=movie,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])


    def test_update_movie_not_found(self):
        movie = {
            'title': None,
            'release_date': '2023/08/08'
        }
        res = self.client().patch('/movies/100', json=movie,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_delete_movie_success(self):
        res = self.client().delete('/movies/6',
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_movie_unprocessable(self):
    
        res = self.client().delete('/movies/100',
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # """
    # Actor APIs
 
    # """

    def test_get_actors_success_200(self):
        res = self.client().get('/actors',headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['acorts'])


    def test_get_actors_unauthorized_401(self):
        res = self.client().get('/actors', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


    def test_add_actor_success(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_add_actor_empty_obj(self):
        res = self.client().post('/actors', json=None, headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_update_actor_success(self):
        actor = {
            'name':'Robert',
            "age": None,
            "gender": None,
            "movie_id": None
        }
        res = self.client().patch('/actors/12', json=actor,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_update_actor_not_found(self):
        res = self.client().patch('/actors/100', json='',
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    
    def test_delete_actor_success(self):
        res = self.client().delete('/actors/13',
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_actor_unprocessable(self):
    
        res = self.client().delete('/actors/100',
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    
# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()
