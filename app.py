
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import joblib
import os


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)
CORS(app)


# =========================================================
# LOAD ML MODEL
# =========================================================

MODEL_FILE = "final_coal_mining_risk_model.pkl"

model = joblib.load(MODEL_FILE)


# =========================================================
# LOAD DATASET
# Used for dropdown options
# =========================================================

DATASET_FILE = "coal_mining_risk_ml_dataset.csv"

df = pd.read_csv(DATASET_FILE)


# Fix None categories
df["Training_Level"] = (
    df["Training_Level"]
    .fillna("None")
)

df["Machinery_Involved"] = (
    df["Machinery_Involved"]
    .fillna("None")
)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# OPTIONS API
# =========================================================

@app.route("/options", methods=["GET"])
def options():

    # ---------------------------------------------
    # Create State -> District -> Mine hierarchy
    # ---------------------------------------------

    state_data = {}

    for state in sorted(df["State"].dropna().unique()):

        state_df = df[
            df["State"] == state
        ]

        district_data = {}

        for district in sorted(
            state_df["District"].dropna().unique()
        ):

            district_df = state_df[
                state_df["District"] == district
            ]

            mines = sorted(
                district_df["Mine_Name"]
                .dropna()
                .unique()
                .tolist()
            )

            district_data[district] = mines

        state_data[state] = district_data


    return jsonify({

        "location_data": state_data,

        "mine_types": [
            "Underground",
            "Opencast"
        ],

        "places": [
            "Face",
            "Haul Road",
            "Workshop",
            "Stockyard",
            "Shaft",
            "Excavation Area"
        ],

        "machinery": [
            "None",
            "Drill",
            "Excavator",
            "Loader",
            "Dumper",
            "Truck",
            "Heavy Earth Moving Machinery"
        ],

        "experience": [
            "<1 year",
            "1–3 years",
            "3–5 years",
            "5–10 years",
            "10+ years"
        ],

        "training": [
            "None",
            "Basic",
            "Intermediate",
            "Advanced",
            "Certified"
        ],

        "shifts": [
            "Morning",
            "Afternoon",
            "Night"
        ]
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()


        # -------------------------------------------------
        # Validate required fields
        # -------------------------------------------------

        required_fields = [
            "State",
            "District",
            "Mine_Name",
            "Mine_Type",
            "Place_of_Operation",
            "Machinery_Involved",
            "Worker_Age",
            "Worker_Experience_Years",
            "Training_Level",
            "Shift",
            "Safety_Compliance_Score"
        ]


        for field in required_fields:

            if field not in data:

                return jsonify({
                    "error": f"Missing field: {field}"
                }), 400


        # -------------------------------------------------
        # Create input dataframe
        # -------------------------------------------------

        input_data = pd.DataFrame({

            "State": [
                data["State"]
            ],

            "District": [
                data["District"]
            ],

            "Mine_Name": [
                data["Mine_Name"]
            ],

            "Mine_Type": [
                data["Mine_Type"]
            ],

            "Place_of_Operation": [
                data["Place_of_Operation"]
            ],

            "Machinery_Involved": [
                data["Machinery_Involved"]
            ],

            "Worker_Age": [
                float(data["Worker_Age"])
            ],

            "Worker_Experience_Years": [
                data["Worker_Experience_Years"]
            ],

            "Training_Level": [
                data["Training_Level"]
            ],

            "Shift": [
                data["Shift"]
            ],

            "Safety_Compliance_Score": [
                float(data["Safety_Compliance_Score"])
            ]
        })


        # -------------------------------------------------
        # Prediction
        # -------------------------------------------------

        prediction = model.predict(
            input_data
        )[0]


        # -------------------------------------------------
        # Probability
        # -------------------------------------------------

        probabilities = model.predict_proba(
            input_data
        )[0]


        classes = model.classes_


        probability_dict = {

            str(cls): round(
                float(prob) * 100,
                2
            )

            for cls, prob
            in zip(classes, probabilities)
        }


        # -------------------------------------------------
        # Highest confidence
        # -------------------------------------------------

        confidence = round(
            float(max(probabilities)) * 100,
            2
        )


        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return jsonify({

            "risk_level": prediction,

            "confidence": confidence,

            "probabilities": probability_dict

        })


    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# =========================================================
# RUN SERVER
# =========================================================



# =========================================================
# DASHBOARD PAGE
# =========================================================

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


# =========================================================
# DASHBOARD DATA API
# =========================================================

@app.route("/dashboard-data")
def dashboard_data():

    # Accident counts
    state_counts = (
        df["State"]
        .value_counts()
        .to_dict()
    )

    year_counts = (
        df["Year"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    mine_type_counts = (
        df["Mine_Type"]
        .value_counts()
        .to_dict()
    )

    shift_counts = (
        df["Shift"]
        .value_counts()
        .reindex(
            ["Morning", "Afternoon", "Night"]
        )
        .fillna(0)
        .to_dict()
    )

    training_counts = (
        df["Training_Level"]
        .value_counts()
        .reindex(
            [
                "None",
                "Basic",
                "Intermediate",
                "Advanced",
                "Certified"
            ]
        )
        .fillna(0)
        .to_dict()
    )

    machinery_counts = (
        df["Machinery_Involved"]
        .value_counts()
        .reindex(
            [
                "None",
                "Drill",
                "Excavator",
                "Loader",
                "Dumper",
                "Truck",
                "Heavy Earth Moving Machinery"
            ]
        )
        .fillna(0)
        .to_dict()
    )

    place_counts = (
        df["Place_of_Operation"]
        .value_counts()
        .to_dict()
    )

    accident_counts = (
        df["Accident_Type"]
        .value_counts()
        .to_dict()
    )

    risk_counts = (
        df["Pre_Accident_Risk_Level"]
        .value_counts()
        .reindex(
            [
                "Low",
                "Moderate",
                "High",
                "Very High"
            ]
        )
        .fillna(0)
        .to_dict()
    )

    # Safety score by risk
    safety_by_risk = (
        df.groupby(
            "Pre_Accident_Risk_Level"
        )["Safety_Compliance_Score"]
        .mean()
        .reindex(
            [
                "Low",
                "Moderate",
                "High",
                "Very High"
            ]
        )
        .fillna(0)
        .round(2)
        .to_dict()
    )

    return jsonify({

        "total_records": int(len(df)),

        "total_injured": int(
            df["Injured"].sum()
        ),

        "total_deaths": int(
            df["Death"].sum()
        ),

        "average_safety": round(
            float(
                df["Safety_Compliance_Score"].mean()
            ),
            2
        ),

        "state_counts": state_counts,

        "year_counts": year_counts,

        "mine_type_counts": mine_type_counts,

        "shift_counts": shift_counts,

        "training_counts": training_counts,

        "machinery_counts": machinery_counts,

        "place_counts": place_counts,

        "accident_counts": accident_counts,

        "risk_counts": risk_counts,

        "safety_by_risk": safety_by_risk
    })




if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
