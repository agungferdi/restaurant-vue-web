/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fef7ee',
          100: '#fdedd3',
          200: '#fbd7a5',
          300: '#f8bc6d',
          400: '#f59833',
          500: '#f37f0c',
          600: '#e46407',
          700: '#bd4b08',
          800: '#983c0e',
          900: '#7c320f',
          950: '#431605',
        }
      }
    },
  },
  plugins: [],
}