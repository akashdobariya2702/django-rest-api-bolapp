import requests, base64
import json

# from celery import task
from celery import Celery
from ratelimit import limits, sleep_and_retry
from urllib.parse import urlencode, quote_plus
from datetime import datetime, date, time, timedelta
from requests.auth import HTTPBasicAuth

app = Celery()

CLIENT_CONFIG = {
        "basic_auth_token" : "https://login.website_xyz.com/token?grant_type=client_credentials",
        "get_shipments" : "https://api.website_xyz.com/retailer/shipments",
    }

class Client():
    client_id = None
    client_secret = None
    auth_response = None
    expires_time = None
    access_token = None
    base_headers = {
        'Authorization' : '',
        # 'Accept'        : 'application/json'
        'Accept'        : 'application/vnd.retailer.v3+json'
    }

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        if self.access_token is None:
            self.get_auth()

    def get_auth(self):
        r = requests.post(CLIENT_CONFIG["basic_auth_token"], auth=HTTPBasicAuth(self.client_id, self.client_secret))
        # print(r.request.headers['Authorization'])
        self.auth_response = r.json()
        print("self.auth_response = %s" % (str(self.auth_response)))
        self.expires_time = datetime.now() + timedelta(seconds=self.auth_response["expires_in"])

        self.access_token = self.auth_response["access_token"]
        self.base_headers["Authorization"] = "Bearer "+self.access_token

    def check_expiry(self):
        print("self.expires_time = %s" % (str(self.expires_time)))
        print("datetime.now = %s" % (str(datetime.now())))
        if self.expires_time is None or self.expires_time <= datetime.now():
            self.get_auth()

    @sleep_and_retry
    @limits(calls=14, period=60) # period in seconds
    def get(self, request_type, id):
        self.check_expiry()
        url = CLIENT_CONFIG[request_type] + '/' + str(id)
        print(url)

        i = 0
        while True:
            try:
                print("while i = %s" % (str(i)))
                i += 1
                response = requests.get(url, headers=self.base_headers)
                break
            except Exception as e:
                print("while Exception e = %s" % (str(e)))
                # for connection rest by peer handling if occured
                import time
                time.sleep(0.1)
                if i >= 5:
                    break
        return response

    @sleep_and_retry
    @limits(calls=7, period=60)
    def search(self, request_type, payload={}):
        #for lists of data request .get()
        self.check_expiry()
        params = urlencode(payload)#convert json to url params
        url = CLIENT_CONFIG[request_type] + "?" + str(params)
        print(url)
        response = requests.get(url, headers=self.base_headers)
        return response

@app.task
def sync_client_shipment_data(client_id, client_secret, client_pk):
    from api.serializers import ShipmentSerializer

    cres = Client(client_id, client_secret)
    for fulfilment_method in ["FBR", "FBB"]:
        page = 1
        while page > 0:
            basic_info = cres.search("get_shipments", {"page":page, "fulfilment-method":fulfilment_method}).json()
            # print("basic_info = %s" % (str(basic_info)))
            print("page = %s" % (str(page)))
            if "shipments" in basic_info:
                all_shipments = basic_info["shipments"]
                if len(all_shipments) == 50:
                    page += 1
                else:
                    page = 0
                for shipment in all_shipments:
                    complete_info = cres.get("get_shipments", shipment["shipmentId"]).json()
                    # print(json.dumps(complete_info))
                    # import time
                    # time.sleep(100) #in second
                    jsondata = {
                        "shipment_id" : shipment["shipmentId"],
                        "shipment_date" : shipment["shipmentDate"],
                        "transport_id" : shipment["transport"]["transportId"],
                        "basic_info" : str(json.dumps(shipment)),
                        "complete_info" : str(json.dumps(complete_info)),
                        "fulfilment_method" : fulfilment_method,
                        "shop_detail" : client_pk,
                    }
                    # print(jsondata)
                    ship_ser = ShipmentSerializer(data=jsondata)
                    if ship_ser.is_valid():
                        ship_ser.save()
                    else:
                        print("ship_ser.errors = %s" % (str(ship_ser.errors)))
            else:
                page = 0
    return True

@app.task
def sync_shipment_data():
    from api.models import ShopDetail

    clients = ShopDetail.objects.all()
    for client in clients:
        r = sync_client_shipment_data.apply_async((client.client_id, client.client_secret, client.pk), expires=datetime.now() + timedelta(days=2))
        print("sync_shipment_data r = %s" % (str(r)))

    return True
