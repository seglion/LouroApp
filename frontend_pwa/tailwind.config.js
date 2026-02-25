/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#373943",
        "accent-blue": "#99CCFF",
        "background-light": "#f7f7f7",
        "background-dark": "#18181a",
        // Colores de soporte adicionales
        "state-error": "#dc2626",
        "state-success": "#16a34a"
      },
      fontFamily: {
        display: ["Inter", "sans-serif"],
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "0.25rem",
        lg: "0.5rem",
        xl: "0.75rem",
        full: "9999px"
      },
      spacing: {
        'touch': '3rem',
      }
    },
  },
  plugins: [
    import('@tailwindcss/container-queries').then(m => m.default || m),
    import('@tailwindcss/forms').then(m => m.default || m)
  ],
}
