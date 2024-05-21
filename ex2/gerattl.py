import csv
import json

# Create a dictionary to store disease descriptions
disease_descriptions = {}
disease_treatments = {}

# Read the disease descriptions
with open('Disease_Description.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header
    for row in csv_reader:
        disease_name = row[0].replace(" ", "_")  # Replace spaces with underscores
        disease_descriptions[disease_name] = row[1]

# Read the disease symptoms and create TTL content
with open('Disease_Syntoms.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header
    ttl = ""
    for row in csv_reader:
        disease_name = row[0].replace(" ", "_")  # Replace spaces with underscores
        description = disease_descriptions.get(disease_name, '').replace('"', '')
        ttl += f":{disease_name} a :Disease ;\n"
        ttl += f"    :hasDescription \"{description}\" ;\n"
        
        # Assuming symptoms are in the second column and are separated by commas
        symptoms = row[1].split(',')
        for i, symptom in enumerate(symptoms):
            symptom_name = symptom.strip().replace(" ", "_")
            ttl += f"    :hasSymptom :{symptom_name}"
            ttl += " ;\n" if i != len(symptoms) - 1 else " .\n"  # Add a semicolon if it's not the last symptom, otherwise add a period

# Read the disease treatments
with open('Disease_Treatment.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header
    for row in csv_reader:
        disease_name = row[0].replace(" ", "_")  # Replace spaces with underscores
        # Assuming treatments are in the second column and are separated by commas
        treatments = row[1].split(',')
        disease_treatments[disease_name] = [treatment.strip().replace(" ", "_") for treatment in treatments]

# Add treatments to the TTL content
for disease_name, treatments in disease_treatments.items():
    ttl += f":{disease_name}"
    for i, treatment_name in enumerate(treatments):
        ttl += f" :hasTreatment :{treatment_name} ;\n"
        ttl += f":{treatment_name} a :Treatment .\n"

# Read the patient data
with open('pg54707.json', 'r') as file:
    data = json.load(file)

# Create TTL content for patients
for i, patient in enumerate(data):
    patient_id = f"Patient_{i+1}"  # Create a unique ID for each patient
    patient_name = patient['nome'].replace(" ", "_")  # Replace spaces with underscores
    ttl += f":{patient_id} a :Patient ;\n"
    ttl += f"    :hasName \"{patient_name}\" ;\n"
    
    # Symptoms are in a list
    symptoms = patient['sintomas']
    for j, symptom in enumerate(symptoms):
        symptom_name = symptom.strip().replace(" ", "_")
        ttl += f"    :hasSymptom :{symptom_name}"
        ttl += " ;\n" if j != len(symptoms) - 1 else " .\n"  # Add a semicolon if it's not the last symptom, otherwise add a period

# Write the TTL data to a file
with open('med_doentes.ttl', 'w', encoding='utf-8') as output_file:
    output_file.write(ttl)

print("Turtle data has been written to 'med_doentes.ttl'.")