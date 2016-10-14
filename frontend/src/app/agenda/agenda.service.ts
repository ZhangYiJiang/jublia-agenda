import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { GlobalVariable }  from '../globals';
import { Observable }     from 'rxjs/Observable';
import { DashBoardService } from '../dash-board/dash-board.service';
import { Agenda }     from './agenda';
import { Session }     from '../session/session';

@Injectable()
export class AgendaService {
  private httpOptions = GlobalVariable.REQUEST_OPTION;

  constructor (private http: Http) {}

  getAgendaById(id: string): Observable<any> {
    return this.http.get('/api/'+id, this.httpOptions)
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
  }
}