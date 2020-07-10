const path = require('path');
const webpack = require('webpack');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, './bin'),
    filename: 'app.js',
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /\/node_modules\//,
      use: {
        loader: 'babel-loader'
      }
    }, {
      test: /\.css$/,
      use: [ 'style-loader',
             { loader: 'css-loader', options: { importLoaders: 1 } },
             'postcss-loader' ]
    }]
  }
};
