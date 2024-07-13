import { useRef, useState } from "react";
import { encodePacked, keccak256, parseUnits } from "viem";
import { generatePrivateKey } from "viem/accounts";
import { useReadContract, useWaitForTransactionReceipt, useWriteContract } from "wagmi";
import deployedContracts from "~~/contracts/deployedContracts";
import { notification } from "~~/utils/scaffold-eth";

const generateEANHash = (ean: string, salt: string): `0x${string}` => {
  const packed = encodePacked(["uint256", "bytes32"], [BigInt(ean), salt as `0x${string}`]);
  return keccak256(packed);
};

export const CreateCommunity = ({
  contractAddress,
  meters,
  escrowAmount,
}: {
  contractAddress: `0x${string}`;
  meters: { meterType: number; meterEAN: string }[];
  escrowAmount: string;
}) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const { writeContract, data: hash, error, isPending } = useWriteContract();
  const privateKey = generatePrivateKey();

  const argsKey = useRef(privateKey);

  const readContract = useReadContract({
    functionName: "generateHash",
    address: contractAddress,
    abi: deployedContracts[31337].DecentralizedEnergyCommunity.abi,
    args: [BigInt(1), argsKey.current],
  });

  const EANhash = readContract.data;

  console.log("Read contract:", readContract);

  const { isLoading: isConfirming, isSuccess: isConfirmed } = useWaitForTransactionReceipt({
    hash,
  });

  const handleCreateCommunity = async () => {
    setIsProcessing(true);
    try {
      console.log("Processing meters...");
      const processedMeters = await Promise.all(
        meters.map(async meter => {
          const salt = crypto.getRandomValues(new Uint8Array(32));
          const saltHex = `0x${Array.from(salt)
            .map(b => b.toString(16).padStart(2, "0"))
            .join("")}`;
          const eanHash = await generateEANHash(meter.meterEAN, saltHex);
          return { meterType: meter.meterType, meterEAN: eanHash };
        }),
      );
      console.log("Processed meters:", processedMeters);

      console.log("Calling writeContract..., ", processedMeters, parseUnits(escrowAmount, 6));
      writeContract({
        address: contractAddress,
        abi: deployedContracts[31337].DecentralizedEnergyCommunity.abi,
        functionName: "createCommunity",
        args: [
          {
            escrowAmount: 1000000000000n,
            meters: [
              {
                meterType: 2,
                meterEAN: EANhash!,
              },
              {
                meterType: 1,
                meterEAN: EANhash!,
              },
            ],
          },
        ],
      });
    } catch (e) {
      console.error("Error in handleCreateCommunity:", e);
      if (e instanceof Error) {
        notification.error(`Error creating community: ${e.message}`);
      } else {
        notification.error("Error creating community");
      }
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div>
      <button onClick={handleCreateCommunity} disabled={isPending || isProcessing}>
        {isPending || isProcessing ? "Creating Community..." : "Create Community"}
      </button>
      {hash && <div>Transaction Hash: {hash}</div>}
      {isConfirming && <div>Waiting for confirmation...</div>}
      {isConfirmed && <div>Community created successfully!</div>}
      {error && <div>Error: {error.message}</div>}
    </div>
  );
};
