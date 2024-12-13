import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primaryDark: "#0F0E17",
        primaryLight: "#F2F3F4",
        primaryAccent: "#FFD700",
      },
    },
  },
  plugins: [],
} satisfies Config;
