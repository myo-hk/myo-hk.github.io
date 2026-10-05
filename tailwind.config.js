/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*.html',
    './blog/**/*.html',
    './css/*.css',
  ],
  safelist: [
    'swiper-pagination-bullet-active',
    'active',
    'hidden',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};