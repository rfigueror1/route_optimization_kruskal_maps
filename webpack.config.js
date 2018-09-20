const path = require('path');

module.exports = {
  entry: './src/index.jsx',
  module: {
  rules: [
    {
      test: /\.jsx$/,
      exclude: /(node_modules|bower_components)/,
      use: {
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env', '@babel/react']
        }
      }
    }
  ]
},
  output: {
    path: path.resolve(__dirname, 'public'),
    filename: 'bundle.js'
  }
};
