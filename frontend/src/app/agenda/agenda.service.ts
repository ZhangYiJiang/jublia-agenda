import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpClient } from '../util/http.util.service';
import { GlobalVariable }  from '../globals';
import { Observable }     from 'rxjs/Observable';
import { DashBoardService } from '../dash-board/dash-board.service';
import { Agenda }     from './agenda';
import { Session }     from '../session/session';

@Injectable()
export class AgendaService {

  constructor (private httpClient: HttpClient) {}

  private BASE_URL = '/api'

  getAgendaById(id: string): Observable<Agenda> {
    return this.httpClient.get(this.BASE_URL + '/'+ id)
                    .map(this.extractData)
                    .catch(this.handleError);
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

  updateSession(agendaId: string, newSession: Session) {
    console.log('updating agenda ' + agendaId + ' session ' + newSession.id);
    console.log(JSON.stringify(newSession, null, 4));
    this.httpClient
        .put(this.BASE_URL + '/' + agendaId + '/sessions/' + newSession.id, JSON.stringify(newSession))
        .catch(this.handleError)
        .subscribe(
          res => {
            console.log('updated session, result:');
            console.log(res)
          },
          err => console.error(err)
        );
  }
}