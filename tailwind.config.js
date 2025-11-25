/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "./static/**/*.js",
        "./static/**/*.css"
    ],
    theme: {
        extend: {
            colors: {
                // Add custom colors here if needed
            },
            fontFamily: {
                // Add custom fonts here if needed
            },
            animation: {
                // Add custom animations here if needed
            },
            keyframes: {
                // Add custom keyframes here if needed
            }
        },
    },
    plugins: [],
}
