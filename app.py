import streamlit as st
import requests
import os
from datetime import datetime

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

    # Debug logging
    st.write("Debug: Using API key starting with:", API_KEY[:12] + "...")

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

    # Debug logging
    st.write("Debug: Making request to:", url)
    st.write("Debug: Request payload:", payload)

    try:
        response = requests.post(url, json=payload, headers=headers)
        st.write("Debug: Response status code:", response.status_code)
        st.write("Debug: Response headers:", dict(response.headers))

        # Get raw response content
        raw_content = response.text
        st.write("Debug: Raw response:", raw_content)

        # Try to parse JSON
        if response.content:
            return response.json()
        else:
            return {"error": True, "message": "Empty response from server"}

    except requests.exceptions.RequestException as e:
        return {"error": True, "message": f"Request failed: {str(e)}"}
    except ValueError as e:
        return {"error": True, "message": f"Failed to parse response: {str(e)}, Raw response: {raw_content}"}

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
                st.error(f"Error: {result['message']}")
            else:
                st.success("✅ IP Asset minted successfully!")
                st.subheader("Minting Results:")
                st.json(result)

        except Exception as e:
            st.error(f"Error during minting: {str(e)}")
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