import { Injectable }     from '@angular/core';

@Injectable()
export class User{
  constructor(){}
  user = { authed:false, agenda:false };
}