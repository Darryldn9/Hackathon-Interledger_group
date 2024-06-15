import {
    createAuthenticatedClient,
    isPendingGrant,} from "@interledger/open-payments";
import config from "./config.js";
import { fetch } from 'node-fetch';

// http://127.0.0.1:8000/reciever_details?subscription_id=1 API end point
// Function to handle payment details
async function fetchSubscriptionDetails(subscriptionId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/reciever_details?subscription_id=${subscriptionId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch subscription details');
        }
        const data = await response.json();
        console.log('Subscription Details:', data);
    } catch (error) {
        console.error('Error:', error.message);
    }
}


export async function handlePaymentDetails(paymentDetails) {
    try {
        // Use the paymentDetails object received from payAndProceed
        console.log(paymentDetails);

        // Example: Use client and config to process payment or other actions
        const client = await createAuthenticatedClient({
            walletAddressUrl: config.CLIENT_WALLET_ADDRESS_URL,
            keyId: config.KEY_ID,
            privateKey: config.PRIVATE_KEY_PATH,
            validateResponses: false,
        });

        // Example: Use the receiving wallet address from paymentDetails
        const receivingWalletAddress = await client.walletAddress.get({
            url: paymentDetails.payment_endpoint,
        });

        // Further processing based on paymentDetails
        // ...

    } catch (error) {
        console.error('Error handling payment details:', error);
        // Handle error (e.g., show an alert to the user)
    }
}


fetchSubscriptionDetails(1);