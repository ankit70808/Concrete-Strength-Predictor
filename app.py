from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
import pickle
import traceback

app = FastAPI()


try:
    with open('concrete_strength_pipeline.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print("FAILED TO LOAD MODEL:", e)
    model = None

@app.post("/predict")
def predict(data: dict = Body(...)):
    if model is None:
        return {'error': 'The model file (.pkl) failed to load on server start.'}
    
    try:
        
        c = float(data.get('cement', 0) or 0)
        bf = float(data.get('blastFurnace', 0) or 0)
        fa = float(data.get('flyAsh', 0) or 0)
        w = float(data.get('water', 0) or 0)
        sp = float(data.get('superplastic', 0) or 0)
        co = float(data.get('coarse', 0) or 0)
        fi = float(data.get('fine', 0) or 0)
        a = float(data.get('age', 0) or 0)

        tot_agg = co + fi
        binder = c + bf + fa
        liquid = w + sp

      
        features = {
            'age_sqrt': np.sqrt(a) if a >= 0 else 0,
            'total_aggregates': tot_agg,
            'aggregate_cement_ratio': tot_agg / c if c > 0 else 0,
            'slag_cement_ratio': bf / c if c > 0 else 0,
            'ash_cement_ratio': fa / c if c > 0 else 0,
            'cement_age_interaction': c * a,
            'water_binder_ratio': w / binder if binder > 0 else 0,
            'coarse_fine_ratio': co / fi if fi > 0 else 0,
            'effective_cement': binder,
            'solids_liquids_ratio': (binder + tot_agg) / liquid if liquid > 0 else 0,
            'sp_to_liquid_ratio': sp / liquid if liquid > 0 else 0
        }

        df = pd.DataFrame([features])
        prediction = model.predict(df)[0]
        
        return {'prediction': round(float(prediction), 2)}

    except Exception as e:
    
        print(traceback.format_exc())
        return {'error': str(e)}


app.mount("/", StaticFiles(directory=".", html=True), name="static")