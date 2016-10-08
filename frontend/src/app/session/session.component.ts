import { Input, Component } from '@angular/core';

import {Session} from '../session/session';

@Component({
  selector: 'my-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent {
  @Input()
  session: Session;
}
