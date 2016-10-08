import { Input, Component,trigger, state, style, transition,animate } from '@angular/core';

import {Session} from '../session/session';

const MARGIN_SHOW: string = '0px';
const MARGIN_HIDE: string = '-200px';

@Component({
  selector: 'relative-column',
  templateUrl: './relative-column.component.html',
  styleUrls: ['./relative-column.component.css'],
  animations: [
	  trigger('colMarginTrigger', [
	    state('open', style({ 'margin-left': MARGIN_SHOW})),
	    state('close', style({ 'margin-left': MARGIN_HIDE})),
	    transition('close => open', animate('300ms ease-in')),
	    transition('open => close', animate('300ms 300ms ease-out'))
	  ]),
	  trigger('iconTrigger', [
      state('open', style({ transform: 'rotate(0deg)' })),
      state('close', style({ transform: 'rotate(180deg)' })),
      transition('close => open', animate('300ms 300ms ease-in')),
      transition('open => close', animate('300ms 300ms'))
  	])
  ]
})

export class RelativeColumnComponent {
  @Input()
  sessions: Session[];
  
  colState = 'open';
  isColShown = true;

  toggleState(): void {
  	this.colState = this.isColShown ? 'close' : 'open';
  	this.isColShown = !this.isColShown;
  }
}
