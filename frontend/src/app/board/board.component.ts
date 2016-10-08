import { Input, Component } from '@angular/core';

import {Session} from '../session/session';

@Component({
  selector: 'board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css']
})
export class BoardComponent {
  @Input()
  sessions: Session[];
}
