import { Input, Component,trigger, state, style, transition, animate, Output, EventEmitter } from '@angular/core';

import * as _ from 'lodash';

import { Session } from '../session/session';
import { Speaker } from '../speaker/speaker';
import { Agenda } from '../agenda/agenda';
import { Venue } from '../venue/venue';

const MARGIN_LEFT_SHOW: string = '0px';
const MARGIN_LEFT_HIDE: string = '-200px';
const MARGIN_RIGHT_SHOW: string = '245px';
const MARGIN_RIGHT_HIDE: string = 'px';

@Component({
  selector: 'relative-column',
  templateUrl: './relative-column.component.html',
  styleUrls: ['./relative-column.component.css'],
  animations: [
    trigger('colMarginTrigger', [
      state('open', style({ 'margin-left': MARGIN_LEFT_SHOW})),
      state('close', style({ 'margin-left': MARGIN_LEFT_HIDE}))
    ]),
    trigger('iconTrigger', [
      state('open', style({ transform: 'rotate(0deg)' })),
      state('close', style({ transform: 'rotate(180deg)' }))
    ])
  ]
})

export class RelativeColumnComponent {
  @Input() sessions: Session[];
  @Input() offsetDate: Date;

  @Input()
  agenda: Agenda;

  @Output() onSessionChanged = new EventEmitter<Session>();
  @Output() onSessionDeletedColumn = new EventEmitter<Session>();
  @Output() onSessionMovedFromPending = new EventEmitter<Session>();
  @Output() onSessionInterestChanged = new EventEmitter<[number, boolean]>();
  @Output() onSpeakerChanged = new EventEmitter<Speaker>();
  @Output() onSpeakerAdded2 = new EventEmitter<Speaker>();
  @Output() onVenueChanged = new EventEmitter<Venue>();
  @Output() onVenueAdded2 = new EventEmitter<Venue>();

  colState = 'open';
  isColShown = true;

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
    console.log('session delete in rel column');
    this.removeSession(deletedSession);
    this.onSessionDeletedColumn.emit(deletedSession);
  }

  removeSession(session: Session) {
    _.remove(this.sessions, (s: Session) => s.id === session.id);
  }

  toggleState(): void {
    this.colState = this.isColShown ? 'close' : 'open';
    this.isColShown = !this.isColShown;
  }
}
