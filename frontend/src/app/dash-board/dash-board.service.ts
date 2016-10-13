import { Injectable }     from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { GlobalVariable }  from '../globals';
import { Observable }     from 'rxjs/Observable';

@Injectable()
export class DashBoardService {
  private httpOptions = GlobalVariable.REQUEST_OPTION;
  private isLoggedIn = false;

  constructor (private http: Http) {}
  
  signUp(email: string, password: string): Observable<number> {
    let body = JSON.stringify({ username: email, password: password});
    console.log(this.httpOptions);
    return this.http.post('/api/users/sign_up', body, this.httpOptions)
                    .map(this.extractStatus)
                    .catch(this.handleError);
  } 

  logIn(email: string, password: string): Observable<Object> {
    let body = JSON.stringify({ username: email, password: password});
    console.log(this.httpOptions);
    return this.http.post('/api/users/auth', body, this.httpOptions)
                    .map(this.extractData)
                    .map(this.storeToken)
                    .catch(this.handleError);
  } 

  //set the scope of this to the class
  private storeToken = (data: any) =>  {
    if (data.token) {
      console.log(data.token);
      localStorage.setItem('auth_token',data.token);
      this.isLoggedIn = true;
      return true;
    }else {
      this.isLoggedIn = false;
      return false;
    }
  }
  private extractStatus(res: Response) {
    console.log(res.status);
    return res.status;
  }
  private extractData(res: Response) {
    let body = res.json();
    return body;
  }
  private handleError (error: any) {
    let errMsg = (error.message) ? error.message :
      error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    console.error(errMsg);
    return Observable.throw(errMsg);
  }
  hasLoggedIn() {
    return this.isLoggedIn;
  }
}