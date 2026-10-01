import pandas as pd
import yaml
import json

#lager variabler for filene
xlsx_file = "sensors.xlsx"
csv_file = "calibrations.csv"
yml_file = "config.yml"

#leser inn data fra Excel og CSV filer
xlsxdata = pd.read_excel(xlsx_file)
csvdata = pd.read_csv(csv_file)

#leser inn YAML filen
with open(yml_file, "r") as f:
    config = yaml.safe_load(f)

#mergerer dataene basert på sensor_id
merged = pd.merge(xlsxdata, csvdata, on="sensor_id", how="left")

#henter ut variabler fra YAML filen
max_days = config["max_days_since_calibration"]
output_file = config["output_file"]

#finner sensorer som har gått over max_days siden siste kalibrering
overdue = merged[merged["days_since_calibration"] > max_days]
records = overdue[["sensor_id", "lab_room", "owner", "days_since_calibration"]].to_dict(orient="records")

#skriver ut resultatene til en JSON fil
with open(output_file, "w") as f:
    json.dump(records, f, indent=2)