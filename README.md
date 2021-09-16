# django-rest-api-bolapp

# open 2 tabs in console and run below commands. (Tested in Ubuntu)

# In 1st Tab
source dj_run.sh

# In 2nd Tab
source celery_run.sh

# can add, update or delete client credentials
http://127.0.0.1:8000/api/shop-detail/

# cron job url : it will sync shipments from a website for clients (Will not work now as it is accessing private api)
http://127.0.0.1:8000/api/sync-shipment/

# list of all shipments
http://127.0.0.1:8000/api/shipment/


# admin panel
http://127.0.0.1:8000/admin/
username - admin
password - @dWed@$2030
