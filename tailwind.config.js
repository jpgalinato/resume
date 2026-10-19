/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*.{html,js}',
    './assets/*.{html,js}',
  ],
  theme: {
    extend: {
      fontFamily: {
        "opensans": ['Open Sans', 'sans-serif'],
        "lora": ['Lora', 'serif'],
        "poppins": ['Poppins', 'sans-serif'],
      },
      colors: {
        'themecolor': '#f5f3ee',
        'accent': '#6CB4EE',
      },
      transitionTimingFunction: {
        'custom': 'cubic-bezier(0.165, 0.84, 0.44, 1)',
      },
      keyframes: {
        lineout: {
          '0%' : {
            transform: 'scaleX(1)',
            transformOrigin: '100% 50%',
          },
          '100%' : {
            transform: 'scaleX(0)',
            transformOrigin: '100% 50%',
          }
        },
        linein: {
          '0%' : {
            transform: 'scaleX(0)',
            transformOrigin: '0% 50%',
          },
          '100%' : {
            transform: 'scaleX(1)',
            transformOrigin: '0% 50%',
          }
        },
      },
      animation: {
        lineOut: 'lineout 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) both',
        lineIn: 'linein 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) both',
        loaderSpin: 'spin 650ms infinite linear',
      },
    },
  },
  plugins: [],
}