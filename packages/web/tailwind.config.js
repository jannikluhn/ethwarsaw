/** @type {import('tailwindcss').Config} */
const plugin = require("tailwindcss/plugin");

const Flip = plugin(function ({ addUtilities }) {
  addUtilities({
    ".my-rotate-y-180": {
      transform: "rotateY(180deg)",
    },
    ".preserve-3d": {
      transformStyle: "preserve-3d",
    },
    ".perspective": {
      perspective: "1000px",
    },
    ".backface-hidden": {
      backfaceVisibility: "hidden",
    },
  });
});

export default {
  content: ["./public/**/*.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        TitanOne: ["Titan One"],
        LexendDeca: ["Lexend Deca"],
      },
      backgroundImage: (theme) => ({
        "hero-fluffe-1": "url('/fluffe-1.svg')",
        "telegram-bot": "url('/telegram-bot-bg.svg')",
        "p-cloud": "url('/p-cloud.png')",
        "fluffe-bot": "url('/fluffe-bot.svg')",
      }),
    },
  },
  plugins: [Flip],
};
