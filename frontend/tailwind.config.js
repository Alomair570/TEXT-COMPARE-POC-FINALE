/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  content: [
 
    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    colors: {
      'header': '#00AFA9',
      'comparator': '#F6F6F6'
    },
    fontFamily: {
      customFont: ["Noto Kufi Arabic", "sans-serif"],
    },
    extend: {},
  },
  plugins: [],
}

