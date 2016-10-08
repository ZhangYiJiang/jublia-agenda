import { Component } from '@angular/core';

import {Session} from '../session/session';

@Component({
  selector: 'board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css']
})
export class BoardComponent {
  sessions: Session[] = [];
  ngOnInit() {
    let session1 = <Session>{
      _id: '1',
      title: 'session 1',
      order: 1,
      columnId: '1',
      pending: true
    };
    let session2 = <Session>{
      _id: '2',
      title: 'session 2',
      order: 2,
      columnId: '1',
      pending: true
    };
    this.sessions.push(session1);
    this.sessions.push(session2);
  }
}
