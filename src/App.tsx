import { useState } from 'react'
import './App.css'

interface MintResponse {
  error?: boolean;
  message?: string;
  [key: string]: any;
}

function App() {
  const [name, setName] = useState('')
  const [imageUrl, setImageUrl] = useState('')
  const [voiceUrl, setVoiceUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<MintResponse | null>(null)

  const mintIpAsset = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)

    const payload = {
      owner: 'email:creator@example.com:story-testnet',
      nftMetadata: {
        name: `${name} Voice License`,
        description: `A voice sample of the iconic narration style of ${name}`,
        image: imageUrl
      },
      ipAssetMetadata: {
        title: `${name} Voice Model`,
        createdAt: new Date().toISOString(),
        ipType: 'voice',
        creators: [
          {
            name: 'AI Voice Labs',
            email: 'creator@example.com',
            crossmintUserLocator: 'email:creator@example.com:story-testnet',
            contributionPercent: 100
          }
        ],
        media: [
          {
            name: `${name} Voice Sample`,
            url: voiceUrl,
            mimeType: 'audio/mpeg'
          }
        ],
        attributes: [
          {
            key: 'Voice Type',
            value: 'Narration'
          },
          {
            key: 'Voice Character',
            value: name
          },
          {
            key: 'License Type',
            value: 'Commercial Use'
          }
        ]
      },
      licenseTerms: [{
        type: 'commercial-use',
        terms: {
          defaultMintingFee: 100,
          currency: '0x1514000000000000000000000000000000000000'
        }
      }]
    }

    try {
      const response = await fetch(
        'https://staging.crossmint.com/api/v1/ip/collections/f44f5c02-6fb4-4841-9423-e1e192a1c539/ipassets',
        {
          method: 'POST',
          headers: {
            'X-API-KEY': import.meta.env.VITE_CROSSMINT_API_KEY,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        }
      )

      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({
        error: true,
        message: error instanceof Error ? error.message : 'An error occurred'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>IP Asset Minter</h1>
      <form onSubmit={mintIpAsset}>
        <div className="form-group">
          <label htmlFor="name">Voice Character Name</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g., Morgan Freeman"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="imageUrl">Character Image URL</label>
          <input
            id="imageUrl"
            type="url"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
            placeholder="Enter the URL of the character's image"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="voiceUrl">Voice Sample URL</label>
          <input
            id="voiceUrl"
            type="url"
            value={voiceUrl}
            onChange={(e) => setVoiceUrl(e.target.value)}
            placeholder="Enter the URL of the voice sample (MP3)"
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Minting...' : 'Mint IP Asset'}
        </button>
      </form>

      {result && (
        <div className={`result ${result.error ? 'error' : 'success'}`}>
          {result.error ? (
            <p>❌ Minting failed: {result.message}</p>
          ) : (
            <>
              <p>✅ IP Asset minted successfully!</p>
              <details>
                <summary>View Details</summary>
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </details>
            </>
          )}
        </div>
      )}
    </div>
  )
}

export default App
