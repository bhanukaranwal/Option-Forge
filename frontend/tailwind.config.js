// frontend/tailwind.config.js

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enable dark mode via class
  theme: {
    extend: {
      colors: {
        'primary': '#3b82f6', // blue-500
        'primary-hover': '#2563eb', // blue-600
        'secondary': '#10b981', // emerald-500
        'background-light': '#f8fafc', // slate-50
        'background-dark': '#1e293b', // slate-800
        'card-light': '#ffffff',
        'card-dark': '#334155', // slate-700
        'text-light': '#0f172a', // slate-900
        'text-dark': '#f1f5f9', // slate-100
        'border-light': '#e2e8f0', // slate-200
        'border-dark': '#475569', // slate-600
      },
    },
  },
  plugins: [],
}
