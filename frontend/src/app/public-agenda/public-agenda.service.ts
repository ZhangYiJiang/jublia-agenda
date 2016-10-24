import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpClient } from '../util/http.util.service';
import { GlobalVariable }  from '../globals';
import { Observable }     from 'rxjs/Observable';
import { DashBoardService } from '../dash-board/dash-board.service';
import { Agenda } from '../agenda/agenda';
import { Session } from '../session/session';

@Injectable()
export class PublicAgendaService {

  constructor (private httpClient: HttpClient) {}

  private BASE_URL = '/api'

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

  getViewerByToken(agendaId: number, token: string) {
    return this.httpClient.get(this.BASE_URL + '/' + agendaId + '/viewers/' + token)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  createToken(agendaId: number, email: string) {
    console.log(email);
    let body = JSON.stringify({email: email});
    return this.httpClient.post(this.BASE_URL + '/' + agendaId + '/viewers', body)
                    .map(this.extractData)
                    .catch(this.handleError);
  }
}