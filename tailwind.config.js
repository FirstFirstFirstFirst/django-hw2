/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './myapp/template/**/*.html',
    './templates/**/*.html',
    './static/**/*.js',
    './templates/cotton/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        'stratford': ['Stratford-Serial', 'serif'],
      },
      colors: {
        // Earth tone palette from your requirements
        'terracotta': {
          50: '#fdf5f3',
          100: '#fbe9e6',
          200: '#f6d6d1',
          300: '#efb8ad',
          400: '#e4927f',
          500: '#cb846c', // Primary terracotta
          600: '#bf6b55',
          700: '#9f5749',
          800: '#834943',
          900: '#6e3f3f',
        },
        'sage': {
          50: '#f5f7f2', // Very light sage/cream
          100: '#eaeee4',
          200: '#d6ddcb',
          300: '#bbc6a8',
          400: '#9da985',
          500: '#829169',
          600: '#6b7455',
          700: '#555c46',
          800: '#46493b',
          900: '#3c3e33',
        },
        'earth': {
          50: '#faf9f7',
          100: '#f0ede8',
          200: '#e5d9ba', // Light beige
          300: '#d4c7a6',
          400: '#c1b292',
          500: '#a8997e',
          600: '#94938d', // Medium gray
          700: '#7a7671',
          800: '#5f5c57',
          900: '#483e37', // Dark brown
        },
        'brown': {
          50: '#f7f5f3',
          100: '#ede8e4',
          200: '#ddd4cc',
          300: '#c7b8ac',
          400: '#b09688',
          500: '#895f4c', // Medium brown
          600: '#7d5544',
          700: '#68463a',
          800: '#553a32',
          900: '#47322b',
        },
        'muted': {
          50: '#f7f7f6',
          100: '#eeeeec',
          200: '#ddddd9',
          300: '#c8c8c2',
          400: '#b0b0a8',
          500: '#cecbc5', // Light gray
          600: '#8a8a82',
          700: '#74736e',
          800: '#62615c',
          900: '#53524f',
        },
        'tan': {
          50: '#faf8f5',
          100: '#f3efe8',
          200: '#e8ddd0',
          300: '#d8c7b2',
          400: '#d19e7d', // Light brown/tan
          500: '#c08964',
          600: '#a87654',
          700: '#8d6349',
          800: '#735242',
          900: '#5e453a',
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
      boxShadow: {
        'soft': '0 2px 8px 0 rgba(72, 62, 55, 0.08)',
        'medium': '0 4px 12px 0 rgba(72, 62, 55, 0.12)',
        'large': '0 8px 24px 0 rgba(72, 62, 55, 0.15)',
        'inner-soft': 'inset 0 2px 4px 0 rgba(72, 62, 55, 0.06)',
      },
      borderRadius: {
        'xl2': '1rem',
        'xl3': '1.5rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}