/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'carbon-green': '#10b981',
        'carbon-dark': '#1f2937',
      }
    },
  },
  plugins: [],
}
