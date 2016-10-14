import { Headers,RequestOptions } from '@angular/http';

export const GlobalVariable = Object.freeze({
  APP_NAME: 'Agenda Builder',
  TOKEN_NAME: 'auth_token',
  CONTENT_HEADER: new Headers({ 'Content-Type': 'application/json' })
});
