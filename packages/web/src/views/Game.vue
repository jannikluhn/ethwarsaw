<template>
  <section
    class="bg-gray-900 h-screen flex justify-center items-center gap-x-16 text-white"
  >
    <Spinner v-if="fetchInProgress"></Spinner>
    <div
      v-else
      v-for="answerIndex in possibleAnswers"
      @click="_submitGameAnswer(answerIndex.toString())"
      class="w-[300px] h-[420px] bg-transparent cursor-pointer group perspective"
    >
      <div
        class="relative preserve-3d w-full h-full duration-1000"
        :class="{
          'my-rotate-y-180': encounterGame?.answer == answerIndex.toString(),
        }"
      >
        <div class="absolute backface-hidden w-full h-full">
          <img src="/card-back.png" class="w-full h-full" />
        </div>
        <div
          class="absolute my-rotate-y-180 backface-hidden w-full h-full bg-gray-100 overflow-hidden"
        >
          <Spinner v-if="submissionInProgress"></Spinner>
          <div
            v-else-if="encounterGame?.correctAnswer == answerIndex.toString()"
            class="text-center flex flex-col items-center justify-center h-full text-gray-800 px-2 pb-24"
          >
            <div
              class="text-center flex flex-col items-center justify-center pt-4"
            >
              <ConnectButton
                v-if="!isConnected"
                :chain-id="chainId"
                class="bg-[#d9d9d9] text-black"
              ></ConnectButton>
              <Button
                v-else-if="!claimed"
                @click="handleClaimClick"
                class="bg-[#d9d9d9] text-black"
                :dislabed="claimStatus === 'inProgress'"
              >
                <Spinner v-if="claimStatus === 'inProgress'"></Spinner>
                <span v-else>Claim</span>
              </Button>
              <div v-else>Claim success</div>

              <div v-if="claimStatus === 'failed'" class="text-red">
                Claiming failed.
              </div>
            </div>
          </div>
          <div v-else>
            <div class="absolute backface-hidden w-full h-full">
              <img src="/card-front.png" class="w-full h-full" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script lang="ts" setup>
import { useRoute } from "vue-router";
import {
  useAccount,
  useSwitchNetwork,
  useNetwork,
  useContractWrite,
} from "use-wagmi";
import { useClaim } from "../composables/useClaim";
import ConnectButton from "../components/ConnectButton.vue";
import Button from "../components/common/Button.vue";
import { useGameApi } from "../composables/useGameApi";
import Spinner from "../components/common/Spinner.vue";
import { Ref, ref } from "vue";

const {
  params: { encounterId },
} = useRoute();

const possibleAnswers = 3;

const {
  encounterGame,
  fetchInProgress,
  submissionInProgress,
  submitGameAnswer,
} = useGameApi(encounterId as string);

async function _submitGameAnswer(index: string) {
  if (encounterGame.value?.answer == undefined) {
    await submitGameAnswer(index);
  }
}
const claimStatus: Ref<string | undefined> = ref(undefined);
const claimed = ref(false);
const { isConnected } = useAccount();
const { chain } = useNetwork();
const { switchNetworkAsync } = useSwitchNetwork();
const chainId = ref(undefined);
const { claim } = useClaim(chainId);

async function handleClaimClick() {
  claimStatus.value = "inProgress";
  if (
    !encounterGame.value?.chainId ||
    !encounterGame.value?.eligibleMinter ||
    !encounterGame.value?.tokenId ||
    !encounterGame.value?.uriIndex ||
    !encounterGame.value?.authorizationSignature
  )
    return false;

  const chainId = parseInt(encounterGame.value?.chainId);

  if (chain && chain.value?.id !== chainId) {
    const newChain = await switchNetworkAsync(chainId);
    if (newChain.id !== chainId) {
      claimStatus.value = "failed";
      return false;
    }
  }

  const hash = await claim(
    chainId,
    encounterGame.value?.eligibleMinter,
    encounterGame.value?.tokenId.toString(),
    encounterGame.value?.uriIndex,
    encounterGame.value?.authorizationSignature
  );

  if (hash) {
    claimStatus.value = "success";
    claimed.value = true;
  }
}
</script>
