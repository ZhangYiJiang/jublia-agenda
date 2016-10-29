import { Injectable }     from '@angular/core';
import { Router } from '@angular/router';
import { Response } from '@angular/http';
import { HttpClient } from '../util/http.util.service';
import { User } from '../util/user.util.service';
import { GlobalVariable }  from '../globals';
import { Observable }     from 'rxjs/Observable';
import { Agenda } from '../agenda/agenda';
import { tokenNotExpired } from 'angular2-jwt';
import { JwtHelper } from 'angular2-jwt';
import * as moment from 'moment';

@Injectable()
export class DashBoardService {

  private TOKEN_NAME = GlobalVariable.TOKEN_NAME;

  currentUser = this.user.user;
  agendas: Agenda[];

  constructor (
    private httpClient: HttpClient,
    private jwtHelper: JwtHelper,
    private user: User,
    private router: Router) {
    //check if user has logged in
    this.currentUser.authed = tokenNotExpired(this.TOKEN_NAME);
  }
  
  signUp(email: string, password: string, organiser: string, event: string): Observable<number> {
    console.log(email+'\n'+password+'\n'+organiser+'\n'+event);
    let body = JSON.stringify({ username: email, password: password, company: organiser, event_name: event});
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
    this.currentUser.authed = false;
    localStorage.removeItem(this.TOKEN_NAME);
  }

  getAgendas(): Observable<any> {
    return this.httpClient.get('/api/agendas')
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  createAgenda(name: string, description: string, location: string, start: string, duration: number, website: string, tracks: string[]): Observable<any> {
    const body = JSON.stringify({
      name: name, 
      description: description, 
      location: location, 
      published: false, 
      start_at: start, 
      duration: duration,
      tracks: tracks,
      website: website,
    });
    
    return this.httpClient.post('/api/agendas', body)
      .map(this.extractData)
      .catch(this.handleError);
  }
 

  //set the scope of this to the class
  private storeToken = (data: any) =>  {
    if (data.token) {
      //console.log(data.token);
      localStorage.setItem(this.TOKEN_NAME,data.token);
      this.currentUser.authed = true;
      console.log('token saved');
      return true;
    }else {
      this.currentUser.authed = false;
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