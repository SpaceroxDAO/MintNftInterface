import dotenv from 'dotenv';
dotenv.config();

const API_KEY = process.env.CROSSMINT_API_KEY;

async function main() {
    // Create IP Asset
    const createResponse = await fetch("https://staging.crossmint.com/api/v1/ip/collections/f44f5c02-6fb4-4841-9423-e1e192a1c539/ipassets", {
        method: "POST",
        headers: {
            "X-API-KEY": API_KEY || '',
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            owner: 'email:creator@example.com:story-testnet',
            nftMetadata: {
                name: 'Morgan Freeman Voice License',
                description: 'A voice sample of the iconic narration style of Morgan Freeman',
                image: 'https://futureoflife.org/wp-content/uploads/2020/08/Morgan-Freeman-net-worth-1-e1597654595477.jpg'
            },
            ipAssetMetadata: {
                title: 'Morgan Freeman Voice Model',
                createdAt: new Date().toISOString(),
                ipType: 'voice',
                creators: [
                    {
                        name: 'AI Voice Labs',
                        email: 'creator@example.com',
                        crossmintUserLocator: 'email:creator@example.com:story-testnet',
                        contributionPercent: 100
                    },
                ],
                media: [
                    {
                        name: 'Morgan Freeman Voice Sample',
                        url: 'https://gateway.pinata.cloud/ipfs/Qmcuzm3oknzQ8eRSekyjAYw37GPvG4eTn2EcEsNscyZFoY',
                        mimeType: 'audio/mpeg'
                    },
                ],
                attributes: [
                    {
                        key: 'Voice Type',
                        value: 'Narration'
                    },
                    {
                        key: 'Voice Character',
                        value: 'Morgan Freeman'
                    },
                    {
                        key: 'License Type',
                        value: 'Commercial Use'
                    }
                ]
            }
        })
    });

    const createdIpAsset = await createResponse.json();
    console.log("Created IP Asset:", createdIpAsset);
}

main().catch(console.error);