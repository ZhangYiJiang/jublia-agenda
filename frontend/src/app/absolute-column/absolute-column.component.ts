import { Component, Input, OnInit, Output, EventEmitter, OnDestroy } from '@angular/core';

import { DragulaService } from 'ng2-dragula/ng2-dragula';
import * as _ from 'lodash';
import * as moment from 'moment';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { Track } from '../track/track';
import { Speaker } from '../speaker/speaker';
import { Venue } from '../venue/venue';
import { AgendaService } from '../agenda/agenda.service';

import { DOMUtilService } from '../util/dom.util.service';
import { GlobalVariable } from '../globals';

export class Container {
  start_at: number;
  sessions: Session[];
}

@Component({
  selector: 'absolute-column',
  templateUrl: './absolute-column.component.html',
  styleUrls: ['./absolute-column.component.css']
})
export class AbsoluteColumnComponent implements OnInit, OnDestroy {
  @Input() sessions: Session[];

  @Input()
  agenda: Agenda;

  // column's date
  @Input() day: Date;
  @Input() track: Track;

  // event start date
  @Input() offsetDate: Date;

  @Input() isPublic: boolean;

  @Input() token: string;
  @Input() interestedSessionIds: number[];

  @Output() onSessionChanged = new EventEmitter<Session>();
  @Output() onSessionDeletedColumn = new EventEmitter<Session>();
  @Output() onSessionMovedFromPending = new EventEmitter<Session>();
  @Output() onSessionInterestChanged = new EventEmitter<[number, boolean]>();
  @Output() onSpeakerChanged = new EventEmitter<Speaker>();
  @Output() onVenueChanged = new EventEmitter<Venue>();
  @Output() onCreateSessionWithStart = new EventEmitter<number>();

  containers: Container[] = [];

  hours = ['8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00'];

  private PLACEHOLDER_DURATION: number = 15;
  private DEFAULT_DAY_START_OFFSET_MIN: number = 8 * 60; // default start time for column is 8AM

  

  // offset from start of the column's date to start of displayed time withn the date (8AM, etc)
  private dayStartOffsetMin: number;

  // offset from event start date to column's date, in number of minutes 
  private eventStartOffsetMin: number;

  displayedSessions: Session[];

  dropSub: any;

  constructor(private dragulaService: DragulaService, 
    private domUtilService: DOMUtilService) {
    this.dropSub = dragulaService.dropModel.subscribe((value: any) => {
      console.log('drop event in abs col');
      this.onDrop(value.slice(1));
    });
  }

  ngOnDestroy() {
    console.log('ondestroy abs');
    this.dropSub.unsubscribe();
  }

  onSessionEdited(editedSession: Session) {
    // propagate to board
    this.onSessionChanged.emit(editedSession);
  }

  onSessionInterestEdited(event: [number, boolean]) {
    // propagate to board
    this.onSessionInterestChanged.emit(event);
  }

  onSpeakerEdited(editedSpeaker: Speaker) {
    // propagate to board
    this.onSpeakerChanged.emit(editedSpeaker);
  }

  onVenueEdited(editedVenue: Venue) {
    // propagate to board
    this.onVenueChanged.emit(editedVenue);
  }

  onSessionDeleted(deletedSession: Session) {
    // propagate to board
    console.log('session delete in abs column');
    this.removeSession(deletedSession);
    this.onSessionDeletedColumn.emit(deletedSession);
  }

  private removeSession(session: Session) {
    for (var i = 0; i < this.containers.length; i++) {
      for (var j = 0; j < this.containers[i].sessions.length; ++j) {
        _.remove(this.containers[i].sessions, (s: Session) => s.id === session.id);
      }
    }
  }

  private isInterestedInSession(session: Session): boolean {
    if(!this.interestedSessionIds) {
      return false;
    } else {
      return this.interestedSessionIds.indexOf(session.id) !== -1;
    }
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

  private isEventForThisContainer(containerDate: Date, containerTrackId: number): boolean {
    return containerDate.toISOString() === this.day.toISOString() && containerTrackId === this.track.id;
  }

  private onDrop(args: [HTMLElement, HTMLElement, HTMLElement]) {
    let [e, el, source] = args;
    if (this.isEventForAbsoluteColumn(el)) {
      let containerDate = this.domUtilService.getContainerDate(el);
      let containerTrackId = this.domUtilService.getContainerTrack(el);
      if (this.isEventForThisContainer(containerDate, containerTrackId)) {
        let sessionId = this.domUtilService.getSessionIdFromDOM(e);
        console.log(sessionId + ' moved to:');
        console.log(containerDate.toLocaleString());
        let startAt = this.domUtilService.getContainerStartAt(el);
        console.log(startAt);
        this.handleSessionDropped(sessionId, containerTrackId, startAt);
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

  private handleSessionDropped(sessionId: number, trackId: number, startAt: number) {
    let movedSession = this.getSessionById(sessionId);
    if(movedSession) {
      let globalStartTime = this.getGlobalStartTimeFromDisplayedStartTime(startAt);
      this.updateDroppedSession(movedSession, globalStartTime, trackId);
    } else {
      console.log('moved session ID ' + sessionId + ' cannot be found in board');
    }
  }

  private getGlobalStartTimeFromDisplayedStartTime(displayedStartTime: number) {
    return displayedStartTime + this.dayStartOffsetMin + this.eventStartOffsetMin;
  }

  private updateDroppedSession(session: Session, newStartTime: number, trackId: number) {
    let isFromPending = (session.start_at == null);
    session.start_at = newStartTime;
    if (session.duration == null) {
      session.duration = GlobalVariable.DEFAULT_NEW_DURATION;
    }
    session.track = trackId;
    if(isFromPending) {
      this.onSessionMovedFromPending.emit(session);
    } else {
      this.onSessionChanged.emit(session);
    }
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
    console.error('cannot find session ' + sessionId + ' in containers:');
    for (var i = 0; i < this.containers.length; i++) {
        console.log(this.containers[i]);
      for (var j = 0; j < this.containers[i].sessions.length; ++j) {
        console.log(this.containers[i].sessions[j]);
      }
    }
    return null;
  }

  addNewSession(container: Container){
    let startTime = this.dayStartOffsetMin+this.eventStartOffsetMin+container.start_at;
    //console.log(startTime);
    this.onCreateSessionWithStart.emit(startTime);
  }

  private generateContainers() {
    // mins are relative to start of the day i.e. 8AM
    this.containers = [];
    for (var mins = 0; mins < 12 * 60; mins += this.PLACEHOLDER_DURATION) {
      this.containers.push({
        start_at: mins,
        sessions: this.getSessionByStartTime(mins)
      });
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

  addInNewSession(session:Session) {
    this.displayedSessions.push(session);
    this.generateContainers();
    console.log('col called');
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

    // if (this.isPublic) {
    //   this.dragulaService.destroy('column');
    // }
  }
}
