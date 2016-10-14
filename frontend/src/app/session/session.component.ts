import { Input, Component } from '@angular/core';

import {Session} from '../session/session';

@Component({
  selector: 'my-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent {
  @Input() session: Session;
  @Input() offsetDate: Date;

  getDisplayedTime(): string {

    let startMs = this.offsetDate.getTime() + 60000 * this.session.start_at;
    let startDate = new Date(startMs);
    let endDate = new Date(startMs + 60000 * this.session.duration);
    return this.getFormattedTime(startDate)
           + ' - '
           + this.getFormattedTime(endDate);
  }

  getFormattedTime(date: Date): string {
    return date.getHours() + ':' + (date.getMinutes()<10?'0':'') + date.getMinutes();
  }
}
