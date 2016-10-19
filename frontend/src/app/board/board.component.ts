import { Input, Component, OnInit } from '@angular/core';
import * as _ from 'lodash';

import { DragulaService } from 'ng2-dragula/ng2-dragula';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { Track } from '../track/track';
import { AgendaService } from '../agenda/agenda.service';

import { DOMUtilService } from '../util/dom.util.service';

@Component({
  selector: 'board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css']
})
export class BoardComponent implements OnInit {
  @Input()
  agenda: Agenda;
  offsetDate: Date;
  eventDates: Date[];
  eventTracks: Track[];

  allSessions: Session[];
  pendingSessions: Session[];
  nonPendingSessions: Session[];

  dragging: boolean = false;

  private PLACEHOLDER_DURATION: number = 15;

  constructor(private dragulaService: DragulaService,
    private agendaService: AgendaService,
    private domUtilService: DOMUtilService) {
    dragulaService.dropModel.subscribe((value: any) => {
      // console.log(`drop: ${value}`);
      this.dragging = false;
      this.onDrop(value.slice(1));
    });

    dragulaService.drag.subscribe((value: any) => {
      this.dragging = true;
    });

    dragulaService.setOptions('column', {
      // copy: true,
      // copySortSource: true
      accepts: this.canDropSession.bind(this)
    });
  }

  canDropSession(el: HTMLElement, target: HTMLElement): boolean {
    // only accept when the slot container is empty
    // or the slot is for pending session
    return this.domUtilService.hasClass(target, 'pending-session-list') 
      || this.canContainerAcceptNewSession(el, target);
  }

  canContainerAcceptNewSession(sessionEl: HTMLElement, target: HTMLElement): boolean {
    if(target.children.length !== 0) {
      return false;
    } else {
      let sessionId = this.domUtilService.getSessionIdFromDOM(sessionEl);
      let containerTrackId = this.domUtilService.getContainerTrack(target);
      let globalStartAt = this.domUtilService.getContainerGlobalStartAt(target);
      return !this.isThereCollision(sessionId, globalStartAt, containerTrackId);
    }
  }

  isThereCollision(draggingSessionId: number, startAt: number, trackId: number): boolean {
    let draggingSession = this.getSessionById(draggingSessionId);
    if(draggingSession == null) {
      console.error('Session not found in board for id: ' + draggingSessionId);
    }
    for (var i = 0; i < this.allSessions.length; i++) {
      // skip pending session
      if(this.allSessions[i].start_at == null) {
        continue;
      }
      console.log('checking with: ' + this.allSessions[i].start_at);
      // no collision with itself
      if(this.allSessions[i].id !== draggingSessionId
        // same track
        && this.allSessions[i].track === trackId
        // existing session starts before the dragging session ends
        && this.allSessions[i].start_at < (startAt + draggingSession.duration)
        // existing session ends after the dragging session start
        && (this.allSessions[i].start_at + this.allSessions[i].duration) > startAt) {
        return true;
      }
    }
    return false;
  }

  onSessionChanged(changedSession: Session) {
    console.log('session changed in board');
    console.log(changedSession);
    this.agendaService.updateSession(this.agenda.id, changedSession);
  }

  onSessionMovedFromPending(sessionFromPending: Session) {
    console.log('session from pending in board');
    console.log(sessionFromPending);
    this.agendaService.updateSession(this.agenda.id, sessionFromPending);
  }

  private onDrop(args: [HTMLElement, HTMLElement]) {
    let [e, el] = args;
    // console.log('drop board');
    // console.log(e);
    // console.log(el);
    let sessionId = e.getAttribute('data-session-id');
    let columnType = el.getAttribute('data-column-type');
    if(columnType === 'relative') {
      this.changeSessionToPending(parseInt(sessionId));
    }
  }

  getSessionsForColumn(columnDate: Date, columnTrack: number): Session[] {
    let sessions:Session[] = [];
    for (let session of this.nonPendingSessions) {
      if (
        //add session to every track if it doesn't have a specific track
        (!session.track || session.track === columnTrack) 
        && this.isOnSameDay(this.addMinToDate(session.start_at, this.agenda.start_at) ,columnDate))
        sessions.push(session);
    }

    return sessions;
  }

  //return the calculated time as a Date
  addMinToDate(minute: number, date: string) {
    let minToMs = 60000;
    let baseMs = new Date(date).getTime();
    return new Date(baseMs + minToMs * minute);
  }

  isOnSameDay(day1: Date, day2: Date) {
    return day1.getFullYear() === day2.getFullYear() 
           && day1.getMonth() === day2.getMonth() 
           && day1.getDate() === day2.getDate();
  }

  changeSessionToPending(sessionId: number) {
    let session: Session = this.getSessionById(sessionId);
    if(session) {
      delete session.start_at;
      console.log('session to pending in board');
      console.log(session);
      this.agendaService.updateSession(this.agenda.id, session);
    } else {
      console.error('Session not found for id=' + sessionId + '.');
    }
  }

  getSessionById(sessionId: number): Session {
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
    let tempDate: Date = new Date(this.agenda.start_at);
    while (tempDate <= new Date(this.agenda.end_at)) {
      dates.push(new Date(tempDate.getTime()));
      tempDate.setDate(tempDate.getDate() + 1);
    }
    return dates;
  }

  getEventTracks(): Track[] {
    if (!this.agenda.tracks || this.agenda.tracks.length === 0) {
      return [];
    } else {
      return this.agenda.tracks;
    }
  }

  ngOnInit(): void {
    this.offsetDate = new Date(this.agenda.start_at);
    this.eventDates = this.getEventDates();
    this.eventTracks = this.getEventTracks();
    this.allSessions = this.agenda.sessions;
    let partioned = _.partition(this.allSessions, function(o:Session){return o.hasOwnProperty('start_at')});
    this.pendingSessions = partioned[1];
    this.nonPendingSessions = partioned[0];
  }
}
