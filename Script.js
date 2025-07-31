const provider = window.solana;

document.getElementById("connectWallet").addEventListener("click", async () => {
  if (provider && provider.isPhantom) {
    try {
      const resp = await provider.connect();
      alert("Connected: " + resp.publicKey.toString());
    } catch (err) {
      console.error("Wallet connection failed:", err);
    }
  } else {
    alert("Please install Phantom Wallet!");
  }
});

async function makePayment(amount) {
  const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');
  const toPubkey = new solanaWeb3.PublicKey(DB9YZwXgNeQByab3bgJnJKrnYP7CtZGktrdnDRCLrKA3); // Replace this

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
    const signed = await provider.signTransaction(transaction);
    const signature = await connection.sendRawTransaction(signed.serialize());
    alert("Payment Sent! Tx: " + signature);
  } catch (err) {
    console.error("Transaction failed:", err);
    alert("Payment failed");
  }
}
