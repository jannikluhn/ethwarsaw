<template>
  <div class="page-wrapper flex flex-col justify-center items-center w-full">
    <div
      class="bg-hero-fluffe-1 bg-no-repeat bg-[length:320px_400px] bg-[bottom_-1rem_right_-1rem] w-full d-flex flex-row justify-center py-52 h-[57rem]"
    >
      <section class="hero space-y-14 max-w-2xl mx-auto">
        <Hero></Hero>
      </section>
    </div>
    <div
      class="bg-telegram-bot bg-no-repeat bg-center bg-[length:36rem] h-[64rem] w-full py-52"
    >
      <section class="telegram-bot max-w-md mx-auto h-full">
        <h1 class="telegram-bot-header text-5xl mb-12">MYSTERALICE</h1>

        <div
          class="font-LexendDeca text-xl text-right text-black flex flex-col h-full justify-between"
        >
          <p class="">
            Meet the enigmatic Mysteralice (Telegram Bot), your loyal guide on
            this magical expedition.
          </p>
          <div
            class="flex bg-fluffe-bot bg-no-repeat bg-[left] bg-[length:12rem] h-[18rem]"
          >
            <div class="bg-p-cloud self-center ml-auto w-[50%]">
              <p>Hey Fluffeverse explorer, Where have you been?</p>
            </div>
          </div>

          <div>
            <p>
              Mysteralice will be your trusted companion, offering guidance,
              answering queries, and providing tantalizing hints that unveil the
              secrets to the hideouts of these endearing creatures.
            </p>
          </div>
        </div>
      </section>
    </div>
    <section
      class="use-cases max-w-2xl w-full flex my-24 text-black flex-col space-y-24"
    >
      <div
        class="bg-white rounded-3xl h-24 flex items-center justify-center px-12 w-[80%]"
      >
        <p class="text-3xl">Discover & Adopt Fluffees</p>
      </div>
      <div
        class="bg-white rounded-3xl h-24 flex items-center justify-center ml-auto px-12 w-[80%]"
      >
        <p class="text-3xl">Gain Fluffe Powers</p>
      </div>
      <div
        class="bg-white rounded-3xl flex items-center justify-center h-24 px-12 w-[80%]"
      >
        <p class="text-3xl">Battle it out with Frens</p>
      </div>
    </section>

    <section
      class="meet max-w-2xl w-full flex my-24 text-black flex-col space-y-24 justify-center items-center"
    >
      <h1 class="text-black">MEET THE FLUFFEES</h1>
      <div class="flex space-y-8 flex-wrap flex-row justify-center">
        <img
          src="/fluffe-2.png"
          class="h-auto max-w-sm shadow-lg dark:shadow-black/30"
          alt=""
        />

        <img
          src="fluffe-3.png"
          class="h-auto max-w-sm shadow-lg dark:shadow-black/30"
          alt=""
        />

        <img
          src="/fluffe-4.png"
          class="h-auto max-w-sm shadow-lg dark:shadow-black/30"
          alt=""
        />
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
import Hero from "../components/Hero.vue";
</script>

<style scoped>
.telegram-bot-header {
  color: #ff7ee3;
  text-shadow: 0px 3px 10px rgba(0, 0, 0, 0.12);
  font-family: Titan One;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 0.1875rem;
}
</style>
