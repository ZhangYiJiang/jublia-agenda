import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpClient } from '../util/http.util.service';
import { GlobalVariable } from '../globals';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class SpeakerService {

  constructor (private httpClient: HttpClient) {
  }

  createSpeaker(agendaId: number, name: string, company: string, profile: string, position: string, email: string, phone_number: string, company_description: string, company_url: string): Observable<any> {
    const body = JSON.stringify({name, company, profile, position, email, phone_number, company_description, company_url});
    return this.httpClient.post('/api/' + agendaId + '/speakers', body)
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
    return Observable.throw(error.json());    
  }
}
