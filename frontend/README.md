# Front-end for Event Agenda App in Angular 2

## Setting up front-end for development:
- Run `sudo npm install -g npm` [due to a possible bug](http://stackoverflow.com/questions/37038269/npm-err-invalid-name-angular-core-when-following-the-angular-2-quick-start)
- Run `npm install`

## Running in dev environment
- `npm start`

## Building
- `npm run build`

## Running in production environment
- `npm run build`
- `cd dist`
- server the folder using any backend server

## Set-up Reference:
- https://angular.io/docs/ts/latest/guide/webpack.html

## Style Guide Reference:
- https://angular.io/docs/ts/latest/guide/style-guide.html

## Issues:
- Need to manually precompile scss to css before building due to [complexity in using sass loaders with angular 2](https://github.com/AngularClass/angular2-webpack-starter/issues/136)
