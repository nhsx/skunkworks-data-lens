module.exports = {
  presets: [ [ "@vue/app", { useBuiltIns: "entry" } ] ],
  plugins: ["@babel/plugin-transform-spread", "@babel/plugin-proposal-object-rest-spread"]
}
