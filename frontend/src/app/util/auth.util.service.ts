import { Injectable }     from '@angular/core';

@Injectable()
export class Auth{
  constructor(){}
  user = { authed:false };
}