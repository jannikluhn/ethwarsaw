import { useContractWrite } from "use-wagmi";
import { DEPLOYED_ADDRESSES, isChainSupported } from "../config/deployment";
import FluffeABI from "../assets/abi/Fluffe.json";
import { Ref, computed } from "vue";

export const useClaim = function (chainId: Ref<number | undefined>) {
  const contractAddress = computed(() => {
    return DEPLOYED_ADDRESSES.Fluffe[chainId.value ?? 42220];
  });

  const { writeAsync, isLoading, isSuccess, error } = useContractWrite({
    abi: FluffeABI,
    functionName: "mint",
    address: contractAddress,
  });

  async function claim(
    chainId: number,
    to: string,
    tokenId: string,
    uriIndex: string,
    authorizationSignature: string
  ) {
    if (!isChainSupported(chainId)) {
      console.log("Chain not supported.");
      return false;
    }
    console.log(contractAddress.value, chainId);
    const hash = await writeAsync({
      args: [to, tokenId, uriIndex, authorizationSignature],
    });

    return hash;
  }

  return {
    claim,
  };
};
