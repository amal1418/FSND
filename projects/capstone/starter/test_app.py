import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', '12345678', 'localhost:5432', self.database_name)
        "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'hala',
            'age': '25',
            'gender': 'female'
        }
   
        self.bad_new_actor = {
            'name': 'bad',
            'age': 'aa'
        }

        self.new_movie = {
            'title': 'hi',
            'release_date': '2019'
        }

        self.bad_new_movie = {
            'title': 'bad'
        }

        self.castingassitant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRhLXlvaWNSVXpLYldoNG1JMmNtMyJ9.eyJpc3MiOiJodHRwczovL2FtYWwtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMjE1YjgzZmNmYjU3MDA2ZmVlOTk4NyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjEyOTc2MjEzLCJleHAiOjE2MTMwNjI2MTMsImF6cCI6ImpMT2xOMDQwWm9hRlFiOUM4WFFsMFFlZXFEcDNLRFRmIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.POSlaUNeDny1zctTKMDiTAJO6OCbB12B5LU9PQiYLf4S3RhvTS198UR5pAMD9YQoqkX4WRe3czMNvaQLz4_adv1lYCCEqNgFPyb9iXzFSQcA-m-29jM7dK8N9_K4KVg5Wg0JJyuJb6CY7js2MDqi8Fc9rBrOOj2PQXdy-xGNZRQ69yunumua5nALoskk8WQ6ZZpnAIBOUvGBnaOy-97y1tSpCJoAqoiL5VhClpZwCaj5NDZI1GUSSOeiIkujUWsDHeCgb1SqC-CfKZGI1OgCjKG3Sss5n7Rn7BLyhmUZea2X2uJWPOsmPzUMgwf41y__9Oqhetzn6oB4zV71MY3Ogg"
        self.castingdirector= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRhLXlvaWNSVXpLYldoNG1JMmNtMyJ9.eyJpc3MiOiJodHRwczovL2FtYWwtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMjE1YmQwOTA2MmJlMDA3MTI3MGEyYSIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjEyOTc2MjE3LCJleHAiOjE2MTMwNjI2MTcsImF6cCI6ImpMT2xOMDQwWm9hRlFiOUM4WFFsMFFlZXFEcDNLRFRmIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.tlWDrBzzgbSpeT5e6y3y73g9gKe23BpEgu1lLkJIjhDfyigM7pShhNm2cEz-pijhwMMkpgc04cujcMj3zKH15KZlerI9szOM7lQguKDwxbO2WXT0qlpplvjeQWN17Ywj7JWUML2-6hugcAo9_bsVj_ObQ1lTWiEpOrjWzdNlfS5hM8VLcOOafFEdr4IRkq0MhE4Da_dG0YgTyB80xSSlQc-Fv28f5rBDCZypZTQPSd4ZLcFLpzqtE4AztJ5UjFXw6Y4jAtTT25krfpunoOknd1pndZf1zSZBOlFna0MQXpX5WLRVGP2hkbrx9C2LYM62bpERI8enr0EiUqA_t_4ZLw"
        self.executiveproducer= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRhLXlvaWNSVXpLYldoNG1JMmNtMyJ9.eyJpc3MiOiJodHRwczovL2FtYWwtY2FzdGluZy1hZ2VuY3kudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMjE1YzAzOTA2MmJlMDA3MTI3MGEzOCIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjEyOTc2MjA2LCJleHAiOjE2MTMwNjI2MDYsImF6cCI6ImpMT2xOMDQwWm9hRlFiOUM4WFFsMFFlZXFEcDNLRFRmIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.aBKTMq9UvyginlT2YHPqyWYRtIU5z5JF4-OEGLtbeubmhaY_kkXod6p1iIjzXlRqdE6CvOGkHoDKZsY9sDElrs0ewpBUtpV7S_UKBhazHk14WmU74YQ3Yo00pPzKBiA80cyLC7JODBnXindHzy_kntQ3p5xjUMHaJDkcUndusWNgtTQL6_1TtOtDEVuevwA5w4JsFuntln_C0207Kg-cDPbbAsSVp217tTRg6hNGLoj7Utz5BfjlAkR6MDbi_2Ii_sYH4uoYurbnTd3wDEmiSWLrZOkQMrRtgYcnRxYMTwXJIZelkm0_uWC4TXsAjTlHO1SJKC_yM1xOINlG0Djimg"

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    GET test (pass & fail)

    ''' 
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer {}'.format(self.castingassitant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_404_actor_not_found(self):
        res = self.client().get('/actors/1000', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer {}'.format(self.castingassitant)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_404_movie_not_found(self):
        res = self.client().get('/movies/1000', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)})
        data = json.loads(res.data)
         
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''
    DELETE test (pass & fail)

    ''' 

    def test_delete_actor(self):
        res = self.client().delete('/actors/8', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 4)

    def test_404_if_actor_dose_not_exist_when_delete(self):
        res = self.client().delete('/actor/1000', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/8', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 4)

    def test_404_if_movie_dose_not_exist_when_delete(self):
        res = self.client().delete('/movie/1000', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''
    POST test (pass & fail)

    ''' 

    def test_create_new_actor(self):
        res = self.client().post('/actors', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)}, json=self.new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_422_if_actor_creation_failed(self):
        res = self.client().post('/actors', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)}, json=self.bad_new_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_movie(self):
        res = self.client().post('/movies', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_422_if_movie_creation_failed(self):
        res = self.client().post('/movies', headers={'Authorization': 'Bearer {}'.format(self.executiveproducer)}, json=self.bad_new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    '''
    PATCH test (pass & fail)

    ''' 

    def test_edit_actor(self):
        res= self.client().patch('/actors/7', headers={'Authorization': 'Bearer {}'.format(self.castingdirector)}, json={"age": "34"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_400_when_edit_actor(self):
        res= self.client().patch('/actors/10', headers={'Authorization': 'Bearer {}'.format(self.castingdirector)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_edit_movie(self):
        res= self.client().patch('/movies/7', headers={'Authorization': 'Bearer {}'.format(self.castingdirector)}, json={"title": "not"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_400_when_edit_movie(self):
        res= self.client().patch('/movies/10', headers={'Authorization': 'Bearer {}'.format(self.castingdirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

  

if __name__ == "__main__":
    unittest.main()
