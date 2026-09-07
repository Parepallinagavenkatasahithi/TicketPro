/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#F8F9FC',
        surface: '#FFFFFF',
        'surface-subtle': '#F4F5F9',
        border: '#E7E8EF',
        'border-strong': '#D1D5E3',
        text: {
          primary: '#151827',
          secondary: '#62677A',
          tertiary: '#9398AA',
        },
        brand: {
          50: '#F0ECFF',
          100: '#DED3FF',
          200: '#BEA7FF',
          300: '#9E7BFF',
          400: '#7C4DFF',
          500: '#5B35D5',
          600: '#4724B0',
          700: '#34178B',
          800: '#230E66',
          900: '#140642',
          DEFAULT: '#5B35D5',
        },
        success: {
          light: '#E6F6ED',
          DEFAULT: '#2E9B62',
          dark: '#1E6F44',
        },
        warning: {
          light: '#FDF6EA',
          DEFAULT: '#E6A23C',
          dark: '#B37820',
        },
        danger: {
          light: '#FDECEE',
          DEFAULT: '#E44D5E',
          dark: '#B32C3B',
        },
        info: {
          light: '#EEF3FD',
          DEFAULT: '#4A78E8',
          dark: '#2B53B8',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        'card': '0 1px 3px 0 rgba(21, 24, 39, 0.05), 0 1px 2px -1px rgba(21, 24, 39, 0.05)',
        'card-hover': '0 4px 12px 0 rgba(21, 24, 39, 0.08), 0 2px 4px -1px rgba(21, 24, 39, 0.04)',
        'dropdown': '0 10px 25px -5px rgba(21, 24, 39, 0.1), 0 8px 10px -6px rgba(21, 24, 39, 0.05)',
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
      }
    },
  },
  plugins: [],
}
