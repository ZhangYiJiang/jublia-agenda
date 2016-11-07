import {Component, Input, OnInit} from '@angular/core';
import {Agenda} from "../agenda";
import {Session} from "../../session/session";
import {AgendaService, DirtySession} from "../agenda.service";
import * as _ from 'lodash';

@Component({
  selector: 'dirty-session',
  templateUrl: 'dirty-session.component.html',
  styleUrls: [
    "dirty-session.component.css",
  ]
})

export class DirtySessionComponent implements OnInit {
  constructor(
    private agendaService: AgendaService,
  ) { }
  
  @Input() agenda: Agenda;
  
  loading = true;
  dirtySessions: DirtySession[] = [];
  total: number;
  
  ngOnInit() {
    this.agendaService.getDirtySessions(this.agenda.id)
      .subscribe((sessions: DirtySession[]) => {
        this.dirtySessions = sessions.map(session => {
          session.name = _.find(this.agenda.sessions, {id: session.id}).name;
          return session;
        });
        
        this.total = _.sum(sessions.map(session => session.popularity));
        
        this.loading = false;
      });
  }
}