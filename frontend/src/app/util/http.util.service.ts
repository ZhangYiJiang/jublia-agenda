import { Injectable }     from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { GlobalVariable }  from '../globals';
import { User } from './user.util.service';
import { Router } from '@angular/router';
import { JwtHelper } from 'angular2-jwt';
import * as moment from 'moment';

export const enum METHOD {
  GET = 0,
  POST,
  PATCH,
  PUT
}

@Injectable()
export class HttpClient {
  constructor(
    private http: Http,
    private jwtHelper: JwtHelper,
    private router: Router,
    private user: User
  ) {}

  private TOKEN_NAME = GlobalVariable.TOKEN_NAME;

  //should refresh token if it expires in less than 1 hr
  private shouldRefreshToken(): boolean {
    let token = localStorage.getItem(this.TOKEN_NAME);
    let expireOn = this.jwtHelper.getTokenExpirationDate(token);
    console.log('token expire in ' + moment(expireOn).diff(moment(),'hours',true) +' hrs');
    if (!moment().isBefore(expireOn)){
      //expired token
      //can't refresh, send user to login
      localStorage.removeItem(this.TOKEN_NAME);
      this.user.user.authed = false;
      this.router.navigate(['']);
      return false;
    }else if (moment(expireOn).diff(moment(),'hours',true) < 1){
      return true;
    }else {
      return false;
    }
  }

  private refreshThenRequest(method:METHOD, url:string, body?:string){
    let token = localStorage.getItem(this.TOKEN_NAME);
    let tokenBody = JSON.stringify({token:token});
    return this.http.post('/api/users/refresh', tokenBody, this.createRequestOptions())
      .mergeMap(res => {
        let newToken = res.json().token;
        console.log('token refreshed '+ newToken);
        localStorage.setItem(this.TOKEN_NAME, newToken);
        if (method === METHOD.GET){
          return this.forwardRequest (method, url);
        }else { 
          return this.forwardRequest (method, url, body);
        }
      }
    )
  }

  private forwardRequest (method:METHOD, url:string, body?:string){
    let requestOptions = this.createRequestOptions();
    console.log('resend '+ url);
    switch (method) {
      case METHOD.GET:
        return this.http.get(url,requestOptions);
      case METHOD.POST:
        return this.http.post(url,body,requestOptions);
      case METHOD.PATCH:
        return this.http.patch(url,body,requestOptions);
      case METHOD.PUT:
        return this.http.put(url,body,requestOptions);         
      default:
        return;        
    }
  }

  private createRequestOptions() : RequestOptions {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept','application/json');
    if(localStorage.getItem(GlobalVariable.TOKEN_NAME)){
      headers.append('Authorization', 'Bearer ' + localStorage.getItem(GlobalVariable.TOKEN_NAME));
    }
    //console.log(headers);
    return new RequestOptions({ headers: headers});
  }

  get(url: string) { 
    if (localStorage.getItem(GlobalVariable.TOKEN_NAME) && this.shouldRefreshToken()){
      return this.refreshThenRequest(METHOD.GET,url);
    }
    return this.http.get(url, this.createRequestOptions());
  }

  post(url: string, body: string) {
    if (localStorage.getItem(GlobalVariable.TOKEN_NAME) && this.shouldRefreshToken()){
      return this.refreshThenRequest(METHOD.POST,url,body);
    }
    return this.http.post(url, body, this.createRequestOptions());
  }

  patch(url: string, body: string) {
    if (localStorage.getItem(GlobalVariable.TOKEN_NAME) && this.shouldRefreshToken()){
      return this.refreshThenRequest(METHOD.PATCH,url,body);
    }    
    return this.http.patch(url, body, this.createRequestOptions());
  }

  put(url: string, body: string) {
    if (localStorage.getItem(GlobalVariable.TOKEN_NAME) && this.shouldRefreshToken()){
      return this.refreshThenRequest(METHOD.PUT,url,body);
    }
      return this.http.put(url, body, this.createRequestOptions());
  }
}