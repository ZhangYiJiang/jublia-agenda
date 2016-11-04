import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import * as _ from 'lodash';

import { HttpClient } from '../util/http.util.service';
import { Session } from '../session/session';
import { Speaker } from '../speaker/speaker';
import { Venue } from '../venue/venue';
import { Agenda } from './agenda';
import { GlobalVariable } from '../globals';

@Injectable()
export class AgendaService {

  constructor (private httpClient: HttpClient) {}

  static agendaEndpoint(id: number, path: string = ''): string {
      return _.trimEnd([GlobalVariable.API_BASE_URL, id, path].join('/'), '/');
  }
  
  static sessionEndpoint(agendaId: number, sessionId: number) {
      return AgendaService.agendaEndpoint(agendaId, 'sessions/' + sessionId);
  }

  getAgendaAnalytics(id: number): Observable<any> {
    return this.httpClient.get(AgendaService.agendaEndpoint(id, 'data'))
                    .map(AgendaService.extractData)
                    .catch(AgendaService.handleError);
  }

  getAgendaById(id: number): Observable<Agenda> {
    return this.httpClient.get(AgendaService.agendaEndpoint(id))
                    .map(AgendaService.extractData)
                    .map(AgendaService.extractAgenda)
                    .catch(AgendaService.handleError);
  }
  
  getDirtySessions(id: number): Observable<number[]> {
    return this.httpClient.get(AgendaService.agendaEndpoint(id, 'dirty'))
      .map(AgendaService.extractData)
      .catch(AgendaService.handleError);
  }
  
  sendViewerEmail(id: number): Observable<any> {
    return this.httpClient.post(AgendaService.agendaEndpoint(id, 'dirty'), '')
      .catch(AgendaService.handleError);
  }

  setPublished(id: number, status: boolean) {
    return this.updateAgenda(id, {published: status});
  }

  updateAgenda(id: number, data: {}): Observable<Agenda> {
    return this.httpClient.patch(AgendaService.agendaEndpoint(id), JSON.stringify(data))
                    .map(AgendaService.extractData)
                    .map(AgendaService.extractAgenda)
                    .catch(AgendaService.handleError);
  }

  private static extractData(res: Response) {
    // console.log(res.json());
    return res.json();
  }

  private static extractSession(session: any) {
    // TODO: Remove this when multi-track session is ready
    session.track = session.tracks[0];
    return session;
  }

  private static extractAgenda(agenda: any) {
    if (agenda.sessions == null) {
      console.log('added empty sessions array');
      agenda.sessions = [];
    }
    
    // Map extract session
    agenda.sessions = agenda.sessions.map(AgendaService.extractSession);
    
    // Check if there are any dirty sessions
    agenda.hasDirtySession = agenda.sessions.some((session: Session) => session.is_dirty);
    
    // Calculate max and min popularity 
    const popularityCount = agenda.sessions.map((session: Session) => session.popularity);
    agenda.maxPopularity = _.max(popularityCount) || 0;
    agenda.minPopularity = _.min(popularityCount)|| 0;
    console.log(agenda);
    return agenda;
  }

  private static handleError (error: any) {
    let errMsg = (error.message) ? error.message :
      error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    console.error(errMsg);
    return Observable.throw(errMsg);
  }

  updateSession(agendaId: number, session: Session): Observable<any> {
    // TODO: Remove this when multi-track session is ready
    session.tracks = [session.track];
  
    console.log('updating agenda ' + agendaId + ' session ' + session.id);
    console.log(JSON.stringify(session, null, 4));

    return this.httpClient
        .put(AgendaService.sessionEndpoint(agendaId, session.id), JSON.stringify(session))
        .map(AgendaService.extractData)
        .map(AgendaService.extractSession)
        .catch(AgendaService.handleError);
  }

  deleteSession(agendaId: number, session: Session) {
    console.log('deleting agenda ' + agendaId + ' session ' + session.id);
    console.log(JSON.stringify(session, null, 4));
    this.httpClient
        .delete(AgendaService.sessionEndpoint(agendaId, session.id))
        .catch(AgendaService.handleError)
        .subscribe(
          res => {
            console.log('delete session successful');
            // console.log(res)
          },
          err => console.error(err)
        );
  }

  updateSessionInterest(agendaId: number, sessionId: number, interested: boolean, token: string) {
    console.log('updating agenda ' + agendaId + ' session ' + sessionId);
    console.log('interest changed to ' + interested);
    
    const method = interested ? 'put' : 'delete';
    const url = AgendaService.agendaEndpoint(agendaId, ['viewers', token, sessionId].join('/'));
      
    this.httpClient[method](url, '')
        .catch(AgendaService.handleError)
        .subscribe(
            (res : any) => {
              console.log('update session interest successful');
              console.log(res);
            },
            (err : any) => console.error(err),
        );
  }

  updateSpeaker(agendaId: number, speaker: Speaker) {
    console.log('updating speaker ' + agendaId + ' speaker ' + speaker.id);
    console.log(JSON.stringify(speaker, null, 4));
    const url = AgendaService.agendaEndpoint(agendaId, 'speakers/' + speaker.id);
    
    this.httpClient
        .put(url, JSON.stringify(speaker))
        .catch(AgendaService.handleError)
        .subscribe(
          res => {
            console.log('update speaker successful');
            // console.log(res)
          },
          err => console.error(err)
        );
  }

  updateVenue(agendaId: number, venue: Venue) {
    console.log('updating venue ' + agendaId + ' venue ' + venue.id);
    console.log(JSON.stringify(venue, null, 4));
    const url = AgendaService.agendaEndpoint(agendaId, 'venues/' + venue.id);
    
    this.httpClient
        .put(url, JSON.stringify(venue))
        .catch(AgendaService.handleError)
        .subscribe(
          res => {
            console.log('update venue successful');
            // console.log(res)
          },
          err => console.error(err)
        );
  }
}