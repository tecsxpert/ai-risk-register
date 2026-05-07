export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#EFF6FF",
          100: "#DBEAFE",
          200: "#BFDBFE",
          300: "#93C5FD",
          400: "#60A5FA",
          500: "#3B82F6",
          600: "#2563EB",
          700: "#1D4ED8",
          800: "#163d6e",
          900: "#1B4F8A",
          950: "#0f2d52",
        },
      },
      fontFamily: {
        sans: ["Inter", "Arial", "sans-serif"],
      },
      borderRadius: {
        "xl": "12px",
        "2xl": "16px",
        "3xl": "24px",
      },
      boxShadow: {
        "card": "0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)",
        "card-hover": "0 4px 12px rgba(0,0,0,0.10), 0 2px 4px rgba(0,0,0,0.06)",
        "brand": "0 4px 14px rgba(27, 79, 138, 0.2)",
        "modal": "0 20px 60px rgba(0,0,0,0.15)",
      },
      spacing: {
        "18": "72px",
        "22": "88px",
      },
    },
  },
  plugins: [],
};