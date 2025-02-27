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
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code == 502:
            return {"error": True, "message": "API temporarily unavailable. Please try again in a few minutes."}
        elif response.status_code != 200:
            return {"error": True, "message": f"Request failed (Status {response.status_code})"}

        return response.json()

    except requests.exceptions.Timeout:
        return {"error": True, "message": "Request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}

# Main UI
st.title("IP Asset Minter")
st.markdown("Enter the details below to mint your voice IP asset:")

# Input form
name = st.text_input("Voice Character Name", placeholder="e.g., Morgan Freeman")
image_url = st.text_input("Character Image URL", placeholder="Enter the URL of the character's image")
voice_url = st.text_input("Voice Sample URL", placeholder="Enter the URL of the voice sample (MP3)")

if st.button("Mint IP Asset"):
    if all([name, image_url, voice_url]):
        try:
            with st.spinner("Minting IP asset..."):
                result = mint_ip_asset(name, image_url, voice_url)

            if "error" in result and result["error"]:
                st.error(f"❌ Minting failed: {result['message']}")
            else:
                st.success("✅ IP Asset minted successfully!")
                with st.expander("View Details"):
                    st.json(result)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please fill in all fields before minting.")

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