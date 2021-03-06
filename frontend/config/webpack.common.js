var path = require('path');
var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var helpers = require('./helpers');

module.exports = {
  entry: {
    'polyfills': './src/polyfills.ts',
    'vendor': './src/vendor.ts',
    'app': './src/main.ts'
  },

  resolve: {
    extensions: ['', '.js', '.ts']
  },

  module: {
    loaders: [
      {
        test: /\.ts$/,
        loaders: ['awesome-typescript-loader', 'angular2-template-loader']
      },
      {
        test: /\.js$/,
        include: /(angular2-modal)/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015']
        }
      },
      {
        test: /\.html$/,
        loader: 'html'
      },
      {
        test: /\.(png|jpe?g|gif|ico)$/,
        loader: 'file-loader?name=assets/[name].[hash].[ext]'
      },
      {
        test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=application/font-woff'
      },
      {
        test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=application/font-woff'
      },
      {
        test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=application/octet-stream'
      },
      {
        test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'file-loader'
      },
      {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=image/svg+xml'
      },
      {
        test: /\.css$/,
        exclude: helpers.root('src', 'app'),
        // loader: ExtractTextPlugin.extract('style', 'css?sourceMap!to-string!css-loader!postcss-loader')
        loader: ExtractTextPlugin.extract('style', 'css?sourceMap')
        // https://github.com/AngularClass/angular2-webpack-starter/wiki/How-to-include-PostCSS
        // http://stackoverflow.com/questions/36122012/how-to-run-postcss-after-sass-loader-and-extracttextplugin-have-finished
      },
      {
        test: /\.css$/,
        include: helpers.root('src', 'app'),
        loader: 'to-string!css-loader!postcss-loader'
      },
      {
        // for modernizr
        test: /\.json$/, loader: 'json-loader'
      }
    ],
    postcss: [
      require('postcss-cssnext')({
        browsers: ['ie >= 9', 'last 2 versions']
      }),
      require('autoprefixer')({
        browsers: ['last 2 versions']
      })
    ]
  },

  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      name: ['app', 'vendor', 'polyfills']
    }),

    new HtmlWebpackPlugin({
      template: 'src/index.html'
    })
  ]
};
