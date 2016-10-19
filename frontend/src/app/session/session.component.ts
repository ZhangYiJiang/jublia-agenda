import { Input, Component, OnInit, ViewContainerRef, ViewEncapsulation, ViewChild, TemplateRef } from '@angular/core';

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

  speakersObj = {};
  trackObj = {};

  HEIGHT_PER_15_MINS = 15; // px
  VERTICAL_MARGIN = 4;

  height: number;

  clicked(event: DocumentEvent) {
    console.log(event);
    this.modal
      .open(this.templateRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
    console.log();
  }

  getDisplayedDate(): string {
    let startMs = this.offsetDate.getTime() + 60000 * this.session.start_at;
    let date = new Date(startMs);
    return moment(date).utc().format("dddd, MMMM Do YYYY");
  }

  getDisplayedTime(): string {
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

  ngOnInit(): void {
    // TODO: move this logic up to agenda/board component to avoid repeated operations
    this.speakersObj = _.keyBy(this.agenda.speakers, 'id');
    this.trackObj = _.keyBy(this.agenda.tracks, 'id');

    if (this.session.start_at != null) {
      this.height = Math.ceil(this.session.duration / 15) * this.HEIGHT_PER_15_MINS - this.VERTICAL_MARGIN;
    }
  }
}
