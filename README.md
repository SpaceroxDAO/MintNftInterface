# IP Asset Minter

A Streamlit web application for minting IP assets using the Crossmint API.

[https://replit.com/@adamxboyle/MintNftInterface](https://mint-nft-interface-adamxboyle.replit.app/)

## Setup Instructions

1. Make sure you have Python installed on your system
2. Clone this repository
3. Install the required packages:
   ```bash
   pip install streamlit requests
   ```

## Environment Variables

The following environment variable is required:
- `CROSSMINT_API_KEY`: Your Crossmint staging API key (starts with `sk_staging_`)

## Running the Application

To run the application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Enter the voice character name (e.g., "Morgan Freeman")
2. Provide a valid image URL for the character
3. Provide a valid URL for the voice sample (MP3 format)
4. Click "Mint IP Asset" to create your asset

## Project Structure

- `app.py`: Main application file containing the Streamlit interface and minting logic
- `.streamlit/config.toml`: Streamlit configuration file
- `README.md`: This documentation file

## Notes

- Make sure to use the staging API key for testing
- All URLs must be publicly accessible
- The application will display success/error messages clearly
- Detailed minting results can be viewed by expanding the "View Details" section
