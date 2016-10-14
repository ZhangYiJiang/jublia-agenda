import { Headers,RequestOptions } from '@angular/http';

export const GlobalVariable = Object.freeze({
  APP_NAME: 'Agenda Builder',
  TOKEN_NAME: 'auth_token',
  REQUEST_OPTION: new RequestOptions({ headers: new Headers({ 'Content-Type': 'application/json' }) }),
  REQUEST_OPTION_WITH_TOKEN: new RequestOptions({
   	headers: new Headers({ 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + localStorage.getItem('auth_token') }) 
	})
});
