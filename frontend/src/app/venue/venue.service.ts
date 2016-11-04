import { Injectable } from '@angular/core';
import { Response } from '@angular/http';
import { HttpClient } from '../util/http.util.service';
import { GlobalVariable } from '../globals';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class VenueService {

  constructor (private httpClient: HttpClient) {
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
    return Observable.throw(error.json());    
  }
}
