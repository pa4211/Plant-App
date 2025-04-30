import requests
import streamlit as st
from PIL import Image
import base64
import io

# Function to convert image to base64
def image_to_base64(image: Image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Function to call the Plant.id API
def get_plant_info(image_base64: str):
    api_key = st.secrets["plantid"]["api_key"]
# Replace with your actual Plant.id API key

    url = "https://api.plant.id/v2/identify"  # Correct endpoint
    headers = {
        "Api-Key": api_key,  # Use "Api-Key" header
        "Content-Type": "application/json",
    }

    data = {
        "images": [image_base64],  # Image in base64 format
        "organs": ["leaf"],  # Optional: Specify the plant organ type (e.g., leaf, flower)
        "language": "en",  # Language for plant details
        "plant_details": ["common_names", "description",  "synonyms", "edible_parts",  "scientific_name","propagation_methods", "wiki_description", "best_watering", "best_light_condition", "best_soil_type", "toxicity", "cultural_significance"],  # Details to fetch
    }

    #st.write("Sending request to the API...")  # For debugging

    try:
        # Send the POST request to the API
        response = requests.post(url, json=data, headers=headers)

        # Check for a successful request (status code 200)
        if response.status_code == 200:
            #st.write("Request successful!")  # For debugging
            plant_info = response.json()
            #st.write(plant_info)
            # If the response contains plant suggestions, extract details
            if plant_info and "suggestions" in plant_info:
                suggestion = plant_info["suggestions"][0]
                name = suggestion.get("plant_name", "Unknown plant")
                #common_names = suggestion.get("plant_details", {}).get("common_names", [])
                common_names = ", ".join(suggestion.get("plant_details", {}).get("common_names", []))
                description = suggestion.get("plant_details", {}).get("wiki_description", {}).get("value", "No description available")
                synonyms = suggestion.get("plant_details", {}).get("synonyms", [])
                #synonyms = suggestion.get("plant_details", {}).get("synonyms", [])
                #edible= suggestion.get("plant_details", {}).get("edible_parts", [])
                edible = suggestion.get("plant_details", {}).get("edible_parts", [])
                watering = suggestion.get("plant_details", {}).get("best_watering", [])
                propagation= suggestion.get("plant_details", {}).get("propagation_methods", [])#common_names_text = ", ".join(common_names) if common_names else "No common names available"
                soil = suggestion.get("plant_details", {}).get("best_soil_type", [])
                light = suggestion.get("plant_details", {}).get("best_light_condition", [])
                toxicity = suggestion.get("plant_details", {}).get("toxicity", [])
                culture = suggestion.get("plant_details", {}).get("cultural_significance", [])
                # Extract the wiki description
               
                
                    
                
                # Display plant details
                st.subheader(f"**Plant Name:** {name}")
                #st.write(f"Scientific Name: {scientific_name}")  # Now showing the scientific name
                st.write(f"**Common Names:** {common_names}")
                st.write(f"**Description:** {description}")
                st.write(f"**Synonyms:** {synonyms}")
                st.write(f"**Cultural_significance:** {culture}")
                st.write(f"**Edible Parts:** {edible}")
                st.write(f"**Toxicity:** {toxicity}")
                st.write(f"**Propagation methods:** {propagation}")
                st.subheader("Care Instructions:")
                st.write(f"**Best Watering:** {watering}")
                st.write(f"**Best Soil Types:** {soil}")
                st.write(f"**Light:** {light}")
                
                

                #st.write(care_instructions)
            else:
                st.error("No plant suggestions found in the response.")
        else:
            st.error(f"Error: Unable to get response from the API. Status Code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error with the API request: {str(e)}")
        return None

# Streamlit app layout
st.title("PlantLens")

# Upload image
uploaded_image = st.file_uploader("Upload a photo of a plant", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
    
    # When Search button is clicked
    if st.button("Know More"):
        try:
            image = Image.open(uploaded_image)
            image_base64 = image_to_base64(image)

            # Get plant info from Plant.id API
            get_plant_info(image_base64)
        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.info("Please upload an image to identify a plant.")
