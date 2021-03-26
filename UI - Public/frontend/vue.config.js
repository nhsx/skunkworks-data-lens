const { json2csv } = require("json-2-csv");

module.exports = {
  configureWebpack: {
    devtool: 'source-map'
  },
  devServer: {
    host: 'localhost'
  },
  transpileDependencies: [
    "json2csv",
    "moment"
  ],
  devServer: {
    proxy: {
      "^/api": {
        target: "http://localhost:3000",
        logLevel: "debug",
      }
    }
  }
}