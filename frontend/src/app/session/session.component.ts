import { Input, Component, OnInit, ViewContainerRef, ViewEncapsulation, ViewChild, TemplateRef } from '@angular/core';

import {Session} from '../session/session';

import { overlayConfigFactory } from 'angular2-modal';
import { Overlay } from 'angular2-modal';

import * as moment from 'moment';

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
  './css/vex-theme-default.css',
  './css/vex-theme-os.css',
  './css/vex-theme-plain.css',
  './css/vex-theme-wireframe.css',
  './css/vex-theme-flat-attack.css',
  './css/vex-theme-top.css',
  './css/vex-theme-bottom-right-corner.css'
  ],
  encapsulation: ViewEncapsulation.None
})
export class SessionComponent implements OnInit {
  constructor(public modal: Modal) {
  }
  @ViewChild('templateRef') public templateRef: TemplateRef<any>;
  @Input() session: Session;
  @Input() offsetDate: Date;

  HEIGHT_PER_15_MINS = 15; // px
  VERTICAL_MARGIN = 8; // 4*2px

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
    if (this.session.start_at != null) {
      this.height = Math.ceil(this.session.duration / 15) * this.HEIGHT_PER_15_MINS - this.VERTICAL_MARGIN;
    }
  }
}
