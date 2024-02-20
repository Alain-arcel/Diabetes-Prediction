import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import joblib
import numpy as np
import pandas as pd

# Charger le modèle entraîné
model = joblib.load(r"C:\Users\alain\OneDrive\Documents\Projet personnel\Prédiction du diabète\Random Forest.pkl")

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Styles CSS pour améliorer l'apparence
styles = {
    'container': {
        'margin': 'auto',
        'width': '50%',
        'padding': '20px',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
        'background-color': '#f9f9f9'
    },
    'input-label': {
        'margin-top': '10px',
        'font-weight': 'bold',
        'color': '#555'  # gris pour les étiquettes
    },
    'input-field': {
        'margin-bottom': '10px',
        'color': '#33a',  # bleu clair pour les valeurs d'entrée
        'margin-right': '20px'  # ajout d'un espace à droite
    },
    'predict-button': {
        'margin-top': '20px',
        'background-color': '#8bc34a',  # vert clair pour le bouton
        'color': 'white',
        'padding': '10px 20px',
        'text-align': 'center',
        'text-decoration': 'none',
        'display': 'inline-block',
        'font-size': '16px',
        'border-radius': '5px',
        'cursor': 'pointer',
        'border': 'none',
        'box-shadow': '0 2px 4px 0 rgba(0, 0, 0, 0.1)',  # ombre légère
        'transition': 'background-color 0.3s'  # transition subtile
    },
    'predict-button:hover': {
        'background-color': '#6fa541'  # couleur légèrement plus foncée au survol
    },
    'prediction-output': {
        'margin-top': '20px',
        'font-size': '18px'
    }
}

# Définir la mise en page du tableau de bord
app.layout = html.Div([
    html.H1("Prédiction du diabète", style={'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Label("Nombre de grossesse", style=styles['input-label']),
            dcc.Input(id="number-of-children-input", type="number", value=None, min=0, max=20, step=1, style=styles['input-field']),
            html.Label("Glucose plasmatique", style=styles['input-label']),
            dcc.Input(id="glucose-input", type="number", value=None, min=0, max=300, step=1, style=styles['input-field']),
            html.Label("Tension diastolique", style=styles['input-label']),
            dcc.Input(id="blood-pressure-input", type="number", value=None, min=0, max=200, step=1, style=styles['input-field']),
            html.Label("Épaisseur du pli cutané du triceps", style=styles['input-label']),
            dcc.Input(id="skin-thickness-input", type="number", value=None, min=0, max=100, step=1, style=styles['input-field']),
            html.Label("Insuline sérique", style=styles['input-label']),
            dcc.Input(id="insulin-input", type="number", value=None, min=0, max=900, step=0.1, style=styles['input-field']),
            html.Label("IMC", style=styles['input-label']),
            dcc.Input(id="bmi-input", type="number", value=None, min=0, max=70, step=0.1, style=styles['input-field']),
            html.Label("Fonction pédigrée de diabète", style=styles['input-label']),
            dcc.Input(id="family-history-input", type="number", value=None, min=0.078, max=3.00, step=0.001, style=styles['input-field']),
            html.Label("Âge (ans)", style=styles['input-label']),
            dcc.Input(id="age-input", type="number", value=None, min=0, max=190, step=1, style=styles['input-field']),
            html.Button('Prédire', id='predict-button', n_clicks=0, style=styles['predict-button'])
        ], style=styles['container']),
        html.Div(id='prediction-output', style=styles['prediction-output'])
    ])
])

# Définir la fonction de rappel
@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [
        Input("glucose-input", "value"),
        Input("blood-pressure-input", "value"),
        Input("skin-thickness-input", "value"),
        Input("insulin-input", "value"),
        Input("bmi-input", "value"),
        Input("family-history-input", "value"),
        Input("age-input", "value"),
        Input("number-of-children-input", "value")
    ]
)
def predict_diabetes(n_clicks, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Pregnancies):
    if n_clicks > 0:
        # Prétraiter les données d'entrée
        features = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        features_df = pd.DataFrame(features, columns=feature_names)
        prediction = model.predict(features_df)
        if prediction[0] == 1:
            return "Fort risque de diabète"
        else:
            return "Risque de diabète faible"
    else:
        return ""

# Exécuter l'application Dash
if __name__ == '__main__':
    app.run_server(debug=True)
