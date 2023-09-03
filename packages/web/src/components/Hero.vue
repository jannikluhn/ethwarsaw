<template>
  <h1 class="text-7xl">CHRONICLES OF CUTENESS</h1>
  <h2 class="font-LexendDeca font-light text-black text-2xl">
    Embark on a whimsical journey through the Fluffeverse on Mantle and Celo. In
    this enchanting world, many dApps serve as hideouts for adorable and elusive
    creatures called Fluffees. Your mission is to explore all of those hideouts
    (dApps) so you can spot, interact with, and adopt these charming beings.
  </h2>

  <Button @click="clickHandler" class="bg-[#88cfef] px-8 rounded-3xl">
    <span v-if="!isConnected">Connect</span>
    <span v-else-if="!isRegistered">Register</span>
    <span v-else>Start your journey</span>
  </Button>
</template>

<script lang="ts" setup>
import Button from "./common/Button.vue";
import { useRegister } from "../composables/useRegister";
import { useAccount, useConnect } from "use-wagmi";
import { ref } from "vue";

const { address, isConnected } = useAccount();
const { isRegistered, register, tryNavigateToTelegram, chatSecret } =
  useRegister(address, ref(1));
const { connect, connectors } = useConnect();

async function clickHandler() {
  if (!isConnected.value)
    await connect({
      connector: connectors.value[0],
    });
  else if (!isRegistered.value) {
    await register();
  } else if (chatSecret.value) {
    tryNavigateToTelegram();
  }
}
</script>
