import { Input, Component, OnInit, ViewContainerRef, ViewEncapsulation, ViewChild, TemplateRef, EventEmitter, Output } from '@angular/core';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';

import { overlayConfigFactory } from 'angular2-modal';
import { Overlay } from 'angular2-modal';

import * as moment from 'moment';
import * as _ from 'lodash';

import {
  VEXBuiltInThemes,
  Modal,
  DialogPreset,
  DialogFormModal,
  DialogPresetBuilder,
  VEXModalContext,
  VexModalModule,
  providers
} from 'angular2-modal/plugins/vex';

@Component({
  selector: 'my-session',
  templateUrl: './session.component.html',
  styleUrls: [
  './session.component.css',
  './css/vex.css',
  './css/vex-theme-default.css'
  ],
  encapsulation: ViewEncapsulation.None
})
export class SessionComponent implements OnInit {
  constructor(public modal: Modal) {
  }
  @ViewChild('templateRef') public templateRef: TemplateRef<any>;
  @Input() session: Session;
  @Input() offsetDate: Date;
  @Input()
  agenda: Agenda;
  @Input() isPublic: boolean;

  @Input()
  token: string;

  @Input()
  interested: boolean;

  interestedButtonText: string;

  @Output() onSessionEdited = new EventEmitter<Session>();
  @Output() onSessionInterestEdited = new EventEmitter<[number, boolean]>();

  speakersObj = {};
  trackObj = {};

  HEIGHT_PER_15_MINS = 20; // px
  VERTICAL_MARGIN = 4;

  height: number;
  red: number;
  green: number;
  blue: number;

  updateInterest() {
    this.interested = !this.interested;
    this.updateInterestButtonText();
    this.onSessionInterestEdited.emit([this.session.id, this.interested]);
  }

  updateSession(event: any) {
    console.log(event);
    if(typeof event.description === 'string') {
      console.log(this.session);
      this.session.description = event.description;
      this.onSessionEdited.emit(this.session);
    } else if(typeof event.name === 'string') {
      this.session.name = event.name;
      this.onSessionEdited.emit(this.session);
    }
  }

  clicked(event: DocumentEvent) {
    this.modal
      .open(this.templateRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
  }

  getDisplayedDate(): string {
    if(this.session.start_at == null) {
      return ''
    }
    let startMs = this.offsetDate.getTime() + 60000 * this.session.start_at;
    let date = new Date(startMs);
    return moment(date).utc().format("ddd, MMMM Do YYYY");
  }

  getDisplayedTime(): string {
    if(this.session.start_at == null) {
      return '';
    }
    let startMs = this.offsetDate.getTime() + 60000 * this.session.start_at;
    let startDate = new Date(startMs);
    let endDate = new Date(startMs + 60000 * this.session.duration);
    return this.getFormattedTime(startDate)
      + ' - '
      + this.getFormattedTime(endDate);
  }

  getFormattedTime(date: Date): string {
    return date.getUTCHours() + ':' + (date.getUTCMinutes() < 10 ? '0' : '') + date.getUTCMinutes();
  }

  getAltFormattedTime(date: Date): string {
    return moment(date).utc().format("hA");
  }

  updateInterestButtonText() {
    if(this.interested) {
      this.interestedButtonText = 'Interested. Click to revert.';
    } else {
      this.interestedButtonText = 'Click to indicate interest.';
    }
  }

  ngOnInit(): void {
    // TODO: move this logic up to agenda/board component to avoid repeated operations
    this.speakersObj = _.keyBy(this.agenda.speakers, 'id');
    this.trackObj = _.keyBy(this.agenda.tracks, 'id');

    this.updateInterestButtonText();

    if (this.session.start_at != null) {
      this.height = Math.ceil(this.session.duration / 15) * this.HEIGHT_PER_15_MINS - this.VERTICAL_MARGIN;
    }

    let popularityRatio = 0;
    
    if (this.isPublic) {
      popularityRatio = this.session.popularity / 10; // TODO: divide by highest popularity number?
    }

    // white-pink-red gradient
    this.red = 255;
    this.green = 95 + (1 - popularityRatio) * 160;
    this.blue = 95 + (1 - popularityRatio) * 160;
  }
}
