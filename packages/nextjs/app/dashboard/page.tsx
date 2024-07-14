"use client";

import { useState } from "react";
import { useDynamicContext } from "@dynamic-labs/sdk-react-core";
import { ChartComponent } from "~~/components/AreaChart";
import BarGraph from "~~/components/UI/BarGraph";
import { PieChartComponent } from "~~/components/UI/PieChart";
import { Address } from "~~/components/scaffold-eth";
import deployedContracts from "~~/contracts/deployedContracts";
import { CreateCommunity } from "~~/lib/createCommunity";
import { sendTransaction, signMessage } from "~~/lib/dynamic";

export default function DashboardHome() {
  const { primaryWallet, networkConfigurations } = useDynamicContext();
  const [messageSignature, setMessageSignature] = useState<string>("");
  const [transactionSignature, setTransactionSignature] = useState<string>("");
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [communityCreationHash, setCommunityCreationHash] = useState<string>("");
  const connectedAddress = primaryWallet?.address;
  console.log("");

  const handleSignMessage = async () => {
    try {
      const signature = await signMessage("Hello World", primaryWallet);
      setMessageSignature(signature);
      setTimeout(() => setMessageSignature(""), 10000);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSendTransaction = async () => {
    try {
      const isTestnet = await primaryWallet?.connector?.isTestnet();
      if (!isTestnet) {
        alert("You're not on a testnet, proceed with caution.");
      }
      if (!primaryWallet || !networkConfigurations) {
        throw new Error("Wallet or network configurations not found.");
      }
      const hash = await sendTransaction(connectedAddress, "0.0001", primaryWallet, networkConfigurations);
      setTransactionSignature(hash!);
      setTimeout(() => setTransactionSignature(""), 10000);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white/5 shadow-2xl p-6 rounded-lg">
        <h2 className="text-2xl font-semibold text-white mb-4">Your Hub</h2>
        <div className="grid gap-4 grid-cols-1 md:grid-cols-3">
          <div className="col-span-1 md:col-span-2">
            <ChartComponent />
            <BarGraph />
          </div>
          <div>
            <PieChartComponent />
          </div>
        </div>
      </div>
      <div className="bg-white/5 shadow-2xl p-6 rounded-lg">
        <h2 className="text-2xl font-semibold text-white mb-4">Wallet Actions</h2>
        <div className="space-y-4">
          <div className="flex items-center space-x-2">
            <p className="font-medium text-white">Connected Address:</p>
            <Address address={connectedAddress} />
          </div>
          {primaryWallet && !transactionSignature && !communityCreationHash && (
            <div className="flex flex-col sm:flex-row gap-2">
              <button onClick={handleSendTransaction} className="btn btn-primary">
                Send 0.001 ETH to yourself
              </button>
              <button onClick={handleSignMessage} className="btn btn-primary">
                Sign `&quot;`Hello World`&quot;`
              </button>
              <CreateCommunity
                contractAddress={deployedContracts[31337].DecentralizedEnergyCommunity.address}
                meters={[{ meterType: 1, meterEAN: "123456789012345679" }]}
                escrowAmount="100"
              />
            </div>
          )}
          {primaryWallet && messageSignature && <p className="text-white">Message signed! {messageSignature}</p>}
          {primaryWallet && transactionSignature && (
            <p className="text-white">Transaction processed! {transactionSignature}</p>
          )}
          {primaryWallet && communityCreationHash && (
            <p className="text-white">Community creation transaction sent! {communityCreationHash}</p>
          )}
        </div>
      </div>
    </div>
  );
}
