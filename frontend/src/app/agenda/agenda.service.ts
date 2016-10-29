import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpClient } from '../util/http.util.service';
import { Observable }     from 'rxjs/Observable';
import { DashBoardService } from '../dash-board/dash-board.service';
import { Agenda } from './agenda';
import { Session } from '../session/session';

@Injectable()
export class AgendaService {

  constructor (private httpClient: HttpClient) {}

  private BASE_URL = '/api'

  getAgendaById(id: number): Observable<Agenda> {
    return this.httpClient.get(this.BASE_URL + '/'+ id)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  publishAgenda(id: number) {
    let data = {published: true};
    return this.updateAgenda(id, data);
  }

  unpublishAgenda(id: number) {
    let data = {published: false};
    return this.updateAgenda(id, data);
  }

  updateAgenda(id: number, data: {}): Observable<Agenda> {
    return this.httpClient.patch(this.BASE_URL + '/'+ id, JSON.stringify(data))
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

  updateSession(agendaId: number, newSession: Session) {
    console.log('updating agenda ' + agendaId + ' session ' + newSession.id);
    console.log(JSON.stringify(newSession, null, 4));
    this.httpClient
        .put(this.BASE_URL + '/' + agendaId + '/sessions/' + newSession.id, JSON.stringify(newSession))
        .catch(this.handleError)
        .subscribe(
          res => {
            console.log('update session successful');
            // console.log(res)
          },
          err => console.error(err)
        );
  }

  updateSessionInterest(agendaId: number, sessionId: number, interested: boolean, token: string) {
    console.log('updating agenda ' + agendaId + ' session ' + sessionId);
    console.log('interest changed to ' + interested);
    
    const method = interested ? 'put' : 'delete';
    this.httpClient[method](this.BASE_URL + '/' + agendaId + '/viewers/' + token + '/' + sessionId, '')
        .catch(this.handleError)
        .subscribe(
            (res : any) => {
              console.log('update session interest successful');
              console.log(res);
            },
            (err : any) => console.error(err),
        );
  }
}