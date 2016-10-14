import { Input, Component, OnInit } from '@angular/core';
import * as _ from 'lodash';

import { DragulaService } from 'ng2-dragula/ng2-dragula';

import {Session} from '../session/session';
import {Agenda} from '../agenda/agenda';
import {AgendaService} from '../agenda/agenda.service';

import { DOMUtilService } from '../util/dom.util.service';

@Component({
  selector: 'board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css']
})
export class BoardComponent implements OnInit {
  @Input()
  agenda: Agenda;

  eventDates: Date[];
  eventTracks: string[];

  pendingSessions: Session[];
  nonPendingSessions: Session[];

  constructor(private dragulaService: DragulaService,
    private agendaService: AgendaService,
    private domUtilService: DOMUtilService) {
    dragulaService.dropModel.subscribe((value: any) => {
      // console.log(`drop: ${value}`);
      this.onDrop(value.slice(1));
    });
  }

  private onDrop(args: [HTMLElement, HTMLElement]) {
    let [e, el] = args;
    // console.log('drop board');
    // console.log(e);
    // console.log(el);
    let sessionId = e.getAttribute('data-session-id');
    let columnType = el.getAttribute('data-column-type');
    if(columnType === 'relative') {
      console.log(sessionId + ' moved to pendng');
      this.changeSessionToPending(sessionId);
      console.log(this.agenda.sessions);
    }
  }

  getSessionsForColumn(columnDate: Date, columnTrack: string): Session[] {
    let displayed:Session[] = [];
    for (let session of this.nonPendingSessions) {
      if (session.pending === false 
        //add session to every track if it doesn't have a specific track
        && (!session.track || session.track === columnTrack || session.track === '') 
        && (session.start.toDateString() === columnDate.toDateString() || session.end.toDateString() === columnDate.toDateString()))
        displayed.push(session);
    }
    for (var i = 0; i < 10; ++i) {
      displayed.push(<Session>{
        placeholder: true
      })
    }

    return displayed;
  }

  changeSessionToPending(sessionId: string) {
    let session: Session = this.getSessionById(sessionId);
    if(session) {
      session.pending = true;
      session.start = undefined;
      session.end = undefined;
      this.agendaService.updateSession(this.agenda.id, session);
    } else {
      console.error('Session not found for id=' + sessionId + '.');
    }
  }

  getSessionById(sessionId: string): Session {
    for (var i = 0; i < this.agenda.sessions.length; ++i) {
      if(this.agenda.sessions[i].id === sessionId) {
        return this.agenda.sessions[i];
      }
    }
    return null;
  }

  getEventDates(): Date[] {
    let dates: Date[] = [];
    // create cloned Date to avoid mutating start date
    // TODO: use moment.js to refactor this part
    let tempDate: Date = new Date(this.agenda.start.getTime());
    while (tempDate <= this.agenda.end) {
      dates.push(new Date(tempDate.getTime()));
      tempDate.setDate(tempDate.getDate() + 1);
    }
    return dates;
  }

  getEventTracks(): string[] {
    if (!this.agenda.tracks || this.agenda.tracks.length === 0) {
      return ['']; //return a track with no name as the default track
    } else {
      return this.agenda.tracks;
    }
  }

  ngOnInit(): void {
    this.eventDates = this.getEventDates();
    this.eventTracks = this.getEventTracks();
    let partioned = _.partition(this.agenda.sessions, {pending: true});
    this.pendingSessions = partioned[0];
    this.nonPendingSessions = partioned[1];
  }
}
