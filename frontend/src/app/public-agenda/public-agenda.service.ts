import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpClient } from '../util/http.util.service';
import { Observable }     from 'rxjs/Observable';

@Injectable()
export class PublicAgendaService {

  constructor (private httpClient: HttpClient) {}

  private BASE_URL = '/api'

  private extractData(res: Response) {
    console.log(res.json());
    return res.json();
  }

  private handleError (error: any) {
    /*let errMsg = (error.message) ? error.message :
      error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    console.error(errMsg);
    return Observable.throw(errMsg);*/
    return Observable.throw(error.json());
  }

  getViewerByToken(agendaId: number, token: string) {
    return this.httpClient.get(this.BASE_URL + '/' + agendaId + '/viewers/' + token)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  updateToken(agendaId: number, token: string, email?: string, mobile?:string) {
    var detail={};
    if (email) {
      detail['email'] = email;
    }
    if (mobile) {
      detail['mobile'] = mobile;
    }
    let body = JSON.stringify(detail);
    console.log('mobile is'+mobile);
        console.log(body);

    return this.httpClient.patch(this.BASE_URL + '/' + agendaId + '/viewers/' + token, body)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  createToken(agendaId: number, email: string, mobile:string) {
    console.log(email);
    let body = JSON.stringify({email: email, mobile: mobile});
    return this.httpClient.post(this.BASE_URL + '/' + agendaId + '/viewers', body)
                    .map(this.extractData)
                    .catch(this.handleError);
  }
}