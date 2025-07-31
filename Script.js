async function makePayment(amount) {
  if (!provider || !provider.publicKey) {
    alert("Please connect your wallet first!");
    return;
  }

  const connection = new solanaWeb3.Connection(
    solanaWeb3.clusterApiUrl('mainnet-beta'),
    'confirmed'
  );

  const toPubkey = new solanaWeb3.PublicKey("YOUR_WALLET_ADDRESS"); // Replace this

  const transaction = new solanaWeb3.Transaction().add(
    solanaWeb3.SystemProgram.transfer({
      fromPubkey: provider.publicKey,
      toPubkey,
      lamports: solanaWeb3.LAMPORTS_PER_SOL * amount,
    })
  );

  transaction.feePayer = provider.publicKey;
  const { blockhash } = await connection.getRecentBlockhash();
  transaction.recentBlockhash = blockhash;

  try {
    const signedTx = await provider.signAndSendTransaction(transaction);
    alert("Payment sent! Transaction ID:\n" + signedTx.signature);
  } catch (err) {
    console.error("Payment failed:", err);
    alert("Payment failed: " + err.message);
  }
}
