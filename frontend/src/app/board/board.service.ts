import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpClient } from '../util/http.util.service';
import { GlobalVariable } from '../globals';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class BoardService {

  constructor (private httpClient: HttpClient) {
  }

  createSession(agendaId: number, name: string, description: string, duration: number, speakers: number[], tags: number[], venue: number, start_at?:number): Observable<any> {
    var body:any;
    if(start_at){
      body = JSON.stringify({name: name, description: description, duration: duration, speakers: speakers, tags: tags, venue: venue, start_at:start_at});
    }else{
      body = JSON.stringify({name: name, description: description, duration: duration, speakers: speakers, tags: tags, venue: venue});
    }
    return this.httpClient.post('/api/' + agendaId + '/sessions', body)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  createSpeaker(agendaId: number, name: string, company: string, profile: string, position: string, email: string, phone_number: string, company_description: string, company_url: string): Observable<any> {
    const body = JSON.stringify({name, company, profile, position, email, phone_number, company_description, company_url});
    return this.httpClient.post('/api/' + agendaId + '/speakers', body)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  createCategory(agendaId: number, name: string): Observable<any> {
    let body = JSON.stringify({name: name});
    return this.httpClient.post('/api/' + agendaId + '/categories/', body)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  createTag(agendaId: number, categoryId: number, name: string): Observable<any> {
    let body = JSON.stringify({name: name});
    return this.httpClient.post('/api/' + agendaId + '/categories/' + categoryId + '/tags/', body)
                    .map(this.extractData)
                    .catch(this.handleError);
  }

  createVenue(agendaId: number, name: string, unit: string): Observable<any> {
    let body = JSON.stringify({name: name, unit: unit});
    return this.httpClient.post('/api/' + agendaId + '/venues', body)
                    .map(this.extractData)
                    .catch(this.handleError);
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
