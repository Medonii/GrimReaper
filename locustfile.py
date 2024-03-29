from locust import HttpUser,task,between
import random
import string


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsb2N1c3Rlc3QiLCJzY29wZXMiOltdLCJleHAiOjE2NzQzODQyNjZ9.trXB6hzlCPJmhTvY1j8wXiv_8sMBzb9zX-odkGw_7kY"

class AppUser(HttpUser):
    wait_time = between(2,5)

    

    @task
    def get_users(self):
        self.client.get("/users/", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })

    @task
    def get_user(self):
        self.client.get("/users/1", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })

    
    @task 
    def post_user(self):
        nickname = ''.join(random.choices(string.ascii_lowercase, k=5))
        password = ''.join(random.choices(string.ascii_lowercase, k=5))
        self.client.post("/users/create", json= 
        {
        "nickname": nickname,
        "password": password
        }, headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
        })

    @task 
    def put_user(self):
        nickname = ''.join(random.choices(string.ascii_lowercase, k=5))
        password = ''.join(random.choices(string.ascii_lowercase, k=5))
        self.client.put("/users/update_user/1", json=
        {
        "nickname": nickname,
        "password": password
        }, headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
        })


    @task
    def post_token(self):
        d = {'username': 'locustest', 'password': 'locustest'}
        self.client.post("/users/token/", data=d)

    @task
    def post_register(self):
        nickname = ''.join(random.choices(string.ascii_lowercase, k=5))
        password = ''.join(random.choices(string.ascii_lowercase, k=5))
        d = {'username': nickname, 'password': password}
        self.client.post("/users/register/", data=d)


    @task
    def get_ambulances(self):
        self.client.get("/ambulances/", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })


    @task
    def get_ambulance(self):
        self.client.get("/ambulances/5", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })


    @task
    def post_ambulance(self):
        tag = ''.join(random.choices(string.ascii_lowercase, k=5))
        type = ''.join(random.choices(string.ascii_lowercase, k=1))
        
        self.client.post("/ambulances/create", json=
        {
        "tag": tag,
        "type": "s",
        "position": "dluga 10, Krakow"
        }, headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
        })

    @task 
    def put_ambulance_update(self):
        tag = ''.join(random.choices(string.ascii_lowercase, k=5))
        type = ''.join(random.choices(string.ascii_lowercase, k=1))
        
        self.client.put("/ambulances/update_ambulance/5", json=
        {
        "tag": tag,
        "type": "s",
        "position": "dluga 5, Krakow"
        }, headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
        })

    @task 
    def put_ambulance_set_busy(self):
        self.client.put("/ambulances/set_busy_status/5", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })

    @task 
    def put_ambulance_make_available(self):
        self.client.put("/ambulances/make_available/5", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })
    
    @task 
    def put_ambulance_exclude(self):
        self.client.put("/ambulances/exclude/5", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })


    @task
    def get_patients(self):
        self.client.get("/patients/", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })

    @task
    def get_patient(self):
        self.client.get("/patients/5/", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })

    @task
    def post_patient(self):
        name = ''.join(random.choices(string.ascii_lowercase, k=5))
        type = ''.join(random.choices(string.ascii_lowercase, k=1))
        
        self.client.post("/patients/create", json=
        {
        "name": name,
        "people": 2,
        "address": "dluga 5, Krakow",
        "type": "s",
        }, headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
        })

    @task 
    def put_patient_update(self):
        name = ''.join(random.choices(string.ascii_lowercase, k=5))
        
        self.client.put("/patients/update/5", json=
        {
        "name": name,
        "people": 2,
        "address": "dluga 5, Krakow",
        "type": "S",
        }, headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
        })

    @task 
    def put_patient_suggest(self):
        self.client.put("/patients/suggest/23", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })

    @task
    def put_patient_accept(self):
        self.client.put("/patients/accept/23", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })

    # @task 
    # def put_patient_reject(self):
    #     self.client.put("/patients/reject/5", headers= {
    #                     "Content-Type": "application/json",
    #                     'Authorization': "Bearer " + token,
    #                 })

    @task 
    def put_patient_start(self):
        self.client.put("/patients/start/5", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })


    @task 
    def put_patient_close(self):
        self.client.put("/patients/close/5", headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })


    