const Webpack = require('webpack');
const { merge } = require('webpack-merge');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const common = require('./webpack.common.js');
const { VueLoaderPlugin } = require('vue-loader')

module.exports = merge(common, {
  mode: 'production',
  devtool: 'source-map',
  bail: true,
  output: {
    filename: 'js/[name].js',
    chunkFilename: 'js/[name].[chunkhash:8].chunk.js',
  },
  plugins: [
    new VueLoaderPlugin(),
    new Webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production'),
    }),
    new MiniCssExtractPlugin({
      filename: 'css/app.css',
    }),
  ],
  module: {
    rules: [
    {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.s?css/i,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader'],
      },
    ],
  },
});