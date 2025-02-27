import streamlit as st
import requests
import os
from datetime import datetime
import json

# Set page config
st.set_page_config(
    page_title="IP Asset Minter",
    layout="centered"
)

# Add custom CSS
st.markdown("""
    <style>
    .stAlert {
        margin-top: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def validate_url(url):
    """Validate if the provided string is a URL."""
    try:
        result = requests.head(url)
        return result.status_code == 200
    except:
        return False

def mint_ip_asset(name, image_url, voice_url):
    """Mint IP asset using the Crossmint API."""
    API_KEY = os.getenv("CROSSMINT_API_KEY")
    if not API_KEY:
        raise ValueError("API key not found in environment variables")

    url = "https://staging.crossmint.com/api/v1/ip/collections/f44f5c02-6fb4-4841-9423-e1e192a1c539/ipassets"
    
    payload = {
        "owner": "email:creator@example.com:story-testnet",
        "nftMetadata": {
            "name": f"{name} Voice License",
            "description": f"A voice sample of the iconic narration style of {name}",
            "image": image_url
        },
        "ipAssetMetadata": {
            "title": f"{name} Voice Model",
            "createdAt": datetime.now().isoformat(),
            "ipType": "voice",
            "creators": [
                {
                    "name": "AI Voice Labs",
                    "email": "creator@example.com",
                    "crossmintUserLocator": "email:creator@example.com:story-testnet",
                    "contributionPercent": 100
                }
            ],
            "media": [
                {
                    "name": f"{name} Voice Sample",
                    "url": voice_url,
                    "mimeType": "audio/mpeg"
                }
            ],
            "attributes": [
                {
                    "key": "Voice Type",
                    "value": "Narration"
                },
                {
                    "key": "Voice Character",
                    "value": name
                },
                {
                    "key": "License Type",
                    "value": "Commercial Use"
                }
            ]
        }
    }

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Main UI
st.title("IP Asset Minter")
st.markdown("Create and mint your voice IP assets with customizable properties.")

# Input form
with st.form("mint_form"):
    name = st.text_input("Voice Character Name", placeholder="e.g., John Smith")
    image_url = st.text_input("Image URL", placeholder="https://example.com/image.jpg")
    voice_url = st.text_input("Voice Sample URL", placeholder="https://example.com/voice.mp3")
    
    submit_button = st.form_submit_button("Mint IP Asset")

    if submit_button:
        # Validate inputs
        if not all([name, image_url, voice_url]):
            st.error("Please fill in all fields.")
        elif not validate_url(image_url):
            st.error("Invalid image URL. Please provide a valid URL.")
        elif not validate_url(voice_url):
            st.error("Invalid voice sample URL. Please provide a valid URL.")
        else:
            try:
                with st.spinner("Minting IP asset..."):
                    result = mint_ip_asset(name, image_url, voice_url)
                
                # Display results
                st.success("IP Asset minted successfully!")
                
                # Create expandable section for detailed results
                with st.expander("View Minting Details"):
                    st.json(result)
                
            except ValueError as e:
                st.error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred while minting: {str(e)}")

# Add helpful information
st.markdown("---")
st.markdown("""
### Instructions
1. Enter the voice character name
2. Provide a valid image URL for the character
3. Provide a valid URL for the voice sample (must be in MP3 format)
4. Click 'Mint IP Asset' to create your asset

**Note:** Make sure all URLs are accessible and valid before minting.
""")
