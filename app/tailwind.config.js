/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");

const config = {
    content: ["./templates/**/*.{html, jinja}", "./app/static/js/**/*.js", "./app/**/*.py"],
    theme: {
        minHeight: {
            25: '25vh',
            50: '50vh',
            60: '60vh',
            70: '70vh',
            full: '100vh'
        },
        colors: {
            blue1: '#F2F5FF',
            blue2: '#B6CCFD',
            blue3: '#75A2EF',
            blue4: '#3574CA',
            blue5: '#044182',
            blue6: '#013B6B',
            blue7: '#003354',
            blue8: '#00283D',
            blue9: '#001B26',
            red1: '#FFF2F2',
            red2: '#FCB5B5',
            red3: '#EA7171',
            red4: '#B72E36',
            red5: '#54020B',
            red6: '#49010D',
            red7: '#3D000E',
            red8: '#32000F',
            red9: '#26000D',
            purple1: '#F9F2FF',
            purple2: '#FCF2FF',
            purple3: '#faf7fa',
            yellow1: '#CFC81B',
            yellow2: '#FAFFF2',
            textgrey: '#1f2937',
            orange: '#FF7514',
            transparent: "transparent",
            white: "#eee5f7",
            black: colors.black,
            mainred: "#54020c",
            snd: "#860313",
            high: "#ed8a9d",
            dark: "#1c1d19",
            link: "#F48EA3",
            c1: "#F48EA3",
            c2: "#FE7472",
            c3: "#F64143",
            c4: "#FE7F62",
        }
    },
    daisyui: {
        themes: [
            {
                mytheme: {
                    primary: "#54020c",
                    secondary: "#860313",
                    accent: "#F48EA3",
                    neutral: "#1c1d19",
                },
            },
        ],
    },
    plugins: [require('daisyui')],
}

module.exports = config;
