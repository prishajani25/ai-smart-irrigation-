from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = joblib.load("irrigation_model.pkl")


# ==========================================
# CATEGORY ENCODING
# These mappings match the trained model
# ==========================================

SOIL_TYPE = {
    "Clay": 0,
    "Loamy": 1,
    "Sandy": 2,
    "Silt": 3
}

CROP_TYPE = {
    "Cotton": 0,
    "Maize": 1,
    "Potato": 2,
    "Rice": 3,
    "Sugarcane": 4,
    "Wheat": 5
}

CROP_GROWTH_STAGE = {
    "Flowering": 0,
    "Harvest": 1,
    "Sowing": 2,
    "Vegetative": 3
}

SEASON = {
    "Kharif": 0,
    "Rabi": 1,
    "Zaid": 2
}

IRRIGATION_TYPE = {
    "Canal": 0,
    "Drip": 1,
    "Rainfed": 2,
    "Sprinkler": 3
}

WATER_SOURCE = {
    "Groundwater": 0,
    "Rainwater": 1,
    "Reservoir": 2,
    "River": 3
}

MULCHING_USED = {
    "No": 0,
    "Yes": 1
}

REGION = {
    "Central": 0,
    "East": 1,
    "North": 2,
    "South": 3,
    "West": 4
}


# ==========================================
# SAFE NUMBER FUNCTION
# ==========================================

def get_number(name, default=0):

    value = request.form.get(name, "")

    try:
        return float(value)

    except (ValueError, TypeError):

        return default


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# PREDICTION
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ==================================
        # TEXT VALUES
        # ==================================

        city = request.form.get("city", "")

        region_text = request.form.get(
            "region", "Central"
        )

        soil_type_text = request.form.get(
            "soil_type", "Clay"
        )

        crop_type_text = request.form.get(
            "crop_type", "Wheat"
        )

        growth_stage_text = request.form.get(
            "crop_growth_stage",
            "Vegetative"
        )

        season_text = request.form.get(
            "season",
            "Rabi"
        )

        irrigation_type_text = request.form.get(
            "irrigation_type",
            "Drip"
        )

        water_source_text = request.form.get(
            "water_source",
            "Groundwater"
        )

        mulching_text = request.form.get(
            "mulching_used",
            "No"
        )


        # ==================================
        # NUMERIC VALUES
        # ==================================

        latitude = get_number("latitude")

        longitude = get_number("longitude")

        soil_ph = get_number("soil_ph")

        soil_moisture = get_number(
            "soil_moisture"
        )

        organic_carbon = get_number(
            "organic_carbon"
        )

        electrical_conductivity = get_number(
            "electrical_conductivity"
        )

        sunlight_hours = get_number(
            "sunlight_hours"
        )

        field_area = get_number(
            "field_area"
        )

        previous_irrigation = get_number(
            "previous_irrigation"
        )


        # ==================================
        # CONVERT CATEGORICAL VALUES
        # TO NUMBERS
        # ==================================

        soil_type = SOIL_TYPE.get(
            soil_type_text,
            0
        )

        crop_type = CROP_TYPE.get(
            crop_type_text,
            5
        )

        growth_stage = CROP_GROWTH_STAGE.get(
            growth_stage_text,
            3
        )

        season = SEASON.get(
            season_text,
            1
        )

        irrigation_type = IRRIGATION_TYPE.get(
            irrigation_type_text,
            1
        )

        water_source = WATER_SOURCE.get(
            water_source_text,
            0
        )

        mulching_used = MULCHING_USED.get(
            mulching_text,
            0
        )

        region = REGION.get(
            region_text,
            0
        )


        # ==================================
        # WEATHER VALUES
        # ==================================
        # These are currently default values.
        # They can later be connected to
        # a weather API.

        temperature = 28.0

        humidity = 65.0

        rainfall = 2.0

        wind_speed = 10.0


        # ==================================
        # CREATE MODEL INPUT
        # ==================================

        input_data = pd.DataFrame([{

            "Soil_Type":
                soil_type,

            "Soil_pH":
                soil_ph,

            "Soil_Moisture":
                soil_moisture,

            "Organic_Carbon":
                organic_carbon,

            "Electrical_Conductivity":
                electrical_conductivity,

            "Temperature_C":
                temperature,

            "Humidity":
                humidity,

            "Rainfall_mm":
                rainfall,

            "Sunlight_Hours":
                sunlight_hours,

            "Wind_Speed_kmh":
                wind_speed,

            "Crop_Type":
                crop_type,

            "Crop_Growth_Stage":
                growth_stage,

            "Season":
                season,

            "Irrigation_Type":
                irrigation_type,

            "Water_Source":
                water_source,

            "Field_Area_hectare":
                field_area,

            "Mulching_Used":
                mulching_used,

            "Previous_Irrigation_mm":
                previous_irrigation,

            "Region":
                region

        }])


        # ==================================
        # PRINT INPUT FOR DEBUGGING
        # ==================================

        print("\n==============================")
        print("MODEL INPUT")
        print("==============================")

        print(input_data)

        print("\nData Types:")

        print(input_data.dtypes)


        # ==================================
        # AI PREDICTION
        # ==================================

        prediction_number = model.predict(
            input_data
        )[0]


        print("\nPrediction Number:")

        print(prediction_number)


        # ==================================
        # CONVERT PREDICTION TO TEXT
        # ==================================
        #
        # Model classes:
        #
        # 0 = High
        # 1 = Low
        # 2 = Medium
        #

        prediction_mapping = {

            0: "High",

            1: "Low",

            2: "Medium"

        }

        prediction = prediction_mapping.get(
            int(prediction_number),
            "Unknown"
        )


        # ==================================
        # IRRIGATION RECOMMENDATION
        # ==================================

        if prediction == "High":

            recommendation = (
                "High irrigation is required. "
                "Provide sufficient water to the crop "
                "and monitor soil moisture regularly."
            )

        elif prediction == "Medium":

            recommendation = (
                "Moderate irrigation is required. "
                "Water the crop according to its "
                "growth stage and soil condition."
            )

        elif prediction == "Low":

            recommendation = (
                "Low irrigation is required. "
                "Avoid unnecessary watering and "
                "continue monitoring soil moisture."
            )

        else:

            recommendation = (
                "Unable to determine irrigation requirement."
            )


        # ==================================
        # SEND RESULT TO HTML
        # ==================================

        return render_template(

            "result.html",

            prediction=prediction,

            city=city,

            latitude=latitude,

            longitude=longitude,

            crop=crop_type_text,

            season=season_text,

            soil=soil_moisture,

            ph=soil_ph,

            temperature=temperature,

            humidity=humidity,

            rainfall=rainfall,

            wind=wind_speed,

            recommendation=recommendation

        )


    except Exception as e:

        print("\n==============================")

        print("PREDICTION ERROR")

        print("==============================")

        print(e)

        return render_template(

            "result.html",

            error=str(e)

        )


# ==========================================
# RUN FLASK
# ==========================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )