import firebase_admin
from firebase_admin import credentials

cred = credentials.certificate("Path/to/serviceAccountkey.json")
firebase_admin.initialize_app(cred)