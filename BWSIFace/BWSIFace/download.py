from dlib_models import download_model, download_predictor
from dlib_models import load_dlib_models
from dlib_models import models
download_model()
download_predictor()
# this loads the dlib models into memory. You should only import the models *after* loading them.
# This does lazy-loading: it doesn't do anything if the models are already loaded.

load_dlib_models()
face_detect = models["face detect"]
face_rec_model = models["face rec"]
shape_predictor = models["shape predict"]

face_rec_model.download_predictor()
face_rec_model.download_predictor()
