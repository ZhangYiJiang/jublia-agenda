import { Input, Component, OnInit } from '@angular/core';

import {Session} from '../session/session';

@Component({
  selector: 'my-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent implements OnInit {
  @Input() session: Session;
  @Input() offsetDate: Date;

  HEIGHT_PER_15_MINS = 15; // px
  VERTICAL_MARGIN = 8; // 4*2px

  height: number;

  getDisplayedTime(): string {

    let startMs = this.offsetDate.getTime() + 60000 * this.session.start_at;
    let startDate = new Date(startMs);
    let endDate = new Date(startMs + 60000 * this.session.duration);
    return this.getFormattedTime(startDate)
           + ' - '
           + this.getFormattedTime(endDate);
  }

  getFormattedTime(date: Date): string {
    return date.getUTCHours() + ':' + (date.getUTCMinutes()<10?'0':'') + date.getUTCMinutes();
  }

  ngOnInit(): void {
    this.height = Math.ceil(this.session.duration / 15) * this.HEIGHT_PER_15_MINS - this.VERTICAL_MARGIN;
  }
}
