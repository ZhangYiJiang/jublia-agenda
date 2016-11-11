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

export interface ContainerData {
  date: string;
  startAt: number;
  trackId: number;
}

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
  @Input() agenda: Agenda;

  // column's date
  @Input() day: Date;
  @Input() track: Track;
  @Input() dateIndex: number;
  @Input() trackIndex: number;

  // event start date
  @Input() offsetDate: Date;

  @Input() isPublic: boolean;
  @Input() isAnalytics: boolean;

  @Input() token: string;
  @Input() interestedSessionIds: number[];
  @Input() analyticsData: {};

  @Output() onSessionChanged = new EventEmitter<Session>();
  @Output() onSessionDeletedColumn = new EventEmitter<Session>();
  @Output() onSessionMovedFromPending = new EventEmitter<Session>();
  @Output() onSessionInterestChanged = new EventEmitter<[number, boolean]>();
  @Output() onSpeakerChanged = new EventEmitter<Speaker>();
  @Output() onSpeakerAdded2 = new EventEmitter<Speaker>();
  @Output() onVenueChanged = new EventEmitter<Venue>();
  @Output() onCreateSessionWithStart = new EventEmitter<[number,number,number]>();
  @Output() onVenueAdded2 = new EventEmitter<Venue>();
  
  containers: Container[] = [];

  hours = GlobalVariable.HOURS;

  private PLACEHOLDER_DURATION: number = 15;

  // offset from event start date to column's date, in number of minutes 
  private eventStartOffsetMin: number;

  displayedSessions: Session[];

  dropSub: any;

  constructor(
    private dragulaService: DragulaService, 
    private domUtilService: DOMUtilService,
    private agendaService: AgendaService,
  ) {
    this.dropSub = dragulaService.dropModel.subscribe((value: any) => {
      console.log('drop event in abs col');
      this.onDrop(value.slice(1));
    });
  }

  ngOnDestroy() {
    console.log('ondestroy abs');
    this.dropSub.unsubscribe();
  }

  private getAnalyticsDataForSession(session: Session): any {
    if(this.analyticsData == null) {
      // console.log('no analytics');
      return null;
    } else {
      return _.find(this.analyticsData, (v: any, key: string) => {
        // console.log(key === (session.id + ''));
        return key === (session.id + '');
      });
    }
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

  onSpeakerAdded(newSpeaker: Speaker) {
    // propagate to board
    this.onSpeakerAdded2.emit(newSpeaker);
  }

  onVenueEdited(editedVenue: Venue) {
    // propagate to board
    this.onVenueChanged.emit(editedVenue);
  }

  onVenueAdded(newVenue: Venue) {
    // propagate to board
    this.onVenueAdded2.emit(newVenue);
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
        _.remove(this.displayedSessions,(s: Session) => s.id === session.id);
      }
    }
  }

  private isInterestedInSession(session: Session): boolean {
    if (!this.interestedSessionIds) {
      return false;
    } else {
      return this.interestedSessionIds.indexOf(session.id) !== -1;
    }
  }

  private onDrop([e, el, source]: [HTMLElement, HTMLElement, HTMLElement]) {
    if (el.dataset['columnType'] !== 'absolute') return;
    
    const data = this.domUtilService.getContainerData(el);

    if (data.date === this.day.toISOString() && data.trackId === this.track.id) {
      const sessionId = this.domUtilService.getSessionIdFromDOM(e);
      const movedSession = this.getSessionById(sessionId);
      
      console.log(sessionId + ' moved to:' + data.date);
      
      if (!movedSession) {
        console.log('moved session ID ' + sessionId + ' cannot be found in board');
      }
      
      const isFromPending = (movedSession.start_at == null);
      
      movedSession.start_at = data.startAt;
      movedSession.track = data.trackId;
      movedSession.duration = movedSession.duration || GlobalVariable.DEFAULT_NEW_DURATION;
      
      if (isFromPending) {
        this.onSessionMovedFromPending.emit(movedSession);
      } else {
        this.onSessionChanged.emit(movedSession);
      }
    }
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
    console.log('public '+this.isPublic);
    console.log('analytics '+this.isAnalytics);
    const startTime = this.eventStartOffsetMin + container.start_at;
    //console.log(startTime);
    this.onCreateSessionWithStart.emit([startTime, this.dateIndex, this.trackIndex]);
  }

  private generateContainers() {
    // mins are relative to start of the day i.e. 8AM
    this.containers = [];
    
    for (let mins = this.hours[0] * 60, end = _.last(this.hours) * 60; mins < end; mins += this.PLACEHOLDER_DURATION) {
      this.containers.push({
        start_at: mins + this.eventStartOffsetMin,
        sessions: this.getSessionByStartTime(mins),
      });
    }
  }

  private getSessionByStartTime(start_time: number): Session[] {
    if (this.displayedSessions.length === 0) {
      return [];
    }
    
    const sessions = this.displayedSessions.filter(session => {
      const delta = session.start_at - start_time - this.eventStartOffsetMin;
      return delta >= 0 && delta < this.PLACEHOLDER_DURATION;
    });
    
    if (sessions.length > 1) {
      console.warn('multiple sessions with same start time');
    }
    
    return sessions;
  }

  addInNewSession(session:Session) {
    this.displayedSessions.push(session);
    this.generateContainers();
  }
  
  getContainerData(container: Container): ContainerData {
    return {
      startAt: container.start_at, 
      trackId: this.track.id,
      date: this.day.toISOString(),
    }
  }

  ngOnInit(): void {
    this.eventStartOffsetMin = moment(this.day).diff(moment(this.offsetDate), 'minutes', true);
    this.displayedSessions = this.sessions;

    if (this.isPublic) {
      this.hours = this.agendaService.getEventHours(this.agenda.sessions);
    }

    this.generateContainers();

    // let sortedSessions = _.sortBy(this.sessions, ['start_at']);
    // this.displayedSessions = this.addPlaceHolderSessions(sortedSessions);
    // console.log(this.displayedSessions);

    // if (this.isPublic) {
    //   this.dragulaService.destroy('column');
    // }
  }
}
