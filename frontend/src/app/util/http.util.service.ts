import { Injectable }     from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { GlobalVariable }  from '../globals';

@Injectable()
export class HttpClient {
  constructor(private http: Http) {}

  createRequestOptions() : RequestOptions {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Authorization', 'Bearer ' + localStorage.getItem(GlobalVariable.TOKEN_NAME));
    //console.log(headers);
    return new RequestOptions({ headers: headers});
  }

  get(url: string) { 
    return this.http.get(url, this.createRequestOptions());
  }

  post(url: string, body: string) {
    return this.http.post(url, body, this.createRequestOptions());
  }
}