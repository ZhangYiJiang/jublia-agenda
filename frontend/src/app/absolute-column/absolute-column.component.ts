import { Component, Input, OnInit } from '@angular/core';

import { DragulaService } from 'ng2-dragula/ng2-dragula';
import * as _ from 'lodash';
import * as moment from 'moment';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { Track } from '../track/track';
import { AgendaService } from '../agenda/agenda.service';

import { DOMUtilService } from '../util/dom.util.service';

@Component({
  selector: 'absolute-column',
  templateUrl: './absolute-column.component.html',
  styleUrls: ['./absolute-column.component.css']
})
export class AbsoluteColumnComponent implements OnInit {
  @Input() sessions: Session[];

  @Input()
  agenda: Agenda;

  // column's date
  @Input() day: Date;
  @Input() track: Track;

  // event start date
  @Input() offsetDate: Date;

  containers: any[] = [];

  private PLACEHOLDER_DURATION: number = 15;
  private DEFAULT_DAY_START_OFFSET_MIN: number = 8 * 60; // default start time for column is 8AM

  private DEFAULT_NEW_DURATION: number = 60;

  // offset from start of the column's date to start of displayed time withn the date (8AM, etc)
  private dayStartOffsetMin: number;

  // offset from event start date to column's date, in number of minutes 
  private eventStartOffsetMin: number;

  displayedSessions: Session[];

  constructor(private dragulaService: DragulaService,
    private agendaService: AgendaService,
    private domUtilService: DOMUtilService) {
    dragulaService.dropModel.subscribe((value: any) => {
      // console.log(`drop: ${value}`);
      this.onDrop(value.slice(1));
    });

    // dragulaService.over.subscribe((value: any) => {
    // console.log(`drop: ${value}`);
    // this.onOver(value.slice(1));
    // });
  }

  private getColumnDate(el: HTMLElement): Date {
    return new Date(el.getAttribute('data-date'));
  }

  private getColumnTrack(el: HTMLElement): number {
    return +el.getAttribute('data-track-id');
  }

  private isEventForAbsoluteColumn(el: HTMLElement): boolean {
    let columnType = el.getAttribute('data-column-type');
    return columnType === 'absolute';
  }

  private isEventForThisColumn(columnDate: Date, columnTrackId: number): boolean {
    return columnDate.toISOString() === this.day.toISOString() && columnTrackId === this.track.id;
  }

  private onDrop(args: [HTMLElement, HTMLElement, HTMLElement]) {
    let [e, el, source] = args;
    if (this.isEventForAbsoluteColumn(el)) {
      let columnDate = this.getColumnDate(el);
      let columnTrackId = this.getColumnTrack(el);
      if (this.isEventForThisColumn(columnDate, columnTrackId)) {
        let sessionId = parseInt(e.getAttribute('data-session-id'));
        console.log(sessionId + ' moved to:');
        console.log(columnDate.toLocaleString());
        let startAt = parseInt(el.getAttribute('data-container-start-at'));
        console.log(startAt);
        this.handleSessionDropped(sessionId, columnTrackId, startAt);
        // this.refreshSessions();
      }
    }

    if (this.isEventForAbsoluteColumn(source)) {
      let columnDate = this.getColumnDate(source);
      let columnTrackId = this.getColumnTrack(source);
      if (this.isEventForThisColumn(columnDate, columnTrackId)) {
        // this.refreshSessions();
      }
    }
  }

  private onOver(args: [HTMLElement, HTMLElement, HTMLElement]) {
    let [e, el, container] = args;
    let moved = !(el === container);
    if (this.isEventForAbsoluteColumn(container)) {
      let columnDate = this.getColumnDate(container);
      let columnTrackId = this.getColumnTrack(container);
      if (this.isEventForThisColumn(columnDate, columnTrackId)) {
        let sessionId = parseInt(e.getAttribute('data-session-id'));
        console.log(sessionId + ' moved container:');
        console.log(columnDate.toLocaleString());
        console.log('track ' + columnTrackId);
      }
    }
    if (this.isEventForAbsoluteColumn(el)) {
      let columnDate = this.getColumnDate(el);
      let columnTrackId = this.getColumnTrack(el);
      if (this.isEventForThisColumn(columnDate, columnTrackId)) {
        let sessionId = parseInt(e.getAttribute('data-session-id'));
        console.log(sessionId + ' moved el:');
        console.log(columnDate.toLocaleString());
        console.log('track ' + columnTrackId);
      }
    }
  }

  private reCalculateSessionStartTime(sessionId: number): number {
    let duration: number = 0;
    for (var i = 0; i < this.displayedSessions.length; ++i) {
      let session: Session = this.displayedSessions[i];
      if (session.id === sessionId) {
        break;
      } else if (session.placeholder) {
        duration += this.PLACEHOLDER_DURATION;
      } else {
        duration += session.duration;
      }
    }
    let globalStartTime = this.getGlobalStartTimeFromDisplayedStartTime(duration);
    return globalStartTime;
  }

  private refreshSessions() {
    for (var i = 0; i < this.displayedSessions.length; i++) {
      if (!this.displayedSessions[i].placeholder) {
        let newStartTime = this.reCalculateSessionStartTime(this.displayedSessions[i].id);
        this.displayedSessions[i].start_at = newStartTime;
        this.agendaService.updateSession(this.agenda.id, this.displayedSessions[i]);
      }
    }
  }

  private handleSessionDropped(sessionId: number, trackId: number, startAt: number) {
    let movedSession = this.getSessionById(sessionId);
    let globalStartTime = this.getGlobalStartTimeFromDisplayedStartTime(startAt);
    this.updateDroppedSession(movedSession, globalStartTime, trackId);
  }

  private getGlobalStartTimeFromDisplayedStartTime(displayedStartTime: number) {
    return displayedStartTime + this.dayStartOffsetMin + this.eventStartOffsetMin;
  }

  private updateDroppedSession(session: Session, newStartTime: number, trackId: number) {
    session.start_at = newStartTime;
    if (session.duration == null) {
      session.duration = this.DEFAULT_NEW_DURATION;
    }
    session.track = trackId;
    this.agendaService.updateSession(this.agenda.id, session);
  }

  // Get start minutes of session relative to start of the day
  getRelativeStartMin(session: Session): number {
    if (this.eventStartOffsetMin % 60 !== 0) {
      console.error('offset date and current date diff is not exact multiple of days');
    }
    return session.start_at - this.eventStartOffsetMin - this.dayStartOffsetMin;
  }

  getSessionById(sessionId: number): Session {
    for (var i = 0; i < this.containers.length; i++) {
      for (var j = 0; j < this.containers[i].sessions.length; ++j) {
        if (this.containers[i].sessions[j].id === sessionId) {
          return this.containers[i].sessions[j];
        }
      }
    }

    return null;
  }

  addPlaceHolderSessions(rawSessions: Session[]): Session[] {
    let newSessions: Session[] = [];
    let lastSessionMins: number = 0;
    for (var i = 0; i < rawSessions.length; i++) {
      let relativeStartMins = this.getRelativeStartMin(rawSessions[i]);
      if (relativeStartMins < 0) {
        console.error('Start minutes relative to start of the day smaller than zero.');
      }
      if (relativeStartMins - lastSessionMins < 0) {
        console.warn('Start minutes relative to last session smaller than zero, session conflict.');
        console.warn('Conflicted sessions: ');
        console.warn(rawSessions[i - 1].name);
        console.warn(rawSessions[i].name);
      }
      // round down number of placeholders
      let noOfPlaceholders = Math.floor((relativeStartMins - lastSessionMins) / this.PLACEHOLDER_DURATION);
      for (var j = 0; j < noOfPlaceholders; ++j) {
        newSessions.push(<Session>{
          placeholder: true
        })
      }
      newSessions.push(rawSessions[i]);
      lastSessionMins = relativeStartMins + rawSessions[i].duration;
    }
    // placeholders after the last session
    // allow 6 hours
    for (var i = 0; i < (60 / this.PLACEHOLDER_DURATION * 6); ++i) {
      newSessions.push(<Session>{
        placeholder: true
      })
    }
    return newSessions;
  }

  private generateContainers() {
    let mins = 0;
    // mins are relative to start of the day i.e. 8AM
    for (var i = 0; i < 12 * 60; ++i) {
      this.containers.push({
        start_at: mins,
        sessions: this.getSessionByStartTime(mins)
      });
      mins += this.PLACEHOLDER_DURATION;
    }
  }

  private getSessionByStartTime(start_time: number): Session[] {
    if (this.displayedSessions.length === 0) {
      return [];
    }
    let sessions: Session[] = [];
    for (var i = 0; i < this.displayedSessions.length; i++) {
      let delta = this.getRelativeStartMin(this.displayedSessions[i]) - start_time;
      if (delta >= 0 && delta < this.PLACEHOLDER_DURATION) {
        sessions.push(this.displayedSessions[i]);
      }
    }
    if (sessions.length > 1) {
      console.warn('multiple sessions with same start time');
    }
    return sessions;
  }

  ngOnInit(): void {
    this.eventStartOffsetMin = moment(this.day).diff(moment(this.offsetDate), 'minutes', true);
    if (this.sessions.length > 0) {
      let firstSessionMins = this.getRelativeStartMin(this.sessions[0]);
      if (firstSessionMins < this.DEFAULT_DAY_START_OFFSET_MIN) {
        console.error('Earliest session before 8AM, session before 8AM will be hidden.');
      }
    }
    this.dayStartOffsetMin = this.DEFAULT_DAY_START_OFFSET_MIN;
    this.displayedSessions = this.sessions;

    this.generateContainers();
    // let sortedSessions = _.sortBy(this.sessions, ['start_at']);
    // this.displayedSessions = this.addPlaceHolderSessions(sortedSessions);
    // console.log(this.displayedSessions);
  }
}
