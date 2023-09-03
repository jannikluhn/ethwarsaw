<template>
  <div class="d-flex h-16 w-full justify-between items-centers pt-0 px-6">
    <div
      class="d-flex text-black text-2xl cursor-pointer"
      @click="push({ name: 'Home' })"
    >
      <Logo></Logo>
    </div>
  </div>
</template>
<script lang="ts" setup>
import Logo from "./common/Logo.vue";
import { useRouter } from "vue-router";

const { push } = useRouter();
</script>
