import { Input, Component } from '@angular/core';

import {Session} from '../session/session';

@Component({
  selector: 'relative-column',
  templateUrl: './relative-column.component.html',
  styleUrls: ['./relative-column.component.css']
})
export class RelativeColumnComponent {
  @Input()
  sessions: Session[];
}
