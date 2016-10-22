import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { GlobalVariable }  from './globals';
import { tokenNotExpired } from 'angular2-jwt';


@Injectable()
export class LoggedInGuard implements CanActivate {
  constructor(
  	private router: Router
  ) {}

  private TOKEN_NAME = GlobalVariable.TOKEN_NAME;

  canActivate() {
    if (tokenNotExpired(this.TOKEN_NAME)) {
      return true;
    }
    this.router.navigate(['']);
    return false;
  }
}