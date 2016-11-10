import { Input, Component, trigger, state, style, transition, animate, Output, EventEmitter, OnInit } from '@angular/core';

import * as _ from 'lodash';

import { Session } from '../session/session';
import { Speaker } from '../speaker/speaker';
import { Agenda } from '../agenda/agenda';
import { Venue } from '../venue/venue';

@Component({
  selector: 'session-list',
  templateUrl: './session-list.component.html',
  styleUrls: ['./session-list.component.css']
})

export class SessionListComponent implements OnInit {

  @Input() agenda: Agenda;
  @Input() isPublic: boolean;
  @Input() isAnalytics: boolean;
  @Input() token: string;
  @Input() interestedSessionIds: number[];
  @Input() analyticsData: {};
  @Input() sessions: Session[];
  allSessions: Session[];
  // event start date
  @Input() offsetDate: Date;

  @Output() onSessionChanged = new EventEmitter<Session>();
  @Output() onSessionDeletedColumn = new EventEmitter<Session>();
  @Output() onSessionMovedFromPending = new EventEmitter<Session>();
  @Output() onSessionInterestChanged = new EventEmitter<[number, boolean]>();
  @Output() onSpeakerChanged = new EventEmitter<Speaker>();
  @Output() onSpeakerAdded2 = new EventEmitter<Speaker>();
  @Output() onVenueChanged = new EventEmitter<Venue>();
  @Output() onCreateSessionWithStart = new EventEmitter<[number,number,number]>();
  @Output() onVenueAdded2 = new EventEmitter<Venue>();


  ngOnInit(): void {
    this.allSessions = this.sessions;
  }

  private isInterestedInSession(session: Session): boolean {
    if(!this.interestedSessionIds) {
      return false;
    } else {
      return this.interestedSessionIds.indexOf(session.id) !== -1;
    }
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
    console.log('session delete in session list');
    this.onSessionDeletedColumn.emit(deletedSession);
  }

}
