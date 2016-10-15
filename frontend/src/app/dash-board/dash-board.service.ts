import { Injectable }     from '@angular/core';
import { Response } from '@angular/http';
import { HttpClient } from '../util/http.util.service';
import { GlobalVariable }  from '../globals';
import { Observable }     from 'rxjs/Observable';
import { Agenda } from '../agenda/agenda';

@Injectable()
export class DashBoardService {

  private TOKEN_NAME = GlobalVariable.TOKEN_NAME;

  user = { authed:false };
  agendas: Agenda[];

  constructor (private httpClient: HttpClient) {
    //check if user has logged in
    if (localStorage.getItem(this.TOKEN_NAME)) {
      this.user.authed = true;
    }
  }
  
  signUp(email: string, password: string): Observable<number> {
    let body = JSON.stringify({ username: email, password: password});
    return this.httpClient.post('/api/users/sign_up', body)
                    .map(this.extractStatus)
                    .catch(this.handleError);
  } 

  logIn(email: string, password: string): Observable<boolean> {
    let body = JSON.stringify({ username: email, password: password});
    return this.httpClient.post('/api/users/auth', body)
                    .map(this.extractData)
                    .map(this.storeToken)
                    .catch(this.handleError);
  } 

  logOut() {
    this.agendas = [];
    this.user.authed = false;
    localStorage.removeItem(this.TOKEN_NAME);
  }

  getAgendas(): Observable<any> {
    return this.httpClient.get('/api/agendas')
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  //set the scope of this to the class
  private storeToken = (data: any) =>  {
    if (data.token) {
      //console.log(data.token);
      localStorage.setItem(this.TOKEN_NAME,data.token);
      this.user.authed = true;
      return true;
    }else {
      this.user.authed = false;
      return false;
    }
  }
  private extractStatus(res: Response) {
    console.log(res.status);
    return res.status;
  }
  private extractData(res: Response) {
    console.log(res.json());
    return res.json();
  }
  private handleError (error: any) {
    let errMsg = (error.message) ? error.message :
      error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    console.error(errMsg);
    return Observable.throw(errMsg);
  }
  
}