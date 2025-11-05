/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        background: "#05070f",
        panel: "#11182f",
        border: "#1e293b",
        accent: {
          DEFAULT: "#38bdf8",
          muted: "#0ea5e9"
        }
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"]
      },
      boxShadow: {
        glow: "0 0 20px rgba(56, 189, 248, 0.2)"
      }
    }
  },
  plugins: []
};
