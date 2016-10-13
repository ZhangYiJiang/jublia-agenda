import { Headers,RequestOptions } from '@angular/http';

export const GlobalVariable = Object.freeze({
  APP_NAME: 'Agenda Builder',
  REQUEST_OPTION: new RequestOptions({ headers: new Headers({ 'Content-Type': 'application/json' }) })
});
