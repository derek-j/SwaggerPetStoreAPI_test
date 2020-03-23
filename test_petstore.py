import requests
import json
import unittest
import warnings


"""
    Program to Test a few Swagger Pet Store REST API endpoints
    http://petstore.swagger.io/
    Written in Python 3.8.1 using standard unittest library.

    Derek Johnson
    408-836-9698
    3/21/2020

    TestPlan:
     #1 Create a Pet.  Verify it.  Delete the Pet. Verify it was deleted
     #2 Create a Pet.  Verify it.  Modify the Pet (using PUT).  Verify it.  Delete the Pet.  Verify it was deleted.
     #3 Create a Pet.  Verify it.  Modify the Pet (using POST).  Verify it.  Delete the Pet.  Verify it was deleted
     #4 Create a Pet marked as sold.  Find the pet by status. Delete the pet. Verify it was deleted.
     Negative tests
     #5 Delete non-existant pet (should fail)
     #6 Find a Pet by non findable values (should fail)
"""

class TestPetStore(unittest.TestCase):

    def setUp(self):
        self.test_id = 2     # Use this id for all tests.  It's hardcoded in the body being sent it.
        self.petstore_base_url = "https://petstore.swagger.io/v2/pet"
        self.headers = {'accept': 'application/json', 'content-type': 'application/json'}

    def login(self):
        from requests.auth import HTTPBasicAuth
        r = requests.post("http://petstore.swagger.io/oauth/login", auth=HTTPBasicAuth("test", "abc123"), headers=self.headers)

    def ignoreWarnings(self):
        # For this quick test, ignore the warnings.  Normally create a separate test framework class for the
        # service calls and handle resource management to keep them separate from the testcases, to simplify I have them all here.
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    def get_pet_by_id(self, id):
        self.ignoreWarnings()
        url = self.petstore_base_url + "/" + str(id)
        print("calling GET to: {}".format(url))
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            print("Failed to get pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text))
        return r.status_code, json.loads(r.text)

    def get_find_by_status(self, status):
        self.ignoreWarnings()
        url = self.petstore_base_url + "/findByStatus?status=" + str(status)
        print("calling GET to: {} by status: {}".format(url, status))
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            print("Failed to get pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text))
        return r.status_code, json.loads(r.text)

    def post_pet(self, data):
        self.ignoreWarnings()
        print("Calling POST with data={}".format(data))
        r = requests.post(self.petstore_base_url, data=data, headers=self.headers)
        if r.status_code != 200:
           print("Failed to POST pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text))
        return r.status_code, json.loads(r.text)

    def put_pet(self, data):
        self.ignoreWarnings()
        print("Calling PUT with data={}".format(data))
        r = requests.put(self.petstore_base_url, data=data, headers=self.headers)
        if r.status_code != 200:
            print("Failed to PUT pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text))
        return r.status_code, json.loads(r.text)

    def delete_pet(self, id):
        self.ignoreWarnings()
        url = self.petstore_base_url + "/" + str(id)
        print("calling DELETE to: {}".format(url))
        r = requests.delete(url, headers=self.headers)
        if r.status_code != 200:
            print("Failed to DELETE pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text))
        return r.status_code, json.loads(r.text)

    def does_pet_with_id_exist(self, id):
        c, r = self.get_pet_by_id(id)
        if c == 200:
            return True
        else:
            return False

    # -----------------------------------------------------------------------------------------------------------------
    #   Test Cases
    # -----------------------------------------------------------------------------------------------------------------

    def test_01_create_delete_pet(self):
        """
            TEST Creating a Pet, verifying the pet was created, deleting the Pet and verifying the Pet was deleted.
            Steps:
            - Post pet
            - Get / Verify it was posted
            - Delete
            - Get / Verify it was deleted
        """
        body = "{\"id\": 2, \"category\": {\"id\": 1, \"name\": \"Samoyed\"}, \"name\": \"Pinky\", \"photoUrls\": [\"string\"], \"tags\": [{\"id\": 1, \"name\": \"Female\"}], \"status\": \"available\"}"
        c, r = self.post_pet(body)
        assert (c == 200), "Failed to POST pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["category"]["name"] == "Samoyed")

        # Verify that the Pet was added by checking it's ID and Name
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 200), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["id"] == 2)
        assert (r["name"] == "Pinky")

        # Delete the Pet
        c, r = self.delete_pet(self.test_id)
        assert (c == 200), "Faled to DELETE pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)

        # Verify the pet has been deleted
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 404), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["type"] == "error")
        assert (r["message"] == "Pet not found")

    def test_02_create_modify_put_delete_pet(self):
        """
            TEST Creating a Pet, verifying the pet was created,
            Modify the same pet with a PUT, verifying the pet was modified,
            deleting the Pet and verifying the Pet was deleted.
            Steps:
            - Post pet
            - Get / Verify it was posted
            - Modify pet  (Using PUT)
            - Get / Verify it was modified
            - Delete
            - Get / Verify it was deleted
        """
        body = "{\"id\": 2, \"category\": {\"id\": 1, \"name\": \"Samoyed\"}, \"name\": \"Pinky\", \"photoUrls\": [\"string\"], \"tags\": [{\"id\": 1, \"name\": \"Female\"}], \"status\": \"available\"}"
        c, r = self.post_pet(body)
        assert (c == 200), "Failed to POST pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["name"] == "Pinky"), "Failed to POST pet. \nResponse Code: {} \nResponse Body {}".format(r.status_code,
                                                                                                       r.text)
        assert (r["category"]["name"] == "Samoyed")

        # Verify that the Pet was added by checking it's ID and Name
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 200), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["id"] == 2)
        assert (r["name"] == "Pinky")
        assert (r["status"] == "available")

        # Modify the Pet, mark it as sold!
        body = "{\"id\": 2, \"category\": {\"id\": 1, \"name\": \"Samoyed\"}, \"name\": \"Pinky\", \"photoUrls\": [\"string\"], \"tags\": [{\"id\": 1, \"name\": \"Female\"}], \"status\": \"sold\"}"
        c, r = self.put_pet(body)
        assert (c == 200), "Failed to PUT pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["status"] == "sold")

        # Verify that the Pet is now sold
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 200), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["id"] == self.test_id)
        assert (r["name"] == "Pinky")
        assert (r["status"] == "sold")

        # Delete the Pet
        c, r = self.delete_pet(self.test_id)
        assert (c == 200), "Faled to DELETE pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)

        # Verify the pet has been deleted
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 404), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["type"] == "error")
        assert (r["message"] == "Pet not found")

    def test_03_create_modify_post_delete_pet(self):
        """
            TEST Creating a Pet, verifying the pet was created,
            Modify the same pet with a POST, verifying the pet was modified,
            deleting the Pet and verifying the Pet was deleted.
            Steps:
            - Post pet
            - Get / Verify it was posted
            - Modify pet  (Using POST)
            - Get / Verify it was modified
            - Delete
            - Get / Verify it was deleted
        """
        body = "{\"id\": 2, \"category\": {\"id\": 1, \"name\": \"Samoyed\"}, \"name\": \"Pinky\", \"photoUrls\": [\"string\"], \"tags\": [{\"id\": 1, \"name\": \"Female\"}], \"status\": \"available\"}"
        c, r = self.post_pet(body)
        assert (c == 200), "Failed to POST pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["name"] == "Pinky"), "Failed to POST pet. \nResponse Code: {} \nResponse Body {}".format(r.status_code,
                                                                                                       r.text)
        assert (r["category"]["name"] == "Samoyed")

        # Verify that the Pet was added by checking it's ID and Name
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 200), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["id"] == self.test_id)
        assert (r["name"] == "Pinky")
        assert (r["status"] == "available")

        # Modify the Pet, mark it as sold!
        body = "{\"id\": 2, \"category\": {\"id\": 1, \"name\": \"Samoyed\"}, \"name\": \"Nala\", \"photoUrls\": [\"string\"], \"tags\": [{\"id\": 1, \"name\": \"Female\"}], \"status\": \"sold\"}"
        c, r = self.post_pet(body)
        assert (c == 200), "Failed to PUT pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["status"] == "sold")
        assert (r["name"] == "Nala")

        # Verify that the Pet is now sold
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 200), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["id"] == 2)
        assert (r["name"] == "Nala")
        assert (r["status"] == "sold")

        # Delete the Pet
        c, r = self.delete_pet(self.test_id)
        assert (c == 200), "Faled to DELETE pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)

        # Verify the pet has been deleted
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 404), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["type"] == "error")
        assert (r["message"] == "Pet not found")

    def test_04_create_findByStatus_delete_pet(self):
        """
            TEST Creating a Pet, verifying the pet was created, Find the Pet by Status, deleting the Pet and verifying the Pet was deleted.
            Steps:
            - Post pet
            - Get / Verify it was posted
            - FindByStatus
            - Delete
            - Get / Verify it was deleted
        """
        body = "{\"id\": 2, \"category\": {\"id\": 1, \"name\": \"Samoyed\"}, \"name\": \"Pinky\", \"photoUrls\": [\"string\"], \"tags\": [{\"id\": 1, \"name\": \"Female\"}], \"status\": \"sold\"}"
        c, r = self.post_pet(body)
        assert (c == 200), "Failed to POST pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["category"]["name"] == "Samoyed")

        # Verify that the Pet was added by checking it's ID and Name
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 200), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["id"] == 2)
        assert (r["name"] == "Pinky")

        # Find the pet by name and status
        # url_find_by_status_sold = self.petstore_base_url + "/findByStatus/?status=sold"
        c, r = self.get_find_by_status("sold")
        assert (c == 200), "Failed to POST pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        found = False
        for i in r:
            try:
                if i["name"] == "Pinky" and i["status"] == "sold":
                    found = True
            except KeyError as error:
                pass  # Ignore errors, some won't have a name?
        assert found == True, "Failed to find the Pinky and sold pet"

        # Delete the Pet
        c, r = self.delete_pet(self.test_id)
        assert (c == 200), "Faled to DELETE pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)

        # Verify the pet has been deleted
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 404), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["type"] == "error")
        assert (r["message"] == "Pet not found")

    def test_05_delete_non_existant_pet(self):
        """
            TEST deleting a Pet which doesn't exist and verifying the Pet was deleted.
            Steps:
            - Delete
            - Get / Verify it was deleted
        """
        # Delete the Pet
        try:
            # Make sure pet doesn't already exist.
            if self.does_pet_with_id_exist(self.test_id):
                c, r = self.delete_pet(self.test_id)

            # Now test deleting a pet which doesn't exist
            c, r = self.delete_pet(self.test_id)
            assert (c == 404), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code,
                                                                                                    r.text)
            assert (r["type"] == "error")
            assert (r["message"] == "Pet not found")
        except:
            pass

        # Verify the pet has been deleted
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 404), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["type"] == "error")
        assert (r["message"] == "Pet not found")

    def test_06_create_findByStatus_non_value_delete_pet(self):
        """
            TEST Creating a Pet, verifying the pet was created, Find the Pet by Status, deleting the Pet and verifying the Pet was deleted.
            Steps:
            - Post pet
            - Get / Verify it was posted
            - FindByStatus
            - Delete
            - Get / Verify it was deleted
        """
        body = "{\"id\": 2, \"category\": {\"id\": 1, \"name\": \"Samoyed\"}, \"name\": \"Pinky\", \"photoUrls\": [\"string\"], \"tags\": [{\"id\": 1, \"name\": \"Female\"}], \"status\": \"sold\"}"
        c, r = self.post_pet(body)
        assert (c == 200), "Failed to POST pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["category"]["name"] == "Samoyed")

        # Verify that the Pet was added by checking it's ID and Name
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 200), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["id"] == 2)
        assert (r["name"] == "Pinky")

        # Find the pet by name and status
        # url_find_by_status_sold = self.petstore_base_url + "/findByStatus/?status=sold"
        c, r = self.get_find_by_status("NON_VALUE")
        assert (c == 200), "Failed to POST pets. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (len(r) == 0), "Expected an empty list of found items.  instead got:  {}".format(r)

        # Delete the Pet
        c, r = self.delete_pet(self.test_id)
        assert (c == 200), "Faled to DELETE pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)

        # Verify the pet has been deleted
        c, r = self.get_pet_by_id(self.test_id)
        assert (c == 404), "Failed to GET pets by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["type"] == "error")
        assert (r["message"] == "Pet not found")

    # Dont run this with unittest runner.
    def tst_cases(self):
        self.test_01_create_delete_pet()
        self.test_02_create_modify_put_delete_pet()
        self.test_03_create_modify_post_delete_pet()
        self.test_04_create_findByStatus_delete_pet()
        self.test_05_delete_non_existant_pet()
        self.test_06_create_findByStatus_non_value_delete_pet()
    # test_cases()

if __name__ == '__main__':
    unittest.main()

