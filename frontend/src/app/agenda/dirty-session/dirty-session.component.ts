import {Component, Input, OnInit} from '@angular/core';
import {Agenda} from "../agenda";
import {Session} from "../../session/session";
import {AgendaService} from "../agenda.service";

@Component({
  selector: 'dirty-session',
  templateUrl: 'dirty-session.component.html',
})

export class DirtySessionComponent implements OnInit {
  constructor(
    private agendaService: AgendaService,
  ) { }
  
  @Input() agenda: Agenda;
  
  loading = true;
  dirtySessions = <Session[]>[];
  
  ngOnInit() {
    this.agendaService.getDirtySessions(this.agenda.id)
      .subscribe((sessions: number[]) => {
        this.dirtySessions = this.agenda.sessions.filter((session: Session) => sessions.includes(session.id));
        this.loading = false;
      });
  }
}